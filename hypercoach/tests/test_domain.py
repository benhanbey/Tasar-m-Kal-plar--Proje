import pytest

from hypercoach.engine import HyperCoachEngine
from hypercoach.models import Goal, Level, SetLog, Sex, UserProfile
from hypercoach.physiology import (bmr_mifflin_st_jeor, one_rep_max_brzycki, tdee,
                                   volume_load)
from hypercoach.progression import needs_deload, next_load_factor, next_load_kg
from hypercoach.supplements import recommend_supplements


def test_bmr_male_and_female():
    assert bmr_mifflin_st_jeor(80, 180, 25, Sex.MALE) == 1805.0
    assert bmr_mifflin_st_jeor(60, 165, 30, Sex.FEMALE) == pytest.approx(1320.25)


def test_tdee_and_validation():
    assert tdee(2000, 1.5) == 3000
    with pytest.raises(ValueError):
        tdee(2000, 0)


def test_brzycki():
    assert one_rep_max_brzycki(100, 1) == pytest.approx(100)
    assert one_rep_max_brzycki(100, 10) == pytest.approx(133.37, abs=0.01)
    with pytest.raises(ValueError):
        one_rep_max_brzycki(100, 40)


def test_volume_load():
    assert volume_load([SetLog("a", 50, 10, 7), SetLog("a", 60, 8, 8)]) == 980


@pytest.mark.parametrize("rpe,factor", [
    (9, 1.0),     # RIR=1 -> hedef bolge, sabit
    (7, 1.0),     # RIR=3 -> sabit
    (6, 1.025),   # RIR=4 -> %2.5
    (5, 1.05),    # RIR=5 -> %5
    (3, 1.05),    # RIR=7 -> ust sinir %5
    (10, 1.0),    # RIR=0 -> sabit
])
def test_overload_factor(rpe, factor):
    assert next_load_factor(SetLog("x", 100, 5, rpe)) == factor


def test_deload_and_next_load():
    assert needs_deload(SetLog("x", 100, 5, 10))
    assert not needs_deload(SetLog("x", 100, 5, 9))
    assert next_load_kg(SetLog("x", 100, 5, 5)) == 105.0


def test_setlog_validation():
    with pytest.raises(ValueError):
        SetLog("x", 100, 0, 5)
    with pytest.raises(ValueError):
        SetLog("x", 100, 5, 11)


def test_profile_validation():
    with pytest.raises(ValueError):
        UserProfile(0, 80, 180, Sex.MALE, Level.BEGINNER, Goal.STRENGTH)


def test_supplements(user):
    recs = {r.name: r for r in recommend_supplements(user, dietary_protein_g=110)}
    assert recs["Kreatin Monohidrat"].dose == "5 g/gun"
    assert recs["Whey Protein"].dose.startswith("50 g")      # 2.0*80 - 110
    assert recs["Kafein"].dose == "240-480 mg"                # 3-6 mg/kg
    assert "45 dk" in recs["Kafein"].timing


def test_no_whey_when_protein_target_met(user):
    names = [r.name for r in recommend_supplements(user, dietary_protein_g=170)]
    assert "Whey Protein" not in names


def test_engine_combines_patterns(user):
    injured = UserProfile(25, 80, 180, Sex.MALE, Level.ADVANCED, Goal.STRENGTH, injuries=("lower_back",))
    prog = HyperCoachEngine().generate_program(injured, deload=True)
    assert prog.plan.split_name == "Push/Pull/Legs"                 # Factory Method
    assert (prog.prescription.sets, prog.prescription.reps) == (5, "3-5")  # Strategy
    assert "Deadlift" not in prog.prescription.exercises            # Decorator
    assert prog.prescription.volume_multiplier == pytest.approx(0.9)
    assert prog.tdee == pytest.approx(prog.bmr * 1.55)


def test_demo_runs(capsys):
    from hypercoach import demo
    demo.main()
    out = capsys.readouterr().out
    assert "Plan: Upper/Lower" in out and "Takviye:" in out


def test_demo_entrypoint_and_observer_edge(capsys):
    from hypercoach.patterns.observer import OneRepMaxTracker, WorkoutSession
    s, o = WorkoutSession(), OneRepMaxTracker()
    s.attach(o)
    s.log_set(SetLog("Run", 10, 40, 5))  # 30'dan fazla tekrar 1RM'e katilmaz
    assert o.best == {}
