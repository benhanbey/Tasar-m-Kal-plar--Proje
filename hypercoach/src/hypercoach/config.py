"""SINGLETON kalibi: ConfigurationManager.

Problem: Fizyolojik esikler (RIR esigi, deload orani, kreatin dozu, protein/kg ...)
uygulamanin tum modullerinde ayni degerlerle kullanilmalidir. Her modul kendi kopyasini
olusturursa bir modulde yapilan degisiklik digerlerine yansimaz ve tutarsiz oneriler
uretilir. Tek ve global erisilebilir bir ornek bu tutarliligi garanti eder.

Roller: Singleton = ConfigurationManager.
"""
from __future__ import annotations

import threading
from typing import Any, ClassVar, Optional

_DEFAULTS: dict[str, Any] = {
    "rir_increase_threshold": 3,      # RIR > 3 -> yuk artir
    "increase_min_pct": 2.5,
    "increase_max_pct": 5.0,
    "deload_volume_factor": 0.90,     # hacim %10 dusurulur
    "creatine_daily_g": 5.0,
    "protein_g_per_kg": 2.0,
    "caffeine_mg_per_kg_min": 3.0,
    "caffeine_mg_per_kg_max": 6.0,
    "caffeine_lead_minutes": 45,
}


class ConfigurationManager:
    _instance: ClassVar[Optional["ConfigurationManager"]] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls) -> "ConfigurationManager":
        if cls._instance is None:
            with cls._lock:  # cift kontrollu kilitleme: coklu thread guvenligi
                if cls._instance is None:
                    inst = super().__new__(cls)
                    inst._values = dict(_DEFAULTS)
                    cls._instance = inst
        return cls._instance

    def get(self, key: str) -> Any:
        try:
            return self._values[key]
        except KeyError:
            raise KeyError(f"Bilinmeyen konfigurasyon anahtari: {key}") from None

    def set(self, key: str, value: Any) -> None:
        if key not in _DEFAULTS:
            raise KeyError(f"Bilinmeyen konfigurasyon anahtari: {key}")
        self._values[key] = value

    def reset(self) -> None:
        """Varsayilanlara doner (testler icin)."""
        self._values = dict(_DEFAULTS)
