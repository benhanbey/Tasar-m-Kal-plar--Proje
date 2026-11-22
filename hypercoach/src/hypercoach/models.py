"""Alan modeli: kullanici profili, set kaydi, receteler ve normalize aktivite verisi."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Sex(Enum):
    MALE = "male"
    FEMALE = "female"


class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Goal(Enum):
    HYPERTROPHY = "hypertrophy"
    STRENGTH = "strength"
    ENDURANCE = "endurance"


@dataclass(frozen=True)
class UserProfile:
    age: int
    weight_kg: float
    height_cm: float
    sex: Sex
    level: Level
    goal: Goal
    activity_factor: float = 1.55
    injuries: tuple[str, ...] = ()  # orn. ("lower_back",)

    def __post_init__(self) -> None:
        if self.age <= 0 or self.weight_kg <= 0 or self.height_cm <= 0:
            raise ValueError("Yas, kilo ve boy pozitif olmalidir.")


@dataclass(frozen=True)
class SetLog:
    """Kullanicinin bir sette girdigi veri (FR-04)."""
    exercise: str
    weight_kg: float
    reps: int
    rpe: float

    def __post_init__(self) -> None:
        if self.reps <= 0 or self.weight_kg < 0:
            raise ValueError("Tekrar pozitif, agirlik negatif olmayan olmalidir.")
        if not 1 <= self.rpe <= 10:
            raise ValueError("RPE 1-10 araliginda olmalidir.")

    @property
    def rir(self) -> float:
        return 10 - self.rpe


@dataclass(frozen=True)
class Prescription:
    """Bir egzersiz recetesi: set/tekrar/yogunluk/dinlenme + egzersiz listesi."""
    sets: int
    reps: str
    intensity: str
    rest_sec: int
    exercises: tuple[str, ...] = ()
    volume_multiplier: float = 1.0
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def effective_sets(self) -> float:
        return round(self.sets * self.volume_multiplier, 2)


@dataclass(frozen=True)
class NormalizedActivity:
    """HyperCoach'un ic standart aktivite formati (StandardizedFitnessData)."""
    daily_steps: int
    burned_calories: int
    source: str


@dataclass(frozen=True)
class SupplementInfo:
    name: str
    dose_g: float


@dataclass(frozen=True)
class SupplementRecommendation:
    name: str
    dose: str
    timing: str
