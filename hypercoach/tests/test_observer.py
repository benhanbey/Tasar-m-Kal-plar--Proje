import pytest

from hypercoach.models import SetLog
from hypercoach.patterns.observer import (OneRepMaxTracker, OverloadAdvisor,
                                          SetLoggedObserver, VolumeLoadTracker,
                                          WorkoutSession)
from hypercoach.physiology import one_rep_max_brzycki


def test_observer_is_abstract():
    with pytest.raises(TypeError):
        SetLoggedObserver()  # type: ignore[abstract]


def test_all_observers_notified_on_log_set():
    s, vol, orm, adv = WorkoutSession(), VolumeLoadTracker(), OneRepMaxTracker(), OverloadAdvisor()
    for o in (vol, orm, adv):
        s.attach(o)
    s.log_set(SetLog("Squat", 100, 5, 9))
    s.log_set(SetLog("Squat", 100, 5, 5))
    assert vol.total == 1000
    assert orm.best["Squat"] == pytest.approx(one_rep_max_brzycki(100, 5))
    assert adv.factors["Squat"] == 1.05  # RIR=5
    assert len(s.sets) == 2


def test_detach_stops_notifications():
    s, vol = WorkoutSession(), VolumeLoadTracker()
    s.attach(vol)
    s.detach(vol)
    s.log_set(SetLog("Squat", 100, 5, 8))
    assert vol.total == 0


def test_attach_is_idempotent():
    s, vol = WorkoutSession(), VolumeLoadTracker()
    s.attach(vol)
    s.attach(vol)
    s.log_set(SetLog("Squat", 100, 1, 8))
    assert vol.total == 100


def test_one_rm_tracker_keeps_best_only():
    s, orm = WorkoutSession(), OneRepMaxTracker()
    s.attach(orm)
    s.log_set(SetLog("Bench", 100, 5, 8))
    best = orm.best["Bench"]
    s.log_set(SetLog("Bench", 60, 5, 8))
    assert orm.best["Bench"] == best
