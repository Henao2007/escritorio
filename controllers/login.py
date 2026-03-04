# controllers/login.py

from models.login import AdminModel


class AdminController:

    def __init__(self):
        self.model = AdminModel()

    def login(self, email, password):

        # Validación básica
        if not email or not password:
            return {
                "status": "error",
                "message": "Todos los campos son obligatorios"
            }

        es_valido = self.model.validar_login(email, password)

        if es_valido:
            return {
                "status": "success",
                "message": "Bienvenido administrador"
            }
        else:
            return {
                "status": "error",
                "message": "Credenciales incorrectas"
            }