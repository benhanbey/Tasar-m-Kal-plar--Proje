"""ADAPTER kalibi (yapisal): farkli dis servis verilerinin ic formata donusturulmesi.

Problem: Apple Health, Strava ve takviye veritabani farkli alan adlari/birimler sunar.
Is mantiginin her servise ozel kod icermesi yerine, her servis ortak bir hedef arayuze
uyarlanir (Object Adapter: composition).

Roller:
  Target   -> FitnessDataTarget, SupplementCatalogTarget (ABC)
  Adaptee  -> AppleHealthService, StravaService, ExternalSupplementAPI
  Adapter  -> AppleHealthAdapter, StravaAdapter, SupplementAPIAdapter
  Client   -> ActivityAggregator
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import NormalizedActivity, SupplementInfo

# ---------------- Adaptee'ler (dis servisleri taklit eden sinifler) ----------------


class AppleHealthService:
    def get_step_and_calorie_data(self) -> dict:
        return {"steps": 10450, "active_kcal": 480}


class StravaService:
    """Adim degil mesafe (metre) ve 'calories' alanini dondurur."""

    def fetch_latest_activity(self) -> dict:
        return {"distance_m": 5200.0, "calories": 410, "moving_time_s": 1800}


class ExternalSupplementAPI:
    def fetch_vendor_data(self) -> dict:
        return {"supp_name": "Creatine Monohydrate", "dosage_mg": 5000}


# ---------------- Target arayuzleri ----------------


class FitnessDataTarget(ABC):
    @abstractmethod
    def get_normalized_activity(self) -> NormalizedActivity: ...


class SupplementCatalogTarget(ABC):
    @abstractmethod
    def get_supplement_info(self) -> SupplementInfo: ...


# ---------------- Adapter'ler ----------------


class AppleHealthAdapter(FitnessDataTarget):
    def __init__(self, service: AppleHealthService) -> None:
        self._service = service

    def get_normalized_activity(self) -> NormalizedActivity:
        raw = self._service.get_step_and_calorie_data()
        return NormalizedActivity(raw["steps"], raw["active_kcal"], "AppleHealth")


class StravaAdapter(FitnessDataTarget):
    STEP_LENGTH_M = 0.762  # ortalama adim uzunlugu ile mesafeden adim tahmini

    def __init__(self, service: StravaService) -> None:
        self._service = service

    def get_normalized_activity(self) -> NormalizedActivity:
        raw = self._service.fetch_latest_activity()
        steps = round(raw["distance_m"] / self.STEP_LENGTH_M)
        return NormalizedActivity(steps, int(raw["calories"]), "Strava")


class SupplementAPIAdapter(SupplementCatalogTarget):
    def __init__(self, api: ExternalSupplementAPI) -> None:
        self._api = api

    def get_supplement_info(self) -> SupplementInfo:
        raw = self._api.fetch_vendor_data()
        return SupplementInfo(raw["supp_name"], raw["dosage_mg"] / 1000)  # mg -> g


class ActivityAggregator:
    """Client: kaynak sayisindan bagimsiz, yalnizca Target arayuzunu bilir."""

    def __init__(self, sources: list[FitnessDataTarget]) -> None:
        self._sources = list(sources)

    def collect(self) -> list[NormalizedActivity]:
        return [s.get_normalized_activity() for s in self._sources]

    def total_burned_calories(self) -> int:
        return sum(a.burned_calories for a in self.collect())
