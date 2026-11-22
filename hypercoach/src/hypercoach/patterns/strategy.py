"""STRATEGY kalibi (davranissal): hedefe gore set/tekrar hesaplama algoritmasi.

Problem: Hipertrofi, guc ve dayaniklilik hedefleri farkli set/tekrar/yogunluk/dinlenme
hesabi gerektirir. Bunlar bir if-elif zincirinde tutulursa her yeni hedef mevcut kodu
degistirmeyi gerektirir (Open/Closed ihlali). Strateji ile algoritma calisma zamaninda
degistirilir; yeni hedef = yeni sinif.

Roller:
  Strategy         -> TrainingStrategy (ABC)
  ConcreteStrategy -> HypertrophyStrategy, StrengthStrategy, EnduranceStrategy
  Context          -> WorkoutContext
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Goal, Prescription


class TrainingStrategy(ABC):
    @abstractmethod
    def calculate_sets_and_reps(self) -> Prescription:
        """Hedefe ozgu set/tekrar/yogunluk/dinlenme recetesini dondurur."""


class HypertrophyStrategy(TrainingStrategy):
    def calculate_sets_and_reps(self) -> Prescription:
        return Prescription(sets=4, reps="8-12", intensity="%70-80 1RM", rest_sec=90)


class StrengthStrategy(TrainingStrategy):
    def calculate_sets_and_reps(self) -> Prescription:
        return Prescription(sets=5, reps="3-5", intensity="%85-95 1RM", rest_sec=180)


class EnduranceStrategy(TrainingStrategy):
    def calculate_sets_and_reps(self) -> Prescription:
        return Prescription(sets=3, reps="15-20", intensity="%50-65 1RM", rest_sec=45)


class WorkoutContext:
    def __init__(self, strategy: TrainingStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: TrainingStrategy) -> None:
        self._strategy = strategy

    def execute_plan(self) -> Prescription:
        return self._strategy.calculate_sets_and_reps()


_STRATEGY_BY_GOAL: dict[Goal, type[TrainingStrategy]] = {
    Goal.HYPERTROPHY: HypertrophyStrategy,
    Goal.STRENGTH: StrengthStrategy,
    Goal.ENDURANCE: EnduranceStrategy,
}


def strategy_for_goal(goal: Goal) -> TrainingStrategy:
    return _STRATEGY_BY_GOAL[goal]()
