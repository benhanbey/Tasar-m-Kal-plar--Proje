# Test Dokümanı

## Çalıştırma
```bash
pytest                                  # tüm testler
pytest tests/test_strategy.py           # tek kalıp
pytest --cov=hypercoach --cov-report=term-missing   # kapsama raporu
```

## Test planı
| Dosya | Kapsam | Doğrulanan davranış |
|---|---|---|
| `test_strategy.py` | Strategy | Arayüz soyut; Context çalışma zamanında strateji değiştirir; hedef→strateji eşlemesi |
| `test_factory_method.py` | Factory Method | Her seviye doğru Product'ı üretir; Creator soyut; geçersiz seviye `ValueError` |
| `test_adapter.py` | Adapter | Apple/Strava/takviye çıktıları ortak formata dönüşür (mg→g, mesafe→adım); Target soyut |
| `test_observer.py` | Observer | Tüm gözlemciler bilgilendirilir; detach/tekrar attach; en iyi 1RM korunur |
| `test_decorator.py` | Decorator | Deload %10; sakatlık kısıtı; dekoratörler sırayla birleşir; Singleton konfigürasyonunu okur |
| `test_singleton.py` | Singleton | Tek örnek, 30 thread altında tek örnek, bilinmeyen anahtar reddi, `reset` |
| `test_domain.py` | Alan mantığı | BMR/TDEE, Brzycki 1RM, hacim yükü, RPE/RIR kuralı, takviye motoru, motor entegrasyonu, demo |

## Sonuçlar (Python 3.13, pytest 9.1)
- **52 test geçti, 0 başarısız.**
- **Satır kapsama: %99** (379 ifade, 2 kaçan: `demo.py` `__main__` koruması, `EnduranceStrategy` gövdesi).

## RPE/RIR kural tablosu (testle doğrulanır)
| RPE | RIR | Yük çarpanı |
|---|---|---|
| 10 | 0 | 1.000 (sabit; deload önerilir) |
| 9 | 1 | 1.000 |
| 7 | 3 | 1.000 |
| 6 | 4 | 1.025 (+%2.5) |
| ≤5 | ≥5 | 1.050 (+%5, üst sınır) |
