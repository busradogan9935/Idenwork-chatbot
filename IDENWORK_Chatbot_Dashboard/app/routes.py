"""HTTP yönlendirme ve doğrulama; SQL veya yapay zekâ API çağrısı içermez."""
import hmac
from functools import wraps
from flask import Blueprint, request, jsonify, render_template, session, current_app, redirect, url_for
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

pages = Blueprint('pages', __name__)
api = Blueprint('api', __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            if request.path.startswith('/api/'):
                return jsonify(basari=False, hata='Yetkisiz erişim.'), 401
            return redirect(url_for('pages.login'))
        return fn(*args, **kwargs)
    return wrapper

@pages.get('/')
def home():
    return render_template('index.html')

@pages.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password','')
        expected = current_app.config['ADMIN_PASSWORD']
        if expected and hmac.compare_digest(password, expected):
            session.clear()
            session['admin'] = True
            return redirect(url_for('pages.dashboard'))
        error = 'Şifre yanlış veya yönetici şifresi ayarlanmamış.'
    return render_template('login.html', error=error)

@pages.post('/logout')
@admin_required
def logout():
    session.clear()
    return redirect(url_for('pages.login'))

@pages.get('/dashboard')
@admin_required
def dashboard():
    return render_template('dashboard.html')

@api.post('/sohbet')
def sohbet():
    data = request.get_json(silent=True) or {}
    mesaj = data.get('mesaj','')
    gecmis = data.get('gecmis',[])
    if not isinstance(mesaj, str) or not mesaj.strip() or len(mesaj) > 2000:
        return jsonify(basari=False, hata='1–2000 karakterlik mesaj girin.'), 400
    if not isinstance(gecmis, list):
        return jsonify(basari=False, hata='Sohbet geçmişi listesi bekleniyor.'), 400
    try:
        cevap = ai_service.yanit_uret(mesaj.strip(), gecmis)
        return jsonify(basari=True, cevap=cevap)
    except AIServiceError as exc:
        return jsonify(basari=False, hata=str(exc)), 503

@api.post('/leads')
def yeni_lead():
    data = request.get_json(silent=True) or {}
    isim, telefon, mesaj = data.get('isim',''), data.get('telefon',''), data.get('mesaj','')
    consent = data.get('onay') is True
    if not isinstance(isim,str) or not isinstance(telefon,str) or not isinstance(mesaj,str) or not isim.strip() or not telefon.strip():
        return jsonify(basari=False, hata='İsim ve telefon zorunludur.'), 400
    if len(isim)>100 or len(telefon)>32 or len(mesaj)>1000 or not consent:
        return jsonify(basari=False, hata='Alan uzunluklarını ve veri işleme onayını kontrol edin.'), 400
    try:
        new_id=lead_ekle(isim.strip(), telefon.strip(), mesaj.strip())
        return jsonify(basari=True, id=new_id, mesaj='Kaydınız alındı.'), 201
    except Exception:
        current_app.logger.exception('Kayıt hatası')
        return jsonify(basari=False, hata='Kayıt sırasında bir sorun oluştu.'), 500

@api.get('/leads')
@admin_required
def leadler():
    try:
        return jsonify(basari=True, leads=tum_leadler())
    except Exception:
        current_app.logger.exception('Listeleme hatası')
        return jsonify(basari=False, hata='Kayıtlar okunamadı.'), 500
