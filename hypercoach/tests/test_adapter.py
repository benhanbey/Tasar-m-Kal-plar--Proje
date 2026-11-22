import pytest

from hypercoach.models import NormalizedActivity
from hypercoach.patterns.adapter import (ActivityAggregator, AppleHealthAdapter,
                                         AppleHealthService, ExternalSupplementAPI,
                                         FitnessDataTarget, StravaAdapter, StravaService,
                                         SupplementAPIAdapter)


def test_target_is_abstract():
    with pytest.raises(TypeError):
        FitnessDataTarget()  # type: ignore[abstract]


def test_apple_adapter_normalizes():
    a = AppleHealthAdapter(AppleHealthService()).get_normalized_activity()
    assert a == NormalizedActivity(10450, 480, "AppleHealth")


def test_strava_adapter_converts_distance_to_steps():
    a = StravaAdapter(StravaService()).get_normalized_activity()
    assert a.source == "Strava"
    assert a.burned_calories == 410
    assert a.daily_steps == round(5200 / 0.762)


def test_supplement_adapter_converts_mg_to_g():
    info = SupplementAPIAdapter(ExternalSupplementAPI()).get_supplement_info()
    assert info.name == "Creatine Monohydrate"
    assert info.dose_g == 5.0


def test_aggregator_works_with_any_target():
    agg = ActivityAggregator([AppleHealthAdapter(AppleHealthService()),
                              StravaAdapter(StravaService())])
    assert len(agg.collect()) == 2
    assert agg.total_burned_calories() == 890
