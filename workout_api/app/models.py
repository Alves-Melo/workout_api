
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False, unique=True, index=True)
    atletas = relationship("Atleta", back_populates="categoria")

class CentroTreinamento(Base):
    __tablename__ = "centros_treinamento"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False, unique=True, index=True)
    atletas = relationship("Atleta", back_populates="centro_treinamento")

class Atleta(Base):
    __tablename__ = "atletas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False, index=True)
    cpf = Column(String(14), nullable=False, unique=True, index=True)  # format 000.000.000-00 or only digits
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    centro_treinamento_id = Column(Integer, ForeignKey("centros_treinamento.id"), nullable=True)

    categoria = relationship("Categoria", back_populates="atletas")
    centro_treinamento = relationship("CentroTreinamento", back_populates="atletas")

    __table_args__ = (UniqueConstraint('cpf', name='uq_atleta_cpf'), )
