from config.conexion import conectar


def _ejecutar_query(query, params=None):
    conn = conectar()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR BD] {e}")
        return None
    finally:
        conn.close()


# ─── INGRESOS ────────────────────────────────────────────────────────────────

def _get_ingresos(filtro_fecha_sql: str) -> float:
    rows = _ejecutar_query(f"""
        SELECT COALESCE(SUM(pa.monto), 0)
        FROM pagos pa
        JOIN pedidos pe ON pa.pedido_id = pe.id
        WHERE pa.estado = 'aprobado'
          AND {filtro_fecha_sql}
    """)
    return float(rows[0][0]) if rows else 0.0


def get_ingresos_hoy():
    return _get_ingresos("DATE(pa.fecha) = CURRENT_DATE")

def get_ingresos_semana():
    return _get_ingresos("DATE(pa.fecha) >= DATE_TRUNC('week', CURRENT_DATE)")

def get_ingresos_mes():
    return _get_ingresos("DATE(pa.fecha) >= DATE_TRUNC('month', CURRENT_DATE)")

def get_ingresos_anio():
    return _get_ingresos("DATE(pa.fecha) >= DATE_TRUNC('year', CURRENT_DATE)")


# ─── PEDIDOS ─────────────────────────────────────────────────────────────────

def _get_pedidos(filtro_fecha_sql: str) -> int:
    rows = _ejecutar_query(f"""
        SELECT COUNT(DISTINCT pe.id)
        FROM pedidos pe
        JOIN pagos pa ON pa.pedido_id = pe.id
        WHERE pa.estado = 'aprobado'
          AND {filtro_fecha_sql}
    """)
    return int(rows[0][0]) if rows else 0


def get_pedidos_hoy():
    return _get_pedidos("DATE(pa.fecha) = CURRENT_DATE")

def get_pedidos_semana():
    return _get_pedidos("DATE(pa.fecha) >= DATE_TRUNC('week', CURRENT_DATE)")

def get_pedidos_mes():
    return _get_pedidos("DATE(pa.fecha) >= DATE_TRUNC('month', CURRENT_DATE)")

def get_pedidos_anio():
    return _get_pedidos("DATE(pa.fecha) >= DATE_TRUNC('year', CURRENT_DATE)")


# ─── MÉTODOS DE PAGO ─────────────────────────────────────────────────────────

def _get_metodos_pago(filtro_fecha_sql: str):
    """Retorna lista de (nombre, cant_pedidos, monto_total, porcentaje)"""
    rows = _ejecutar_query(f"""
        SELECT
            mp.nombre,
            COUNT(pa.id)               AS cant_pedidos,
            COALESCE(SUM(pa.monto), 0) AS monto_total
        FROM pagos pa
        JOIN pedidos pe   ON pa.pedido_id      = pe.id
        JOIN metodos_pago mp ON pa.metodo_pago_id = mp.id
        WHERE pa.estado = 'aprobado'
          AND {filtro_fecha_sql}
        GROUP BY mp.nombre
        ORDER BY monto_total DESC
    """)
    if not rows:
        return []
    total = sum(float(r[2]) for r in rows)
    return [
        (r[0], int(r[1]), float(r[2]), round(float(r[2]) / total * 100) if total > 0 else 0)
        for r in rows
    ]


def get_metodos_hoy():
    return _get_metodos_pago("DATE(pa.fecha) = CURRENT_DATE")

def get_metodos_semana():
    return _get_metodos_pago("DATE(pa.fecha) >= DATE_TRUNC('week', CURRENT_DATE)")

def get_metodos_mes():
    return _get_metodos_pago("DATE(pa.fecha) >= DATE_TRUNC('month', CURRENT_DATE)")

def get_metodos_anio():
    return _get_metodos_pago("DATE(pa.fecha) >= DATE_TRUNC('year', CURRENT_DATE)")


# ─── TENDENCIA ───────────────────────────────────────────────────────────────

def _calcular_tendencia(actual: float, filtro_anterior: str) -> str:
    rows = _ejecutar_query(f"""
        SELECT COALESCE(SUM(pa.monto), 0)
        FROM pagos pa
        JOIN pedidos pe ON pa.pedido_id = pe.id
        WHERE pa.estado = 'aprobado'
          AND {filtro_anterior}
    """)
    anterior = float(rows[0][0]) if rows else 0.0
    if anterior == 0:
        return "+0.0%"
    cambio = ((actual - anterior) / anterior) * 100
    return f"+{cambio:.1f}%" if cambio >= 0 else f"{cambio:.1f}%"


def get_tendencia_semana():
    return _calcular_tendencia(
        get_ingresos_semana(),
        "DATE(pa.fecha) >= DATE_TRUNC('week', CURRENT_DATE) - INTERVAL '7 days' "
        "AND DATE(pa.fecha) < DATE_TRUNC('week', CURRENT_DATE)"
    )

def get_tendencia_mes():
    return _calcular_tendencia(
        get_ingresos_mes(),
        "DATE(pa.fecha) >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month' "
        "AND DATE(pa.fecha) < DATE_TRUNC('month', CURRENT_DATE)"
    )

def get_tendencia_anio():
    return _calcular_tendencia(
        get_ingresos_anio(),
        "DATE(pa.fecha) >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year' "
        "AND DATE(pa.fecha) < DATE_TRUNC('year', CURRENT_DATE)"
    )


# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────────────────────

def get_reporte_completo() -> dict:
    """
    Retorna dict con todos los datos para la vista de reportes.
    Filtra SOLO pagos con estado = 'aprobado'.
    """
    return {
        "Hoy": {
            "ingresos":  get_ingresos_hoy(),
            "pedidos":   get_pedidos_hoy(),
            "tendencia": "Diario",
            "metodos":   get_metodos_hoy(),
        },
        "Esta Semana": {
            "ingresos":  get_ingresos_semana(),
            "pedidos":   get_pedidos_semana(),
            "tendencia": get_tendencia_semana(),
            "metodos":   get_metodos_semana(),
        },
        "Este Mes": {
            "ingresos":  get_ingresos_mes(),
            "pedidos":   get_pedidos_mes(),
            "tendencia": get_tendencia_mes(),
            "metodos":   get_metodos_mes(),
        },
        "Este Año": {
            "ingresos":  get_ingresos_anio(),
            "pedidos":   get_pedidos_anio(),
            "tendencia": get_tendencia_anio(),
            "metodos":   get_metodos_anio(),
        },
    }