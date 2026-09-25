from fastapi import APIRouter
from app.config import MODEL_MODE
router=APIRouter()
@router.get('/health',response_model=dict)
def health(): return {'service':'ai-service','ok':True,'mode':MODEL_MODE}
@router.get('/models',response_model=dict)
def models(): return {'lstm':'stub','hmm':'stub','xgboost':'stub','decision':'stub','bandit':'stub'}
