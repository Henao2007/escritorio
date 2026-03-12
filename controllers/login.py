from models.login import AdminModel


class AdminController:

    def __init__(self):
        self.model = AdminModel()

    def login(self, email, password):
        # Validación básica
        if not email or not password:
            return {
                "status": "error",
                "message": "Todos los campos son obligatorios",
                "usuario": None,
            }

        usuario = self.model.validar_login(email, password)

        if usuario:
            return {
                "status": "success",
                "message": "Bienvenido administrador",
                "usuario": usuario,  # dict con id, nombre, email, rol
            }
        else:
            return {
                "status": "error",
                "message": "Correo o contraseña incorrectos",
                "usuario": None,
            }
