from pydantic import BaseModel
class HealthResponse(BaseModel): service:str; ok:bool; mode:str
