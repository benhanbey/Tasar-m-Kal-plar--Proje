"""OBSERVER kalibi (davranissal): canli antrenman takibinde anlik guncelleme.

Problem (FR-05, UI 7.2/3): Kullanici bir set girdigi anda hacim, tahmini 1RM ve
ilerleme grafikleri guncellenmelidir. Oturum sinifi bu hesaplayicilari dogrudan
cagirirsa onlara siki baglanir. Observer ile yeni bir izleyici eklemek oturum kodunu
degistirmez. (Python'da hazir Observer yoktur; kalip bu projede yazilmistir.)

Roller:
  Subject          -> WorkoutSession (attach/detach/notify)
  Observer         -> SetLoggedObserver (ABC)
  ConcreteObserver -> VolumeLoadTracker, OneRepMaxTracker, OverloadAdvisor
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import SetLog
from ..physiology import one_rep_max_brzycki
from ..progression import next_load_factor


class SetLoggedObserver(ABC):
    @abstractmethod
    def update(self, set_log: SetLog) -> None: ...


class WorkoutSession:
    """Subject."""

    def __init__(self) -> None:
        self._observers: list[SetLoggedObserver] = []
        self.sets: list[SetLog] = []

    def attach(self, observer: SetLoggedObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: SetLoggedObserver) -> None:
        self._observers.remove(observer)

    def log_set(self, set_log: SetLog) -> None:
        self.sets.append(set_log)
        for obs in list(self._observers):
            obs.update(set_log)


class VolumeLoadTracker(SetLoggedObserver):
    def __init__(self) -> None:
        self.total = 0.0

    def update(self, set_log: SetLog) -> None:
        self.total += set_log.reps * set_log.weight_kg


class OneRepMaxTracker(SetLoggedObserver):
    def __init__(self) -> None:
        self.best: dict[str, float] = {}

    def update(self, set_log: SetLog) -> None:
        if set_log.reps > 30:
            return
        est = one_rep_max_brzycki(set_log.weight_kg, set_log.reps)
        if est > self.best.get(set_log.exercise, 0.0):
            self.best[set_log.exercise] = est


class OverloadAdvisor(SetLoggedObserver):
    """Her set sonrasi o egzersiz icin bir sonraki hafta yuk katsayisini gunceller."""

    def __init__(self) -> None:
        self.factors: dict[str, float] = {}

    def update(self, set_log: SetLog) -> None:
        self.factors[set_log.exercise] = next_load_factor(set_log)
