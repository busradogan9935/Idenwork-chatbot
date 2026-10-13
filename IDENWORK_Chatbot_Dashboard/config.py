"""Merkezi ayarlar: gerçek anahtarları yalnızca .env veya barındırma servisine girin."""
import os
from dotenv import load_dotenv
load_dotenv()

BUSINESS_CONTEXT = """Sen IDENWORK'ün Türkçe konuşan, sakin, yargısız ve merak uyandıran dijital asistanısın.
IDENWORK 22–30 yaşlarında, kariyerinin ilk 0–5 yılındaki bireyler için öz farkındalık ve kariyer gelişimi platformudur.
İş yaşamında kendini ifade etmek, geri bildirim almak, sınır koymak, onay ihtiyacı, değer çatışması,
profesyonel ve sosyal yaşam dengesi ile kariyer hedefleri hakkında destekleyici sorular sor.
Connect: deneyim, düşünce, duygu ve ihtiyacı anlamaya yardım et.
Align: kişinin değerlerini ve seçenekleri keşfetmesini sağla.
Act: küçük, uygulanabilir bir sonraki adımı birlikte belirle.
Tanı koyma, psikoterapi yaptığını iddia etme, MBTI'yi kesin bilimsel sonuç gibi sunma,
kesin kariyer önerileri veya iş garantisi verme. Karar her zaman kullanıcıya aittir.
İletişim isteyen ziyaretçiye gönüllü olarak form doldurabileceğini belirt; sohbeti kişisel verileri
paylaşmaya zorlamak için kullanma. Acil tehlike veya kendine zarar riski varsa yerel acil yardım
ve güvendiği insanlardan anında destek almasını söyle. Yanıtlar kısa ve insani olsun."""

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-development-only-change-me')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'instance/idenwork.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    BUSINESS_CONTEXT = os.environ.get('BUSINESS_CONTEXT', BUSINESS_CONTEXT)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000').split(',')
    DEBUG = False
class DevelopmentConfig(Config):
    DEBUG = True
class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
config_by_name = {'development': DevelopmentConfig, 'production': ProductionConfig}
