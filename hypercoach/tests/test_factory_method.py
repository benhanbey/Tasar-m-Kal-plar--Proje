import pytest

from hypercoach.models import Level
from hypercoach.patterns.factory_method import (AdvancedPlanCreator, AdvancedWorkout,
                                                BeginnerPlanCreator, BeginnerWorkout,
                                                IntermediateWorkout, WorkoutPlan,
                                                WorkoutPlanCreator, creator_for_level)


def test_creator_and_product_are_abstract():
    with pytest.raises(TypeError):
        WorkoutPlanCreator()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        WorkoutPlan()  # type: ignore[abstract]


@pytest.mark.parametrize("level,product,days", [
    (Level.BEGINNER, BeginnerWorkout, 3),
    (Level.INTERMEDIATE, IntermediateWorkout, 4),
    (Level.ADVANCED, AdvancedWorkout, 6),
])
def test_creator_returns_correct_product(level, product, days):
    plan = creator_for_level(level).create_plan()
    assert isinstance(plan, product)
    assert plan.days_per_week() == days


def test_describe_uses_factory_method():
    assert BeginnerPlanCreator().describe_plan() == "Full Body - 3 gun/hafta"
    assert AdvancedPlanCreator().describe_plan() == "Push/Pull/Legs - 6 gun/hafta"


def test_invalid_level_raises():
    with pytest.raises(ValueError):
        creator_for_level("expert")  # type: ignore[arg-type]


def test_all_exercises_unique():
    ex = BeginnerWorkout().all_exercises()
    assert len(ex) == len(set(ex))
