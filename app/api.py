from fastapi import FastAPI, HTTPException
from cargar_csv import load_fixture
from app.domain import InvalidTransition, InvalidData

app = FastAPI(title="FitZone API - Actividad 4")

# Cargamos los datos en memoria al iniciar la API
reservas_db = load_fixture()

@app.get("/reservas/{reserva_id}")
def get_reserva(reserva_id: str):
    reserva = reservas_db.get(reserva_id)
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {
        "id": reserva.id, 
        "status": reserva.status.value,
        "units": reserva.units,
        "total": str(reserva.total.amount)
    }

@app.post("/reservas/{reserva_id}/confirm")
def confirm_reserva(reserva_id: str):
    reserva = reservas_db.get(reserva_id)
    if reserva is None:
        raise HTTPException(status_code=404, detail="No existe")
    
    try:
        reserva.confirm()
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
        
    return {"id": reserva.id, "status": reserva.status.value}

@app.post("/reservas/{reserva_id}/ship")
def ship_reserva(reserva_id: str, tracking_number: str):
    reserva = reservas_db.get(reserva_id)
    if reserva is None:
        raise HTTPException(status_code=404, detail="No existe")
    
    try:
        reserva.ship(tracking_number)
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
        
    return {"id": reserva.id, "status": reserva.status.value}

@app.post("/reservas/{reserva_id}/cancel")
def cancel_reserva(reserva_id: str, reason: str):
    reserva = reservas_db.get(reserva_id)
    if reserva is None:
        raise HTTPException(status_code=404, detail="No existe")
    
    try:
        reserva.cancel(reason)
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
        
    return {"id": reserva.id, "status": reserva.status.value}