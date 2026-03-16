"""
models/tokens.py
Acceso a datos de tokens de pedidos — PostgreSQL
Flujo: pendiente → confirmado → completado
"""

import psycopg2.extras
from config.conexion import conectar


class TokensModel:

    # ------------------------------------------------------------------
    # LISTAR TODOS LOS TOKENS CON INFO DEL PEDIDO
    # ------------------------------------------------------------------
    @staticmethod
    def listar_tokens() -> list[dict]:
        """
        Retorna lista de tokens con datos del pedido y cliente:
            token_id, token, estado_token, fecha_generacion,
            pedido_id, codigo, estado_pedido, total,
            cliente_nombre, cliente_documento, cliente_email
        """
        sql = """
            SELECT
                tp.id                                             AS token_id,
                tp.token,
                tp.estado                                         AS estado_token,
                TO_CHAR(tp.fecha_generacion, 'DD/MM/YYYY HH24:MI') AS fecha_generacion,
                p.id                                              AS pedido_id,
                'PED-' || LPAD(p.id::TEXT, 3, '0')               AS codigo,
                p.estado                                          AS estado_pedido,
                p.total,
                u.nombre                                          AS cliente_nombre,
                u.tipo_documento || ' ' || u.numero_documento     AS cliente_documento,
                u.email                                           AS cliente_email
            FROM tokens_pedido tp
            INNER JOIN pedidos  p ON p.id  = tp.pedido_id
            INNER JOIN usuarios u ON u.id  = p.usuario_id
            ORDER BY tp.fecha_generacion DESC
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
            print(f"[TokensModel.listar_tokens] ERROR: {e}")
            return []
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # DETALLE COMPLETO DE UN TOKEN/PEDIDO (para el modal)
    # ------------------------------------------------------------------
    @staticmethod
    def obtener_detalle(pedido_id: int) -> dict | None:
        """
        Retorna dict con:
            token, pedido (info completa), items, metodo_pago, comprobante_img
        """
        sql_pedido = """
            SELECT
                tp.token,
                tp.estado                                          AS estado_token,
                'PED-' || LPAD(p.id::TEXT, 3, '0')                AS codigo,
                TO_CHAR(p.fecha, 'DD/MM/YYYY')                     AS fecha,
                TO_CHAR(p.fecha, 'HH12:MI AM')                     AS hora,
                p.estado                                           AS estado_pedido,
                p.total,
                u.nombre                                           AS cliente_nombre,
                u.tipo_documento || ' ' || u.numero_documento      AS cliente_documento,
                u.email                                            AS cliente_email,
                COALESCE(u.telefono, '')                           AS cliente_telefono,
                COALESCE(mp.nombre, 'No registrado')               AS metodo_pago
            FROM pedidos p
            INNER JOIN usuarios      u  ON u.id  = p.usuario_id
            LEFT  JOIN tokens_pedido tp ON tp.pedido_id = p.id
            LEFT  JOIN pagos         pg ON pg.pedido_id = p.id
            LEFT  JOIN metodos_pago  mp ON mp.id = pg.metodo_pago_id
            WHERE p.id = %s
            LIMIT 1
        """
        sql_items = """
            SELECT
                m.nombre        AS menu_nombre,
                m.descripcion,
                m.precio        AS precio_unitario,
                dp.cantidad,
                dp.subtotal,
                COALESCE(im.ruta, '') AS imagen
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
            print(f"[TokensModel.obtener_detalle] ERROR: {e}")
            return None
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # CAMBIAR ESTADO DEL PEDIDO (confirmar / completar)
    # ------------------------------------------------------------------
    @staticmethod
    def cambiar_estado(pedido_id: int, nuevo_estado: str, admin_id: int) -> bool:
        """
        Actualiza pedidos.estado y tokens_pedido.estado según el flujo:
            pendiente → confirmado → completado
        También registra en historial_pedidos.
        """
        estado_token = {
            "confirmado": "activo",
            "completado": "usado",
            "cancelado":  "cancelado",
        }.get(nuevo_estado, "activo")

        conn = conectar()
        if conn is None:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE pedidos SET estado = %s WHERE id = %s",
                    (nuevo_estado, pedido_id)
                )
                cursor.execute(
                    "UPDATE tokens_pedido SET estado = %s WHERE pedido_id = %s",
                    (estado_token, pedido_id)
                )
                cursor.execute("""
                    INSERT INTO historial_pedidos (pedido_id, usuario_id, estado, observacion)
                    VALUES (%s, %s, %s, %s)
                """, (
                    pedido_id, admin_id, nuevo_estado,
                    f"Estado cambiado a '{nuevo_estado}' por administrador"
                ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"[TokensModel.cambiar_estado] ERROR: {e}")
            return False
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # CONTADORES
    # ------------------------------------------------------------------
    @staticmethod
    def contadores() -> dict:
        sql = """
            SELECT
                COUNT(*) FILTER (WHERE p.estado = 'pendiente')  AS pendiente,
                COUNT(*) FILTER (WHERE p.estado = 'confirmado') AS confirmado,
                COUNT(*) FILTER (WHERE p.estado = 'completado') AS completado,
                COUNT(*) FILTER (WHERE p.estado = 'cancelado')  AS cancelado
            FROM tokens_pedido tp
            INNER JOIN pedidos p ON p.id = tp.pedido_id
        """
        conn = conectar()
        if conn is None:
            return {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0}
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql)
                row = cursor.fetchone()
            return {k: int(v) for k, v in row.items()} if row else \
                   {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0}
        except Exception as e:
            print(f"[TokensModel.contadores] ERROR: {e}")
            return {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0}
        finally:
            conn.close()