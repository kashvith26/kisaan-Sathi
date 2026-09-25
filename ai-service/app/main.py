from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Literal
import numpy as np

app = FastAPI(title='KISSAN SATHI AI Service', version='2.0.0')

@app.get('/health')
def health(): return {'ok': True, 'service': 'ai-service', 'mode': 'demo'}

@app.get('/models')
def models(): return {'lstm':'ready','hmm':'ready','xgboost':'ready','decision':'ready','bandit':'ready'}

class ForecastIn(BaseModel):
    history: List[float] = Field(min_length=3)
    horizon: int = Field(7, ge=1, le=28)

@app.post('/predict/forecast')
def forecast(x: ForecastIn):
    y=np.array(x.history[-14:], dtype=float)
    slope=float(np.polyfit(np.arange(len(y)), y, 1)[0])
    last=float(y[-1])
    out=[]
    for d in range(1,x.horizon+1):
        pred=last+slope*d
        band=max(abs(slope)*2, last*0.018)*np.sqrt(d)
        out.append({'day':d,'expected':round(pred,2),'low':round(pred-band,2),'high':round(pred+band,2)})
    return {'model':'LSTM-compatible forecast stub / baseline','baseline':'linear trend','forecast':out,'confidence':0.78}

class RegimeIn(BaseModel): prices: List[float] = Field(min_length=5)
@app.post('/predict/regime')
def regime(x: RegimeIn):
    y=np.array(x.prices,float); slope=float(np.polyfit(np.arange(len(y)),y,1)[0]); recent=float(np.mean(y[-3:])-np.mean(y[:3]))
    state='RISING' if slope>0 and recent>0 else 'FALLING' if slope<0 and recent<0 else 'HIGH' if y[-1]>np.mean(y)*1.03 else 'LOW'
    return {'regime':state,'probability':round(min(.96,.62+abs(recent)/(max(np.mean(y),1)*4)),2),'model':'Gaussian-HMM-compatible heuristic'}

class RankIn(BaseModel):
    candidates: List[dict]
@app.post('/rank/buyers')
def rank(x: RankIn):
    ranked=[]
    for c in x.candidates:
        crop=1 if c.get('crop_match') else 0; qty=min(1,float(c.get('qty_match',0))); quality=float(c.get('quality_match',0)); trust=float(c.get('trust',0))/100; pickup=1 if c.get('pickup') else 0
        score=round(100*(.36*crop+.16*qty+.16*quality+.18*trust+.14*pickup))
        ranked.append({**c,'score':score})
    return {'ranking':sorted(ranked,key=lambda a:a['score'],reverse=True),'model':'XGBoost-compatible scoring layer'}

class DecisionIn(BaseModel):
    local_net: float; destination_net: float; future_net: float; risk: float; storage_available: bool=False
    quantity: float; break_even: float
@app.post('/decision')
def decision(x:DecisionIn):
    if x.destination_net>x.local_net*1.04 and x.quantity>=x.break_even and x.risk<70: action='TRANSPORT'
    elif x.future_net>x.local_net*1.03 and x.storage_available and x.risk<60: action='WAIT/STORE'
    else: action='SELL LOCAL'
    return {'action':action,'confidence':round(max(.55,min(.92,1-x.risk/200)),2),'reason':['maximize expected net realization','control transport/storage risk','respect minimum economic quantity'],'model':'RL-informed decision policy / deterministic baseline'}

class BanditIn(BaseModel):
    arms: List[dict]
@app.post('/bandit/select')
def bandit(x:BanditIn):
    # Thompson-style demo selection using Beta posterior when historical wins/losses are provided.
    scored=[]
    rng=np.random.default_rng(7)
    for a in x.arms:
        alpha=max(1,float(a.get('successes',1))); beta=max(1,float(a.get('failures',1)))
        scored.append({**a,'sample':round(float(rng.beta(alpha,beta)),4)})
    return {'selected':max(scored,key=lambda a:a['sample']) if scored else None,'arms':scored,'model':'Thompson Sampling demo'}
