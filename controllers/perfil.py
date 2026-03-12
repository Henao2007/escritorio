import hashlib
from models.perfil import PerfilModel


class PerfilController:

    @staticmethod
    def cargar_perfil(page) -> tuple[bool, str]:
        usuario_id = getattr(page, "usuario_id", None)
        print(f">>> [PERFIL] usuario_id en page: {usuario_id}")

        if not usuario_id:
            print(">>> [PERFIL] ERROR: No hay usuario_id en page")
            return False, "No hay sesión activa."

        try:
            datos = PerfilModel.obtener_perfil_por_id(usuario_id)
            print(f">>> [PERFIL] datos retornados por el modelo: {datos}")

            if datos is None:
                print(">>> [PERFIL] ERROR: El modelo retornó None")
                return False, "No se encontró el perfil del usuario."

            token_actual  = getattr(page, "profile_data", {}).get("verification_token", "123456")
            avatar_actual = getattr(page, "profile_data", {}).get("avatar_src", None)
            datos["verification_token"] = token_actual
            datos["avatar_src"]         = avatar_actual

            page.profile_data = datos
            print(f">>> [PERFIL] page.profile_data asignado correctamente: {page.profile_data}")
            return True, ""

        except Exception as e:
            print(f">>> [PERFIL] EXCEPCIÓN: {str(e)}")
            return False, f"Error al cargar perfil: {str(e)}"

    # ------------------------------------------------------------------

    @staticmethod
    def guardar_perfil(page, nombre: str, telefono: str, email: str) -> tuple[bool, str]:
        nombre   = nombre.strip()
        telefono = telefono.strip()
        email    = email.strip()

        if not nombre:
            return False, "El nombre no puede estar vacío."
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 caracteres."
        if not email or "@" not in email:
            return False, "Ingresa un correo electrónico válido."
        if telefono and not telefono.lstrip("+").isdigit():
            return False, "El teléfono solo debe contener números."

        usuario_id = getattr(page, "usuario_id", None)
        if not usuario_id:
            return False, "No hay sesión activa."

        try:
            ok = PerfilModel.actualizar_perfil(usuario_id, nombre, telefono, email)
            if ok:
                page.profile_data["name"]  = nombre
                page.profile_data["phone"] = telefono
                page.profile_data["email"] = email
                return True, "Cambios guardados con éxito"
            return False, "No se realizaron cambios en el perfil."
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"

    # ------------------------------------------------------------------

    @staticmethod
    def cambiar_password(page, password_actual: str, nueva_password: str, confirmar_password: str) -> tuple[bool, str]:
        if not all([password_actual, nueva_password, confirmar_password]):
            return False, "Todos los campos son obligatorios."
        if nueva_password != confirmar_password:
            return False, "Las contraseñas nuevas no coinciden."
        if len(nueva_password) < 8:
            return False, "La nueva contraseña debe tener al menos 8 caracteres."

        usuario_id = getattr(page, "usuario_id", None)
        if not usuario_id:
            return False, "No hay sesión activa."

        try:
            hash_bd = PerfilModel.obtener_password_hash(usuario_id)
            if hash_bd is None:
                return False, "Usuario no encontrado."
            if not PerfilController._verificar(password_actual, hash_bd):
                return False, "La contraseña actual es incorrecta."

            nuevo_hash = PerfilController._hashear(nueva_password)
            ok = PerfilModel.cambiar_password(usuario_id, nuevo_hash)
            if ok:
                return True, "Contraseña actualizada correctamente"
            return False, "No se pudo actualizar la contraseña."
        except Exception as e:
            return False, f"Error al cambiar contraseña: {str(e)}"

    # ------------------------------------------------------------------

    @staticmethod
    def _hashear(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def _verificar(password_plano: str, hash_bd: str) -> bool:
        return hashlib.sha256(password_plano.encode("utf-8")).hexdigest() == hash_bd
