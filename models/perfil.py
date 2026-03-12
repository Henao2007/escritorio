from config.conexion import conectar
import psycopg2.extras


class PerfilModel:

    @staticmethod
    def obtener_perfil_por_id(usuario_id: int) -> dict | None:
        sql = """
            SELECT
                u.id,
                u.nombre,
                u.email,
                u.telefono,
                u.tipo_documento,
                u.numero_documento,
                u.discapacidad,
                r.nombre        AS rol_nombre,
                r.descripcion   AS rol_descripcion,
                COALESCE(pa.permisos, '') AS permisos
            FROM usuarios u
            INNER JOIN roles r
                ON u.role_id = r.id
            LEFT JOIN perfil_administrativo pa
                ON pa.usuario_id = u.id
            WHERE u.id = %s
            LIMIT 1
        """
        conn = conectar()
        if conn is None:
            return None
        try:
            # RealDictCursor hace que cada fila sea un dict con nombres de columna
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, (usuario_id,))
                row = cursor.fetchone()

            if row is None:
                return None

            return {
                "id":               row["id"],
                "name":             row["nombre"],
                "role":             row["rol_nombre"],
                "email":            row["email"],
                "phone":            row["telefono"] or "",
                "member_since":     "Miembro desde 15 de Enero, 2024",
                "verification_token": "123456",
                "avatar_src":       None,
                # extras
                "tipo_documento":   row["tipo_documento"],
                "numero_documento": row["numero_documento"],
                "discapacidad":     bool(row["discapacidad"]),
                "rol_descripcion":  row["rol_descripcion"],
                "permisos":         row["permisos"],
            }
        finally:
            conn.close()

    # ------------------------------------------------------------------

    @staticmethod
    def actualizar_perfil(usuario_id: int, nombre: str, telefono: str, email: str) -> bool:
        sql = """
            UPDATE usuarios
            SET nombre   = %s,
                telefono = %s,
                email    = %s
            WHERE id = %s
        """
        conn = conectar()
        if conn is None:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (nombre, telefono, email, usuario_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------

    @staticmethod
    def cambiar_password(usuario_id: int, nuevo_hash: str) -> bool:
        sql = "UPDATE usuarios SET password = %s WHERE id = %s"
        conn = conectar()
        if conn is None:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (nuevo_hash, usuario_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------

    @staticmethod
    def obtener_password_hash(usuario_id: int) -> str | None:
        sql = "SELECT password FROM usuarios WHERE id = %s LIMIT 1"
        conn = conectar()
        if conn is None:
            return None
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, (usuario_id,))
                row = cursor.fetchone()
            return row["password"] if row else None
        finally:
            conn.close()
