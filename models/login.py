import hashlib
import psycopg2.extras
from config.conexion import conectar


class AdminModel:

    def validar_login(self, email, password):
        # Hashear la contraseña ingresada antes de comparar con la BD
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        conn = conectar()
        if conn is None:
            return None
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                query = """
                    SELECT u.id, u.nombre, u.email, r.nombre AS rol
                    FROM usuarios u
                    INNER JOIN roles r ON u.role_id = r.id
                    WHERE u.email = %s AND u.password = %s
                    LIMIT 1
                """
                cursor.execute(query, (email, password_hash))
                resultado = cursor.fetchone()
            return dict(resultado) if resultado else None
        except Exception as e:
            print("Error en la consulta:", e)
            return None
        finally:
            conn.close()
