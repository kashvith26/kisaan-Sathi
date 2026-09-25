from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_forecast():
 r=c.post('/predict/forecast',json={'history':[2700,2720,2750,2760,2790],'horizon':7}); assert r.status_code==200 and len(r.json()['forecast'])==7
def test_all_models():
 assert c.post('/predict/regime',json={'prices':[2700,2720,2750,2760,2790]}).json()['regime']
 assert c.post('/rank/buyers',json={'candidates':[{'id':'b1','crop_match':True,'qty_match':1,'quality_match':1,'trust':90,'pickup':True}]}).json()['ranking'][0]['score']>0
 assert c.post('/decision',json={'local_net':2600,'destination_net':2900,'future_net':2680,'risk':45,'storage_available':True,'quantity':100,'break_even':20}).json()['action']=='TRANSPORT'
 assert c.post('/bandit/select',json={'arms':[{'id':'a','successes':8,'failures':2},{'id':'b','successes':2,'failures':8}]}).status_code==200
