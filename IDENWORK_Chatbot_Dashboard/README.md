# IDENWORK · Chatbot + Dashboard (MVP)

IDENWORK marka başlatma belgesinden uyarlanmıştır. Teknik katmanlar SmartLead AI öğrenci yönergesindeki **Separation of Concerns** ilkesine göre ayrılmıştır.

## Özellikler
- `/` — marka kimliğine uygun karşılama sayfası, Türkçe chatbot, isteğe bağlı iletişim formu
- `/api/sohbet` — Groq API destekli sohbet (`mesaj`, `gecmis` → `basari`, `cevap`)
- `POST /api/leads` — onaylı iletişim formu (`isim`, `telefon`, `mesaj`, `onay`)
- `GET /api/leads` — yalnızca oturum açan yöneticiye lead listesi (`basari`, `leads`)
- `/dashboard` — erişim korumalı yönetim paneli
- `/health` — sunucu durum testi

## Kurulum (Python 3.9+)
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
python run.py
```
`.env` içine **SECRET_KEY** (rastgele güçlü değer) ve **ADMIN_PASSWORD** (güçlü benzersiz şifre) yazın. Gerçek yanıtlar için `GROQ_API_KEY` girin; girilmezse örnek demo yanıtı kullanılır. Açılış: http://localhost:5000 ; panel: http://localhost:5000/login.

## Mimari
- `config.py`: ortam değişkenleri, BUSINESS_CONTEXT, geliştirme/üretim ayarları
- `app/database.py`: tüm SQL ve SQLite erişimi, parametreli sorgular
- `app/services/ai_service.py`: tek Groq HTTP çağrısı, demo modu ve AIServiceError
- `app/routes.py`: iki Blueprint, veri doğrulama, oturum kontrolü, JSON API
- `app/__init__.py`: uygulama fabrikası, CORS, veritabanı, rotalar, `/health`
- `app/templates`: ziyaretçi, giriş, yönetim sayfaları; `app/static`: marka teması ve JS
- `wix/`: Wix Velo bağlantı kodu ve yönetim repeater yerleşimi notları

## Test
```bash
pytest -q
```

## GitHub + Render
1. `.env` gizli tutulur, **GitHub'a eklenmez**; `.env.example` örnek dosyadır.
2. Render Web Service: Build `pip install -r requirements.txt` ; Start `gunicorn run:app`.
3. Render Environment: `FLASK_ENV=production`, `SECRET_KEY`, `ADMIN_PASSWORD`, `GROQ_API_KEY`, `DATABASE_URL`, `CORS_ORIGINS=https://www.siteniz.com,https://siteniz.com`.
4. Wix kodlarındaki `API_URL` alanını Render URL'nizle değiştirin. Wix sitesindeki tüm ID'ler örnekle birebir aynı olmalı.

## Yayın öncesi güvenlik / KVKK
Bu, ders sunumuna uygun MVP'dir, üretime doğrudan hazır değildir. Veriler telefon ve mesaj içerdiğinden gerçek ziyaretçilerden veri almadan önce KVKK aydınlatma ve rıza süreçleri, kayıt silme/erişim kanalları, saklama süresi, TLS/HTTPS, rate limiting, anti-spam, CSRF koruması, güvenli oturum politikaları, logging minimizasyonu ve erişim güvenliği tamamlanmalıdır. Render'ın geçici diskinde SQLite kalıcı olmayabilir; canlı kullanımda kalıcı disk veya yönetilen veritabanına geçin. Yönetim panelini Wix üzerinden herkese açık API ile bağlamayın: erişim kontrollü backend proxy gerekir, paket güvenli Flask paneli içerir.

**Önemli sınır:** Bu chatbot kariyer/öz farkındalık konuşma MVP'sidir; marka belgesindeki profil, kişilik tercihleri değerlendirmesi ve kapsamlı kişiselleştirilmiş kariyer planı henüz geliştirilmedi. Terapi, psikolojik tanı veya iş garantisi sunmaz.
