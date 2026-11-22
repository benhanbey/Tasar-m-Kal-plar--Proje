import pytest

from hypercoach.config import ConfigurationManager
from hypercoach.models import Goal, Level, Sex, UserProfile


@pytest.fixture(autouse=True)
def _reset_config():
    ConfigurationManager().reset()
    yield
    ConfigurationManager().reset()


@pytest.fixture
def user():
    return UserProfile(age=25, weight_kg=80, height_cm=180, sex=Sex.MALE,
                       level=Level.INTERMEDIATE, goal=Goal.HYPERTROPHY)
