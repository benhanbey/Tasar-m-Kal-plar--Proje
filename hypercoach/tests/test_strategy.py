import pytest

from hypercoach.models import Goal
from hypercoach.patterns.strategy import (EnduranceStrategy, HypertrophyStrategy,
                                          StrengthStrategy, TrainingStrategy,
                                          WorkoutContext, strategy_for_goal)


def test_strategy_is_abstract():
    with pytest.raises(TypeError):
        TrainingStrategy()  # type: ignore[abstract]


def test_context_runs_current_strategy():
    ctx = WorkoutContext(HypertrophyStrategy())
    p = ctx.execute_plan()
    assert (p.sets, p.reps, p.rest_sec) == (4, "8-12", 90)


def test_context_switches_strategy_at_runtime():
    ctx = WorkoutContext(HypertrophyStrategy())
    ctx.set_strategy(StrengthStrategy())
    p = ctx.execute_plan()
    assert (p.sets, p.reps, p.rest_sec) == (5, "3-5", 180)


@pytest.mark.parametrize("goal,cls", [
    (Goal.HYPERTROPHY, HypertrophyStrategy),
    (Goal.STRENGTH, StrengthStrategy),
    (Goal.ENDURANCE, EnduranceStrategy),
])
def test_strategy_for_goal(goal, cls):
    assert isinstance(strategy_for_goal(goal), cls)
