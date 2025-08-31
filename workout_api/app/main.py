
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from .database import Base, engine, get_db
from . import models, schemas

# Create tables on startup (for demo; for prod use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout API – FastAPI + Docker",
              description="API de exemplo com filtros, respostas personalizadas, exceções e paginação (limit/offset).")

# ----------------------- Categoria -----------------------
@app.post("/categorias", response_model=dict, status_code=201)
def create_categoria(payload: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    categoria = models.Categoria(nome=payload.nome)
    try:
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe uma categoria cadastrada com o nome: {payload.nome}")
    return {"id": categoria.id, "nome": categoria.nome}

# ----------------------- Centro de Treinamento -----------------------
@app.post("/centros-treinamento", response_model=dict, status_code=201)
def create_centro(payload: schemas.CentroTreinamentoCreate, db: Session = Depends(get_db)):
    centro = models.CentroTreinamento(nome=payload.nome)
    try:
        db.add(centro)
        db.commit()
        db.refresh(centro)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe um centro de treinamento cadastrado com o nome: {payload.nome}")
    return {"id": centro.id, "nome": centro.nome}

# ----------------------- Atleta -----------------------
@app.post("/atletas", response_model=dict, status_code=201)
def create_atleta(payload: schemas.AtletaCreate, db: Session = Depends(get_db)):
    atleta = models.Atleta(
        nome=payload.nome,
        cpf=payload.cpf,
        categoria_id=payload.categoria_id,
        centro_treinamento_id=payload.centro_treinamento_id,
    )
    try:
        db.add(atleta)
        db.commit()
        db.refresh(atleta)
    except IntegrityError:
        db.rollback()
        # Exceção de integridade: CPF duplicado
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {payload.cpf}")
    return {"id": atleta.id, "nome": atleta.nome, "cpf": atleta.cpf}

# GET all atletas com filtros (nome, cpf) e resposta customizada
@app.get("/atletas", response_model=LimitOffsetPage[schemas.AtletaOut])
def list_atletas(
    nome: Optional[str] = Query(None, description="Filtra por nome (contains)"),
    cpf: Optional[str] = Query(None, description="Filtra por CPF (igual)"),
    db: Session = Depends(get_db),
):
    # Monta query base
    stmt = select(models.Atleta).order_by(models.Atleta.id)
    if nome:
        stmt = stmt.where(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        stmt = stmt.where(models.Atleta.cpf == cpf)
    atletas = db.execute(stmt).scalars().all()

    # Resposta customizada: somente nome, centro_treinamento e categoria
    items = [
        schemas.AtletaOut(
            nome=a.nome,
            centro_treinamento=a.centro_treinamento.nome if a.centro_treinamento else None,
            categoria=a.categoria.nome if a.categoria else None
        )
        for a in atletas
    ]
    return paginate(items)  # suporta ?limit=&offset= via LimitOffsetPage

# GET por id (detalhado)
@app.get("/atletas/{atleta_id}", response_model=dict)
def get_atleta(atleta_id: int, db: Session = Depends(get_db)):
    atleta = db.get(models.Atleta, atleta_id)
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    return {
        "id": atleta.id,
        "nome": atleta.nome,
        "cpf": atleta.cpf,
        "categoria": atleta.categoria.nome if atleta.categoria else None,
        "centro_treinamento": atleta.centro_treinamento.nome if atleta.centro_treinamento else None,
    }

# Healthcheck simples
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

add_pagination(app)
