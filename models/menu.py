from config.conexion import conectar


class MenuModel:

    def get_all(self):
        conn = conectar()
        if not conn:
            return []
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT m.id, m.nombre, m.descripcion, m.precio, m.disponible, m.stock,
                       i.ruta
                FROM menu m
                LEFT JOIN imagenes_menu i ON i.menu_id = m.id AND i.principal = 1
                ORDER BY m.id
            """)
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "name": r[1],
                    "description": r[2] or "",
                    "price": f"$ {int(r[3]):,}".replace(",", "."),
                    "price_raw": float(r[3]),
                    "available": bool(r[4]),
                    "stock": r[5] if r[5] is not None else 0,
                    "category": "specialty",
                    "image": r[6] if r[6] else "img/comida1.jpg",
                }
                for r in rows
            ]
        except Exception as e:
            print("Error get_all:", e)
            return []
        finally:
            conn.close()

    def create(self, nombre, descripcion, precio, stock, ruta_imagen=None):
        conn = conectar()
        if not conn:
            return False
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO menu (nombre, descripcion, precio, disponible, stock) VALUES (%s, %s, %s, 1, %s) RETURNING id",
                (nombre, descripcion, precio, stock)
            )
            new_id = cur.fetchone()[0]
            if ruta_imagen:
                cur.execute(
                    "INSERT INTO imagenes_menu (menu_id, ruta, principal) VALUES (%s, %s, 1)",
                    (new_id, ruta_imagen)
                )
            conn.commit()
            return True
        except Exception as e:
            print("Error create:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    def update(self, id, nombre, descripcion, precio, stock, ruta_imagen=None):
        conn = conectar()
        if not conn:
            return False
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE menu SET nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id=%s",
                (nombre, descripcion, precio, stock, id)
            )
            if ruta_imagen:
                cur.execute(
                    "UPDATE imagenes_menu SET ruta=%s WHERE menu_id=%s AND principal=1",
                    (ruta_imagen, id)
                )
                if cur.rowcount == 0:
                    cur.execute(
                        "INSERT INTO imagenes_menu (menu_id, ruta, principal) VALUES (%s, %s, 1)",
                        (id, ruta_imagen)
                    )
            conn.commit()
            return True
        except Exception as e:
            print("Error update:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete(self, id):
        conn = conectar()
        if not conn:
            return False
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM carrito_compra WHERE menu_id=%s", (id,))
            cur.execute("DELETE FROM detalle_pedido WHERE menu_id=%s", (id,))
            cur.execute("DELETE FROM imagenes_menu WHERE menu_id=%s", (id,))
            cur.execute("DELETE FROM menu WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            print("Error delete:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    def toggle_disponible(self, id, disponible: bool):
        conn = conectar()
        if not conn:
            return False
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE menu SET disponible=%s WHERE id=%s",
                (1 if disponible else 0, id)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Error toggle:", e)
            conn.rollback()
            return False
        finally:
            conn.close()