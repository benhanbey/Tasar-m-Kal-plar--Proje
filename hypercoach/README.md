# HyperCoach

Yapay zeka destekli, kişiselleştirilmiş antrenman ve takviye asistanı.
Nişantaşı Üniversitesi – Bilgisayar Mühendisliği, Yazılım Tasarım Kalıpları dersi dönem projesi.

**Öğrenci:** Yusuf Akça (20232013086) · **Dil:** Python 3.10+ · **Bağımlılık:** yalnızca standart kütüphane (test için pytest)

## Hızlı başlangıç

```bash
git clone <REPO_URL> hypercoach && cd hypercoach
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m hypercoach.demo      # çalışan örnek
pytest --cov=hypercoach        # testler + kapsama
```

Ayrıntı: [docs/INSTALL.md](docs/INSTALL.md) · [docs/TESTING.md](docs/TESTING.md) · [docs/PATTERNS.md](docs/PATTERNS.md)

## Kullanılan GoF kalıpları (6)

| Grup | Kalıp | Dosya | Çözdüğü problem |
|---|---|---|---|
| Yaratımsal | **Factory Method** | `patterns/factory_method.py` | Seviyeye göre plan nesnesi üretimi; istemci somut sınıfı bilmez |
| Yaratımsal | **Singleton** | `config.py` | Fizyolojik eşiklerin tüm modüllerde tek, tutarlı kaynaktan okunması |
| Yapısal | **Adapter** | `patterns/adapter.py` | Apple Health / Strava / takviye API'lerinin ortak iç formata uyarlanması |
| Yapısal | **Decorator** | `patterns/decorator.py` | Reçeteye deload ve sakatlık kısıtlarının birleştirilebilir şekilde eklenmesi |
| Davranışsal | **Strategy** | `patterns/strategy.py` | Hedefe göre (hipertrofi/güç/dayanıklılık) set-tekrar algoritması seçimi |
| Davranışsal | **Observer** | `patterns/observer.py` | Set girildiği anda hacim, 1RM ve yük önerisinin canlı güncellenmesi |

Her kalıbın katılımcı rolleri ayrı, anlamlı adlı sınıflarla ve `abc.ABC` arayüzleriyle uygulanmıştır;
rol–sınıf eşlemesi [docs/PATTERNS.md](docs/PATTERNS.md) dosyasındadır. Dile gömülü kalıp karşılığı
(lambda, hazır Observer vb.) **kullanılmamıştır**; sayılan tüm kalıplar bu projede yazılmıştır.

## Proje yapısı

```
src/hypercoach/
  models.py  physiology.py  progression.py  supplements.py  engine.py  demo.py
  config.py                    # Singleton
  patterns/
    strategy.py  factory_method.py  adapter.py  observer.py  decorator.py
tests/                         # 52 test, her kalıp için ayrı dosya
docs/                          # kurulum, test, kalıp dokümanları
```
