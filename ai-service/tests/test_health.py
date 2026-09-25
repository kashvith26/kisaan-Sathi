from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['ok'] is True
def test_models():
    r=client.get('/models'); assert r.status_code==200; assert set(r.json())=={'lstm','hmm','xgboost','decision','bandit'}
