from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class MetodoPago:
    id: int
    nombre: str


@dataclass
class Pago:
    id: int
    pedido_id: int
    metodo_pago_id: int
    monto: float
    fecha: datetime
    estado: str  # 'aprobado' | 'pendiente' | 'rechazado'
    metodo_pago: Optional[MetodoPago] = None

    @property
    def es_aprobado(self) -> bool:
        return self.estado == "aprobado"


@dataclass
class Pedido:
    id: int
    usuario_id: int
    fecha: datetime
    estado: str   # 'completado' | 'pendiente' | 'cancelado'
    total: float
    pagos: List[Pago] = field(default_factory=list)

    @property
    def esta_completado(self) -> bool:
        return self.estado == "completado"

    @property
    def total_aprobado(self) -> float:
        """Suma solo los pagos aprobados del pedido."""
        return sum(p.monto for p in self.pagos if p.es_aprobado)


@dataclass
class ReporteFinanciero:
    periodo: str          # 'Hoy' | 'Esta Semana' | 'Este Mes' | 'Este Año'
    ingresos: float
    total_pedidos: int
    tendencia: str        # ej: '+12.2%' o 'Diario'
    metodos_pago: List[dict] = field(default_factory=list)
    # metodos_pago: [{ nombre, cant_pedidos, monto, porcentaje }]

    @property
    def ingresos_formateado(self) -> str:
        return f"$ {int(self.ingresos):,}".replace(",", ".")