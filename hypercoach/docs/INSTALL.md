# Kurulum Dokümanı

## Gereksinimler
- Python **3.10 veya üzeri** (3.13 ile test edildi)
- git, pip
- Harici çalışma zamanı bağımlılığı yoktur. Geliştirme için `pytest` ve `pytest-cov` gerekir.

## Adımlar

1. **Depoyu klonlayın**
   ```bash
   git clone <REPO_URL> hypercoach
   cd hypercoach
   ```
2. **Sanal ortam oluşturun**
   - Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows (PowerShell): `python -m venv .venv; .venv\Scripts\Activate.ps1`
3. **Paketi geliştirme modunda kurun**
   ```bash
   pip install -e ".[dev]"
   ```
   (Alternatif: `pip install -r requirements.txt` ve `PYTHONPATH=src` ayarı.)
4. **Kurulumu doğrulayın**
   ```bash
   python -m hypercoach.demo
   ```
   Beklenen çıktının ilk satırı: `Plan: Upper/Lower (4 gun)`

## Sık karşılaşılan sorunlar
| Belirti | Çözüm |
|---|---|
| `ModuleNotFoundError: hypercoach` | `pip install -e .` çalıştırın ve sanal ortamın aktif olduğunu kontrol edin |
| `externally-managed-environment` | Sanal ortam kullanın veya `--break-system-packages` ekleyin |
| `python` bulunamadı | `python3` komutunu kullanın |
