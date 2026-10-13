# Support Triage Agent

Müşteri destek taleplerini yapay zekâ ile sınıflandıran, basit soruları otomatik yanıtlayan ve riskli talepleri **insan onayına** gönderen bir triyaj sistemi. Akış [LangGraph](https://langchain-ai.github.io/langgraph/) ile, sınıflandırma ve yanıtlar Anthropic Claude ile yapılır.

## Özellikler

- **Müşteri portalı (`/`)**: Müşteri talebini yazar. Basit sorularda yanıtı anında görür; diğerlerinde "talebiniz alındı" mesajı görür.
- **Temsilci paneli (`/panel`)**: Anahtar ile girilir. Onay bekleyen talepler, sonuçlanan talepler ve istatistikler burada.
- **İnsan onayı (human-in-the-loop)**: Riskli talepler graph içinde durur; temsilci onaylar ya da reddeder (yeniden sınıflandırılır).
- **Kalıcılık**: Karar günlüğü, onay kuyruğu ve graph durumu SQLite'ta tutulur; sunucu yeniden başlasa da bekleyen talepler kaybolmaz.

## Mimari

```
frontend/ (React + Vite)      main.py (FastAPI)       graph_core.py (LangGraph)
  /        CustomerPortal  ->  POST /tickets        ->  sınıflandır -> yanıtla
  /panel   AgentPanel      ->  GET  /tickets/pending     \-> awaiting_review (durur)
                               POST /tickets/{id}/review -> devam eder
                               GET  /tickets, /stats
logger.py : karar_gunlugu.db (kararlar, bekleyenler)      checkpoints.db (graph durumu)
```

## API

| Uç nokta | Yetki | Açıklama |
|---|---|---|
| `POST /tickets` | Herkese açık | Yeni talep oluşturur; `tamamlandi` ya da `beklemede` döner |
| `GET /tickets` | Panel anahtarı | Sonuçlanan talepler |
| `GET /tickets/pending` | Panel anahtarı | Onay bekleyen talepler |
| `POST /tickets/{id}/review` | Panel anahtarı | `{"karar": "onay" \| "red"}` |
| `GET /stats` | Panel anahtarı | Sonuç türüne göre dağılım |
| `GET /panel/auth` | Panel anahtarı | Anahtar doğrulama |

Panel uçları `X-Panel-Token` başlığı ister. Swagger: `http://127.0.0.1:8000/docs`.

## Kurulum

Gereksinimler: Python 3.12+, Node.js 20+.

```bash
# Backend
pip install -r requirements.txt
cp .env.example .env        # değerleri doldurun
uvicorn main:app --port 8000

# Frontend (ayrı terminal)
cd frontend
npm install
npm run dev
```

Ardından: müşteri portalı http://localhost:5173/ — temsilci paneli http://localhost:5173/panel

### Ortam değişkenleri

| Değişken | Açıklama |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API anahtarı (zorunlu) |
| `PANEL_TOKEN` | Temsilci paneli giriş anahtarı (zorunlu; boşsa panel uçları 503 döner) |
| `FRONTEND_URL` | CORS için izinli adres(ler), virgülle ayrılır. Varsayılan `http://localhost:5173` |
| `VITE_API_URL` | Frontend'in backend adresi (varsayılan `http://127.0.0.1:8000`) |

## Canlıya alma notları

- Sunucu, bilinmeyen yolları `index.html`'e yönlendirmeli (SPA fallback); aksi halde `/panel` doğrudan açılmaz.
- `PANEL_TOKEN` güçlü ve gizli tutulmalı; HTTPS kullanın. Tek paylaşılan anahtar basit bir korumadır, çok kullanıcılı gerçek kimlik doğrulama değildir.
- `.env`, `karar_gunlugu.db` ve `checkpoints.db` git'e eklenmez.

## Diğer dosyalar

- `agent_graph*.py`, `classify_experiment.py`, `evaluate_accuracy.py`, `prepare_dataset.py`: geliştirme sürecindeki deney ve değerlendirme betikleri.
- `docs/ADR-0003-ai-rol-ayrimi.md`: yapay zekânın rolü hakkındaki mimari karar kaydı.