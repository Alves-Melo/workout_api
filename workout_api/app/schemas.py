
from typing import Optional
from pydantic import BaseModel

# ---- Create Schemas ----
class CategoriaCreate(BaseModel):
    nome: str

class CentroTreinamentoCreate(BaseModel):
    nome: str

class AtletaCreate(BaseModel):
    nome: str
    cpf: str
    categoria_id: Optional[int] = None
    centro_treinamento_id: Optional[int] = None

# ---- Response Schemas ----
class AtletaOut(BaseModel):
    nome: str
    centro_treinamento: Optional[str] = None
    categoria: Optional[str] = None

    class Config:
        from_attributes = True
