from config.conexion import conectar

class AdminModel:

    def validar_login(self, email, password):
        conexion = conectar()
        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()
            query = """
                SELECT id
                FROM usuarios
                WHERE email = %s AND password = %s
            """
            cursor.execute(query, (email, password))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            return resultado is not None
        except Exception as e:
            print("Error en la consulta:", e)
            return False