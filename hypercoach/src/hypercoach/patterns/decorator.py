"""DECORATOR kalibi (yapisal): receteye calisma zamaninda davranis/kisit eklemek.

Problem: Bir recete bazen deload (hacim %10 dusur), bazen sakatlik kisiti (riskli
egzersizleri cikar), bazen ikisi birden gerektirir. Her kombinasyon icin alt sinif
(DeloadInjuryPrescription ...) patlamasi yerine, kisitlar birbirinin icine sarilir.

Roller:
  Component          -> PrescriptionComponent (ABC)
  ConcreteComponent  -> BasePrescription
  Decorator          -> PrescriptionDecorator (ABC)
  ConcreteDecorator  -> DeloadDecorator, InjuryRestrictionDecorator
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace

from ..config import ConfigurationManager
from ..models import Prescription

# Sakatlik bolgesi -> kacinilacak egzersizler
INJURY_RESTRICTIONS: dict[str, frozenset[str]] = {
    "lower_back": frozenset({"Deadlift", "Barbell Row", "Romanian Deadlift", "Squat"}),
    "shoulder": frozenset({"Overhead Press", "Incline Dumbbell Press", "Bench Press"}),
    "knee": frozenset({"Squat", "Leg Press"}),
}


class PrescriptionComponent(ABC):
    @abstractmethod
    def get_prescription(self) -> Prescription: ...


class BasePrescription(PrescriptionComponent):
    def __init__(self, prescription: Prescription) -> None:
        self._prescription = prescription

    def get_prescription(self) -> Prescription:
        return self._prescription


class PrescriptionDecorator(PrescriptionComponent, ABC):
    def __init__(self, wrapped: PrescriptionComponent) -> None:
        self._wrapped = wrapped


class DeloadDecorator(PrescriptionDecorator):
    def get_prescription(self) -> Prescription:
        p = self._wrapped.get_prescription()
        factor = ConfigurationManager().get("deload_volume_factor")
        return replace(
            p,
            volume_multiplier=round(p.volume_multiplier * factor, 4),
            notes=p.notes + ("Deload: hacim dusuruldu",),
        )


class InjuryRestrictionDecorator(PrescriptionDecorator):
    def __init__(self, wrapped: PrescriptionComponent, injuries: tuple[str, ...]) -> None:
        super().__init__(wrapped)
        self._injuries = injuries

    def get_prescription(self) -> Prescription:
        p = self._wrapped.get_prescription()
        banned: set[str] = set()
        for injury in self._injuries:
            banned |= INJURY_RESTRICTIONS.get(injury, frozenset())
        kept = tuple(e for e in p.exercises if e not in banned)
        removed = [e for e in p.exercises if e in banned]
        notes = p.notes + ((f"Sakatlik nedeniyle cikarildi: {', '.join(removed)}",) if removed else ())
        return replace(p, exercises=kept, notes=notes)
