"""
models/dashboard.py
Consultas SQL para el dashboard del administrador — PostgreSQL
"""

import psycopg2.extras
from config.conexion import conectar


class DashboardModel:

    # ------------------------------------------------------------------
    # INGRESOS DEL DÍA (suma de pedidos completados hoy)
    # ------------------------------------------------------------------
    @staticmethod
    def ingresos_hoy() -> float:
        sql = """
            SELECT COALESCE(SUM(total), 0) AS ingresos
            FROM pedidos
            WHERE estado = 'completado'
              AND DATE(fecha) = CURRENT_DATE
        """
        conn = conectar()
        if conn is None:
            return 0.0
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql)
                row = cursor.fetchone()
            return float(row["ingresos"]) if row else 0.0
        except Exception as e:
            print(f"[DashboardModel.ingresos_hoy] ERROR: {e}")
            return 0.0
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # CONTADORES DE PEDIDOS POR ESTADO
    # ------------------------------------------------------------------
    @staticmethod
    def contadores_pedidos() -> dict:
        """
        Retorna:
            { total, pendiente, completado, cancelado, confirmado }
        """
        sql = """
            SELECT
                COUNT(*)                                          AS total,
                COUNT(*) FILTER (WHERE estado = 'pendiente')     AS pendiente,
                COUNT(*) FILTER (WHERE estado = 'completado')    AS completado,
                COUNT(*) FILTER (WHERE estado = 'cancelado')     AS cancelado,
                COUNT(*) FILTER (WHERE estado = 'confirmado')    AS confirmado
            FROM pedidos
        """
        conn = conectar()
        if conn is None:
            return {"total": 0, "pendiente": 0, "completado": 0, "cancelado": 0, "confirmado": 0}
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql)
                row = cursor.fetchone()
            if row:
                return {k: int(v) for k, v in row.items()}
            return {"total": 0, "pendiente": 0, "completado": 0, "cancelado": 0, "confirmado": 0}
        except Exception as e:
            print(f"[DashboardModel.contadores_pedidos] ERROR: {e}")
            return {"total": 0, "pendiente": 0, "completado": 0, "cancelado": 0, "confirmado": 0}
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # PEDIDOS RECIENTES (últimos N)
    # ------------------------------------------------------------------
    @staticmethod
    def pedidos_recientes(limite: int = 5) -> list[dict]:
        """
        Retorna lista de dicts:
            id, codigo, cliente_nombre, estado, total,
            hora, num_items
        """
        sql = """
            SELECT
                p.id,
                'PED-' || LPAD(p.id::TEXT, 3, '0')   AS codigo,
                u.nombre                               AS cliente_nombre,
                p.estado,
                p.total,
                TO_CHAR(p.fecha, 'HH12:MI AM')        AS hora,
                COUNT(dp.id)                           AS num_items
            FROM pedidos p
            INNER JOIN usuarios u       ON u.id  = p.usuario_id
            LEFT  JOIN detalle_pedido dp ON dp.pedido_id = p.id
            GROUP BY p.id, u.nombre
            ORDER BY p.fecha DESC
            LIMIT %s
        """
        conn = conectar()
        if conn is None:
            return []
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, (limite,))
                rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"[DashboardModel.pedidos_recientes] ERROR: {e}")
            return []
        finally:
            conn.close()