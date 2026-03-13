"""
models/pedidos.py
Acceso a datos de pedidos — PostgreSQL con psycopg2
Tablas: pedidos, detalle_pedido, tokens_pedido, usuarios, menu, imagenes_menu
"""

import uuid
import psycopg2.extras
from config.conexion import conectar


class PedidosModel:

    # ------------------------------------------------------------------
    # LISTAR TODOS LOS PEDIDOS
    # ------------------------------------------------------------------
    @staticmethod
    def listar_pedidos() -> list[dict]:
        """
        Retorna lista de pedidos con datos del cliente y token.
        Cada dict:
            id, codigo, token, cliente_nombre, cliente_documento,
            fecha, hora, total, estado
        """
        sql = """
            SELECT
                p.id,
                'PED-' || LPAD(p.id::TEXT, 3, '0')          AS codigo,
                COALESCE(tp.token, p.token, '')               AS token,
                u.nombre                                      AS cliente_nombre,
                u.tipo_documento || ' ' || u.numero_documento AS cliente_documento,
                TO_CHAR(p.fecha, 'DD Mon YYYY')               AS fecha,
                TO_CHAR(p.fecha, 'HH24:MI')                   AS hora,
                p.total,
                p.estado
            FROM pedidos p
            INNER JOIN usuarios u ON u.id = p.usuario_id
            LEFT  JOIN tokens_pedido tp ON tp.pedido_id = p.id
            ORDER BY p.fecha DESC
        """
        conn = conectar()
        if conn is None:
            return []
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"[PedidosModel.listar_pedidos] ERROR: {e}")
            return []
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # DETALLE COMPLETO DE UN PEDIDO
    # ------------------------------------------------------------------
    @staticmethod
    def obtener_detalle(pedido_id: int) -> dict | None:
        """
        Retorna:
            {
              pedido: { id, codigo, token, fecha, hora, estado, total,
                        cliente_nombre, cliente_documento, cliente_telefono },
              items:  [ { menu_nombre, descripcion, imagen,
                          cantidad, precio_unitario, subtotal } ]
            }
        """
        sql_pedido = """
            SELECT
                p.id,
                'PED-' || LPAD(p.id::TEXT, 3, '0')          AS codigo,
                COALESCE(tp.token, p.token, '')               AS token,
                TO_CHAR(p.fecha, 'DD/MM/YYYY')                AS fecha,
                TO_CHAR(p.fecha, 'HH24:MI')                   AS hora,
                p.estado,
                p.total,
                u.nombre                                      AS cliente_nombre,
                u.tipo_documento || ' ' || u.numero_documento AS cliente_documento,
                COALESCE(u.telefono, '')                      AS cliente_telefono
            FROM pedidos p
            INNER JOIN usuarios u ON u.id = p.usuario_id
            LEFT  JOIN tokens_pedido tp ON tp.pedido_id = p.id
            WHERE p.id = %s
            LIMIT 1
        """
        sql_items = """
            SELECT
                m.nombre        AS menu_nombre,
                m.descripcion,
                COALESCE(im.ruta, '') AS imagen,
                dp.cantidad,
                m.precio        AS precio_unitario,
                dp.subtotal
            FROM detalle_pedido dp
            INNER JOIN menu m ON m.id = dp.menu_id
            LEFT  JOIN imagenes_menu im
                ON im.menu_id = m.id AND im.principal = 1
            WHERE dp.pedido_id = %s
        """
        conn = conectar()
        if conn is None:
            return None
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql_pedido, (pedido_id,))
                pedido = cursor.fetchone()
                if pedido is None:
                    return None
                cursor.execute(sql_items, (pedido_id,))
                items = cursor.fetchall()
            return {
                "pedido": dict(pedido),
                "items":  [dict(i) for i in items],
            }
        except Exception as e:
            print(f"[PedidosModel.obtener_detalle] ERROR: {e}")
            return None
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # CAMBIAR ESTADO
    # ------------------------------------------------------------------
    @staticmethod
    def cambiar_estado(pedido_id: int, nuevo_estado: str, admin_id: int) -> bool:
        sql_update = "UPDATE pedidos SET estado = %s WHERE id = %s"
        sql_historial = """
            INSERT INTO historial_pedidos (pedido_id, usuario_id, estado, observacion)
            VALUES (%s, %s, %s, %s)
        """
        conn = conectar()
        if conn is None:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_update, (nuevo_estado, pedido_id))
                cursor.execute(sql_historial, (
                    pedido_id,
                    admin_id,
                    nuevo_estado,
                    f"Estado cambiado a '{nuevo_estado}' por administrador",
                ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"[PedidosModel.cambiar_estado] ERROR: {e}")
            return False
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # CONTADORES PARA LAS TARJETAS SUPERIORES
    # ------------------------------------------------------------------
    @staticmethod
    def contadores() -> dict:
        sql = """
            SELECT estado, COUNT(*) AS total
            FROM pedidos
            GROUP BY estado
        """
        conn = conectar()
        if conn is None:
            return {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0}
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
            base = {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0}
            for r in rows:
                estado = r["estado"].lower()
                if estado in base:
                    base[estado] = int(r["total"])
            return base
        except Exception as e:
            print(f"[PedidosModel.contadores] ERROR: {e}")
            return {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0}
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # GENERAR TOKEN ÚNICO AL CREAR UN PEDIDO
    # ------------------------------------------------------------------
    @staticmethod
    def generar_token_pedido(pedido_id: int) -> str:
        token = "TK-" + uuid.uuid4().hex[:4].upper()

        sql_insert = """
            INSERT INTO tokens_pedido (pedido_id, token, estado)
            VALUES (%s, %s, 'activo')
        """
        sql_update = "UPDATE pedidos SET token = %s WHERE id = %s"

        conn = conectar()
        if conn is None:
            return token
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_insert, (pedido_id, token))
                cursor.execute(sql_update, (token, pedido_id))
            conn.commit()
            return token
        except Exception as e:
            conn.rollback()
            print(f"[PedidosModel.generar_token_pedido] ERROR: {e}")
            return token
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # BUSCAR PEDIDOS
    # ------------------------------------------------------------------
    @staticmethod
    def buscar(termino: str) -> list[dict]:
        like = f"%{termino}%"
        sql = """
            SELECT
                p.id,
                'PED-' || LPAD(p.id::TEXT, 3, '0')          AS codigo,
                COALESCE(tp.token, p.token, '')               AS token,
                u.nombre                                      AS cliente_nombre,
                u.tipo_documento || ' ' || u.numero_documento AS cliente_documento,
                TO_CHAR(p.fecha, 'DD Mon YYYY')               AS fecha,
                TO_CHAR(p.fecha, 'HH24:MI')                   AS hora,
                p.total,
                p.estado
            FROM pedidos p
            INNER JOIN usuarios u ON u.id = p.usuario_id
            LEFT  JOIN tokens_pedido tp ON tp.pedido_id = p.id
            WHERE
                p.id::TEXT          ILIKE %s
                OR u.nombre          ILIKE %s
                OR u.numero_documento ILIKE %s
                OR tp.token           ILIKE %s
            ORDER BY p.fecha DESC
        """
        conn = conectar()
        if conn is None:
            return []
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, (like, like, like, like))
                rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"[PedidosModel.buscar] ERROR: {e}")
            return []
        finally:
            conn.close()
