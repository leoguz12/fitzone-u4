import pytest
from decimal import Decimal
from app.domain import Money, InvalidData, InvalidTransition, LimitExceeded
from cargar_csv import load_fixture

def test_money_negativo():
    with pytest.raises(InvalidData):
        Money(Decimal("-1"))

def test_reserva_o001_inicia_draft():
    reservas = load_fixture()
    assert reservas["O001"].status.value == "DRAFT"
    assert reservas["O001"].units == 4
    assert reservas["O001"].total.amount == Decimal("2100.00")

def test_confirmacion_doble_falla():
    reservas = load_fixture()
    reserva = reservas["O013"]
    reserva.confirm()  # Primera confirmación exitosa
    
    with pytest.raises(InvalidTransition):
        reserva.confirm()  # Segunda confirmación debe fallar

def test_envio_sin_guia_falla():
    reservas = load_fixture()
    reserva = reservas["O013"]
    reserva.confirm()
    
    with pytest.raises(InvalidData):
        reserva.ship("   ")  # Guía vacía debe fallar

def test_cancelacion_desde_shipped_falla():
    reservas = load_fixture()
    reserva = reservas["O013"]
    reserva.confirm()
    reserva.ship("TRK123")
    
    with pytest.raises(InvalidTransition):
        reserva.cancel("Motivo de prueba") # Cancelar después de enviado debe fallar