"""Progressive overload kurali (FR-04, rapor 6.2).

RIR = 10 - RPE.
  RIR > 3            -> yuk %2.5-%5 artar (RIR arttikca artis, en fazla %5)
  RPE = 10 (RIR < 1) -> yuk sabit, deload onerilir (hacim %10 dusurulur)
  diger (1 <= RIR <= 3) -> hedef bolge, yuk sabit
"""
from __future__ import annotations

from .config import ConfigurationManager
from .models import SetLog


def next_load_factor(set_log: SetLog) -> float:
    cfg = ConfigurationManager()
    rir = set_log.rir
    if rir > cfg.get("rir_increase_threshold"):
        lo, hi = cfg.get("increase_min_pct"), cfg.get("increase_max_pct")
        # RIR esigin hemen ustundeyse lo, esikten 2 uzaktayken hi (dogrusal)
        pct = min(hi, lo + (rir - cfg.get("rir_increase_threshold") - 1) * (hi - lo) / 1.0)
        return round(1 + pct / 100, 4)
    return 1.0


def needs_deload(set_log: SetLog) -> bool:
    return set_log.rpe >= 10


def next_load_kg(set_log: SetLog) -> float:
    return round(set_log.weight_kg * next_load_factor(set_log), 2)
