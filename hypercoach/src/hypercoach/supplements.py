"""Besin takviyesi oneri motoru (FR-03, rapor 6.3)."""
from __future__ import annotations

from .config import ConfigurationManager
from .models import SupplementRecommendation, UserProfile


def recommend_supplements(
    user: UserProfile, dietary_protein_g: float, training_time: str = "18:00"
) -> list[SupplementRecommendation]:
    cfg = ConfigurationManager()
    recs: list[SupplementRecommendation] = []

    recs.append(SupplementRecommendation(
        "Kreatin Monohidrat", f"{cfg.get('creatine_daily_g'):g} g/gun", "Gunun herhangi bir saati"))

    target = cfg.get("protein_g_per_kg") * user.weight_kg
    gap = target - dietary_protein_g
    if gap > 0:
        recs.append(SupplementRecommendation(
            "Whey Protein", f"{gap:.0f} g/gun (acik)", "Antrenman sonrasi"))

    lo = cfg.get("caffeine_mg_per_kg_min") * user.weight_kg
    hi = cfg.get("caffeine_mg_per_kg_max") * user.weight_kg
    recs.append(SupplementRecommendation(
        "Kafein", f"{lo:.0f}-{hi:.0f} mg",
        f"Antrenmandan {cfg.get('caffeine_lead_minutes')} dk once ({training_time})"))
    return recs
