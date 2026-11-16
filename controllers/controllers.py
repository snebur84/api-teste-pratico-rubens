from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Optional, Annotated
from client_api import criar_sessao, obter_coordenadas, obter_dados_climaticos
from models.schemas import CityCollect, FiltroTempoQuery, ParametroClimatico
from models.models import Cidade, PrevisaoHoraria
from database import get_db
from sqlalchemy.dialects.postgresql import insert

router = APIRouter(tags=["Rotas clima/tempo"])

@router.post("/tempo")
def atualizar_dados(data: CityCollect, db: Session = Depends(get_db)):
    """Atualiza os dados climáticos para a cidade desejada no banco de dados."""
    http_sessao = criar_sessao()
    try:
        localizacao = obter_coordenadas(data.city, http_sessao)
        if not localizacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Não foi possível encontrar a cidade '{data.city}'.",
            )

        dados_climaticos = obter_dados_climaticos(
            lat=localizacao["latitude"],
            lon=localizacao["longitude"],
            timezone=localizacao["timezone"],
            days=data.days,
            sessao=http_sessao,
        )
    finally:
        http_sessao.close()

    cidade_db = db.query(Cidade).filter(Cidade.nome == data.city).first()
    if not cidade_db:
        cidade_db = Cidade(
            nome=data.city,
            latitude=dados_climaticos["latitude"],
            longitude=dados_climaticos["longitude"],
            elevation=dados_climaticos.get("elevation"),
            timezone=dados_climaticos["timezone"],
            timezone_abbreviation=dados_climaticos.get("timezone_abbreviation"),
            utc_offset_seconds=dados_climaticos.get("utc_offset_seconds"),
        )
        db.add(cidade_db)
        db.flush()

    h = dados_climaticos["hourly"]
    registros = [
        {
            "cidade_id": cidade_db.id,
            "data_hora": datetime.fromisoformat(t),
            "temperature_2m": temp,
            "relative_humidity_2m": hum,
            "surface_pressure": press,
            "wind_speed_10m": ws,
            "wind_direction_10m": wd,
            "precipitation": prec,
        }
        for t, temp, hum, press, ws, wd, prec in zip(
            h["time"],
            h["temperature_2m"],
            h["relative_humidity_2m"],
            h["surface_pressure"],
            h["wind_speed_10m"],
            h["wind_direction_10m"],
            h["precipitation"],
        )
    ]

    stmt = insert(PrevisaoHoraria).values(registros)
    stmt = stmt.on_conflict_do_update(
        index_elements=["cidade_id", "data_hora"],
        set_={
            "temperature_2m": stmt.excluded.temperature_2m,
            "relative_humidity_2m": stmt.excluded.relative_humidity_2m,
            "surface_pressure": stmt.excluded.surface_pressure,
            "wind_speed_10m": stmt.excluded.wind_speed_10m,
            "wind_direction_10m": stmt.excluded.wind_direction_10m,
            "precipitation": stmt.excluded.precipitation,
        },
    )

    db.execute(stmt)
    db.commit()

    return {
        "mensagem": "Dados climáticos atualizados com sucesso.",
        "cidade": cidade_db.nome,
        "registros_processados": len(registros),
    }

@router.get("/tempo")
def consultar_tempo(
    filtros: Annotated[FiltroTempoQuery, Query()],
    db: Session = Depends(get_db),):
    """ Esta rota permite consultar os dados climáticos de uma cidade específica,
    incluindo temperatura, umidade, pressão, velocidade e direção do vento, e precipitação.
    - **cidade**: Nome da cidade para consulta (padrão: "Belo Horizonte").
    - **dias**: Número de dias para consulta (padrão: 7).
    - **parametros**: Parâmetros climáticos específicos a serem retornados (opcional).
    """
    cidade_db = db.query(Cidade).filter(Cidade.nome.ilike(filtros.cidade.strip())).first()
    if not cidade_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi possível encontrar a cidade '{cidade}' no banco de dados.",
        )
    registros = db.query(PrevisaoHoraria).filter(
        PrevisaoHoraria.cidade_id == cidade_db.id,
        PrevisaoHoraria.data_hora >= datetime.now() - timedelta(days=filtros.dias),
    ).order_by(PrevisaoHoraria.data_hora.asc())
    if not registros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não há dados climáticos disponíveis para '{cidade}' nos últimos {dias} dias.",
        )
    campos_escolhidos = (
        [p.value for p in filtros.parametros] if filtros.parametros else [p.value for p in ParametroClimatico]
    )
    dados_serializados = jsonable_encoder(registros.all())
    return {
        "cidade": cidade_db.nome,
        "latitude": cidade_db.latitude,
        "longitude": cidade_db.longitude,
        "timezone": cidade_db.timezone,
        "dados_climaticos": [
            {campo: registro[campo] for campo in campos_escolhidos + ["data_hora"]}
            for registro in dados_serializados
        ],
    }

