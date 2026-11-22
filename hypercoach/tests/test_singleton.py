import threading

import pytest

from hypercoach.config import ConfigurationManager


def test_same_instance():
    assert ConfigurationManager() is ConfigurationManager()


def test_state_shared_across_references():
    ConfigurationManager().set("creatine_daily_g", 3.0)
    assert ConfigurationManager().get("creatine_daily_g") == 3.0


def test_thread_safe_single_instance():
    ConfigurationManager._instance = None
    found = []
    ts = [threading.Thread(target=lambda: found.append(ConfigurationManager())) for _ in range(30)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert len({id(i) for i in found}) == 1


def test_unknown_key_rejected():
    with pytest.raises(KeyError):
        ConfigurationManager().get("nope")
    with pytest.raises(KeyError):
        ConfigurationManager().set("nope", 1)


def test_reset_restores_defaults():
    ConfigurationManager().set("protein_g_per_kg", 9)
    ConfigurationManager().reset()
    assert ConfigurationManager().get("protein_g_per_kg") == 2.0
