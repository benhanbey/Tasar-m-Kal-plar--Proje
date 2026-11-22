"""FACTORY METHOD kalibi (yaratimsal): seviyeye gore antrenman plani uretimi.

Problem: Istemci kod (HyperCoachEngine) hangi plan sinifinin olusturulacagini bilmek
zorunda kalirsa her yeni seviye icin istemci degisir. Factory Method, nesne yaratma
sorumlulugunu Creator alt siniflarina birakir.

Roller:
  Product         -> WorkoutPlan (ABC)
  ConcreteProduct -> BeginnerWorkout, IntermediateWorkout, AdvancedWorkout
  Creator         -> WorkoutPlanCreator (ABC; factory method = create_plan)
  ConcreteCreator -> BeginnerPlanCreator, IntermediatePlanCreator, AdvancedPlanCreator
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Level


class WorkoutPlan(ABC):
    """Product."""

    @property
    @abstractmethod
    def split_name(self) -> str: ...

    @abstractmethod
    def weekly_schedule(self) -> dict[str, tuple[str, ...]]:
        """Gun adi -> egzersiz listesi."""

    def days_per_week(self) -> int:
        return len(self.weekly_schedule())

    def all_exercises(self) -> tuple[str, ...]:
        seen: dict[str, None] = {}
        for exercises in self.weekly_schedule().values():
            for e in exercises:
                seen.setdefault(e)
        return tuple(seen)


class BeginnerWorkout(WorkoutPlan):
    split_name = "Full Body"

    def weekly_schedule(self) -> dict[str, tuple[str, ...]]:
        day = ("Squat", "Bench Press", "Barbell Row", "Overhead Press", "Plank")
        return {"Pazartesi": day, "Carsamba": day, "Cuma": day}


class IntermediateWorkout(WorkoutPlan):
    split_name = "Upper/Lower"

    def weekly_schedule(self) -> dict[str, tuple[str, ...]]:
        upper = ("Bench Press", "Barbell Row", "Overhead Press", "Pull-Up", "Biceps Curl")
        lower = ("Squat", "Romanian Deadlift", "Leg Press", "Calf Raise")
        return {"Pazartesi": upper, "Sali": lower, "Persembe": upper, "Cuma": lower}


class AdvancedWorkout(WorkoutPlan):
    split_name = "Push/Pull/Legs"

    def weekly_schedule(self) -> dict[str, tuple[str, ...]]:
        push = ("Bench Press", "Overhead Press", "Incline Dumbbell Press", "Triceps Pushdown")
        pull = ("Deadlift", "Barbell Row", "Pull-Up", "Biceps Curl")
        legs = ("Squat", "Romanian Deadlift", "Leg Press", "Calf Raise")
        return {
            "Pazartesi": push, "Sali": pull, "Carsamba": legs,
            "Persembe": push, "Cuma": pull, "Cumartesi": legs,
        }


class WorkoutPlanCreator(ABC):
    """Creator: factory method (create_plan) alt siniflarda uygulanir."""

    @abstractmethod
    def create_plan(self) -> WorkoutPlan: ...

    def describe_plan(self) -> str:
        plan = self.create_plan()
        return f"{plan.split_name} - {plan.days_per_week()} gun/hafta"


class BeginnerPlanCreator(WorkoutPlanCreator):
    def create_plan(self) -> WorkoutPlan:
        return BeginnerWorkout()


class IntermediatePlanCreator(WorkoutPlanCreator):
    def create_plan(self) -> WorkoutPlan:
        return IntermediateWorkout()


class AdvancedPlanCreator(WorkoutPlanCreator):
    def create_plan(self) -> WorkoutPlan:
        return AdvancedWorkout()


_CREATOR_BY_LEVEL: dict[Level, type[WorkoutPlanCreator]] = {
    Level.BEGINNER: BeginnerPlanCreator,
    Level.INTERMEDIATE: IntermediatePlanCreator,
    Level.ADVANCED: AdvancedPlanCreator,
}


def creator_for_level(level: Level) -> WorkoutPlanCreator:
    try:
        return _CREATOR_BY_LEVEL[level]()
    except KeyError:
        raise ValueError(f"Gecersiz kullanici seviyesi: {level!r}") from None
