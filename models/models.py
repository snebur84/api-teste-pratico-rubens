from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from database import Base


class Cidade(Base):
    __tablename__ = "cidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation = Column(Float, nullable=True)
    timezone = Column(String(50), nullable=False)
    timezone_abbreviation = Column(String(10), nullable=True)
    utc_offset_seconds = Column(Integer, nullable=True)
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    previsoes = relationship(
        "PrevisaoHoraria", back_populates="cidade", cascade="all, delete-orphan"
    )


class PrevisaoHoraria(Base):
    __tablename__ = "previsoes_horarias"

    id = Column(Integer, primary_key=True, index=True)
    cidade_id = Column(Integer, ForeignKey("cidades.id"), nullable=False, index=True)
    data_hora = Column(DateTime, nullable=False, index=True)
    temperature_2m = Column(Float, nullable=True)
    relative_humidity_2m = Column(Integer, nullable=True)
    surface_pressure = Column(Float, nullable=True)
    wind_speed_10m = Column(Float, nullable=True) 
    wind_direction_10m = Column(Integer, nullable=True)
    precipitation = Column(Float, nullable=True)
    cidade = relationship("Cidade", back_populates="previsoes")

    __table_args__ = (
        UniqueConstraint("cidade_id", "data_hora", name="uq_cidade_data_hora"),
    )
