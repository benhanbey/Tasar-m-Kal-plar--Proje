"""Saf fizyolojik hesaplar (rapor bolum 6.1-6.2)."""
from __future__ import annotations

from typing import Iterable

from .models import SetLog, Sex


def bmr_mifflin_st_jeor(weight_kg: float, height_cm: float, age: int, sex: Sex) -> float:
    s = 5 if sex is Sex.MALE else -161
    return 10 * weight_kg + 6.25 * height_cm - 5 * age + s


def tdee(bmr: float, activity_factor: float) -> float:
    if activity_factor <= 0:
        raise ValueError("Aktivite carpani pozitif olmalidir.")
    return bmr * activity_factor


def one_rep_max_brzycki(weight_kg: float, reps: int) -> float:
    """1RM = W / (1.0278 - 0.0278 * R); formul 1-30 tekrar icin gecerli kabul edilir."""
    if not 1 <= reps <= 30:
        raise ValueError("Brzycki formulu 1-30 tekrar icin kullanilir.")
    return weight_kg / (1.0278 - 0.0278 * reps)


def volume_load(sets: Iterable[SetLog]) -> float:
    """VL = toplam(tekrar * yuk). Her SetLog tek bir seti temsil eder."""
    return sum(s.reps * s.weight_kg for s in sets)
