import pytest
from app import create_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY','')
    app=create_app('development')
    app.config.update(TESTING=True,DATABASE_URL=str(tmp_path/'test.db'),ADMIN_PASSWORD='test-password',SECRET_KEY='test-key')
    # Config is updated after app factory, so initialize test database explicitly.
    from app.database import init_db
    init_db(app)
    with app.test_client() as c:
        yield c

def test_health(client):
    assert client.get('/health').json['durum']=='aktif'

def test_demo_chat(client):
    resp=client.post('/api/sohbet',json={'mesaj':'İş yerinde sınır koyamıyorum','gecmis':[]})
    assert resp.status_code==200 and resp.json['basari']

def test_leads_protected(client):
    assert client.get('/api/leads').status_code==401
    assert client.post('/api/leads',json={'isim':'Ece','telefon':'123','onay':False}).status_code==400
    assert client.post('/api/leads',json={'isim':'Ece','telefon':'123','onay':True}).status_code==201
    assert client.post('/login',data={'password':'test-password'}).status_code==302
    assert len(client.get('/api/leads').json['leads'])==1
