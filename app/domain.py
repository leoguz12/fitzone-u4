from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from datetime import datetime, timezone

class DomainException(Exception): pass
class InvalidData(DomainException): pass
class InvalidTransition(DomainException): pass
class LimitExceeded(DomainException): pass

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "MXN"

    def __post_init__(self):
        if not self.amount.is_finite() or self.amount < 0:
            raise InvalidData("Monto invalido")

    def add(self, other):
        if self.currency != other.currency:
            raise InvalidData("Monedas distintas")
        return Money(self.amount + other.amount, self.currency)

@dataclass(frozen=True)
class Socio:
    id: str
    is_vip: bool = False
    active: bool = True

@dataclass(frozen=True)
class ItemReserva:
    sku: str
    quantity: int
    unit_price: Money

    def __post_init__(self):
        if not self.sku.strip() or self.quantity <= 0:
            raise InvalidData("Articulo invalido")

    @property
    def subtotal(self):
        return Money(self.unit_price.amount * self.quantity)

class ReservaStatus(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"

@dataclass(frozen=True)
class DomainEvent:
    name: str
    reserva_id: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Reserva:
    socio: Socio
    id: str
    has_promotion: bool = False
    status: ReservaStatus = ReservaStatus.DRAFT
    items: list[ItemReserva] = field(default_factory=list)
    events: list = field(default_factory=list)

    @property
    def units(self):
        return sum(item.quantity for item in self.items)

    @property
    def total(self):
        amount = sum((x.subtotal.amount for x in self.items), Decimal("0"))
        return Money(amount)

    def add_item(self, item):
        if self.status != ReservaStatus.DRAFT:
            raise InvalidTransition("Solo DRAFT admite articulos")
        if self.units + item.quantity > 20:
            raise LimitExceeded("Maximo 20 unidades")
        if item.unit_price.currency != "MXN":
            raise InvalidData("Solo MXN")
        self.items.append(item)

    def confirm(self):
        if self.status != ReservaStatus.DRAFT:
            raise InvalidTransition("Solo DRAFT")
        if not self.items or not self.socio.active:
            raise InvalidData("Requiere articulos y socio activo")
        self.status = ReservaStatus.CONFIRMED
        self.events.append(DomainEvent("ReservaConfirmed", self.id))

    def ship(self, tracking_number: str):
        if self.status != ReservaStatus.CONFIRMED:
            raise InvalidTransition("Requiere CONFIRMED")
        if not tracking_number.strip():
            raise InvalidData("Guia obligatoria")
        self.status = ReservaStatus.SHIPPED
        self.events.append(DomainEvent("ReservaShipped", self.id))

    def cancel(self, reason: str):
        if self.status != ReservaStatus.CONFIRMED:
            raise InvalidTransition("Requiere CONFIRMED para cancelar")
        if not reason.strip():
            raise InvalidData("Motivo obligatorio")
        self.status = ReservaStatus.CANCELLED
        self.events.append(DomainEvent("ReservaCancelled", self.id))

    def deliver(self):
        if self.status != ReservaStatus.SHIPPED:
            raise InvalidTransition("Requiere SHIPPED")
        self.status = ReservaStatus.DELIVERED
        self.events.append(DomainEvent("ReservaDelivered", self.id))

    def return_order(self):
        if self.status != ReservaStatus.SHIPPED:
            raise InvalidTransition("Requiere SHIPPED para devolucion")
        self.status = ReservaStatus.RETURNED
        self.events.append(DomainEvent("ReservaReturned", self.id))