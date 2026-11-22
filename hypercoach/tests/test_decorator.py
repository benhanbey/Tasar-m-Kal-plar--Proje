import pytest

from hypercoach.config import ConfigurationManager
from hypercoach.models import Prescription
from hypercoach.patterns.decorator import (BasePrescription, DeloadDecorator,
                                           InjuryRestrictionDecorator,
                                           PrescriptionComponent, PrescriptionDecorator)

BASE = Prescription(4, "8-12", "%70-80 1RM", 90, ("Squat", "Bench Press", "Deadlift", "Pull-Up"))


def test_components_are_abstract():
    with pytest.raises(TypeError):
        PrescriptionComponent()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        PrescriptionDecorator(BasePrescription(BASE))  # type: ignore[abstract]


def test_deload_reduces_volume_10_percent():
    p = DeloadDecorator(BasePrescription(BASE)).get_prescription()
    assert p.volume_multiplier == pytest.approx(0.9)
    assert p.effective_sets == pytest.approx(3.6)


def test_deload_reads_singleton_config():
    ConfigurationManager().set("deload_volume_factor", 0.8)
    p = DeloadDecorator(BasePrescription(BASE)).get_prescription()
    assert p.volume_multiplier == pytest.approx(0.8)


def test_injury_removes_risky_exercises():
    p = InjuryRestrictionDecorator(BasePrescription(BASE), ("lower_back",)).get_prescription()
    assert "Deadlift" not in p.exercises and "Squat" not in p.exercises
    assert "Pull-Up" in p.exercises
    assert any("cikarildi" in n for n in p.notes)


def test_unknown_injury_changes_nothing():
    p = InjuryRestrictionDecorator(BasePrescription(BASE), ("elbow",)).get_prescription()
    assert p.exercises == BASE.exercises


def test_decorators_compose_in_any_order():
    a = DeloadDecorator(InjuryRestrictionDecorator(BasePrescription(BASE), ("knee",))).get_prescription()
    b = InjuryRestrictionDecorator(DeloadDecorator(BasePrescription(BASE)), ("knee",)).get_prescription()
    assert a.exercises == b.exercises and a.volume_multiplier == b.volume_multiplier
    assert len(a.notes) == 2
