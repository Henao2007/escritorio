"""
controllers/tokens.py
Lógica de negocio para la gestión de tokens de pedidos.
Flujo de estados: pendiente → confirmado → completado
"""

from models.tokens import TokensModel


class TokensController:

    # ------------------------------------------------------------------
    # CARGAR LISTA DE TOKENS
    # ------------------------------------------------------------------
    @staticmethod
    def cargar_tokens(page) -> tuple[bool, str]:
        """
        Llena page.tokens_data y page.tokens_contadores.

        Uso en la vista:
            ok, msg = TokensController.cargar_tokens(page)
        """
        try:
            tokens     = TokensModel.listar_tokens()
            contadores = TokensModel.contadores()
            page.tokens_data       = tokens
            page.tokens_contadores = contadores
            print(f"[TokensController] {len(tokens)} tokens cargados.")
            return True, ""
        except Exception as e:
            return False, f"Error al cargar tokens: {str(e)}"

    # ------------------------------------------------------------------
    # DETALLE DE UN TOKEN (para el modal)
    # ------------------------------------------------------------------
    @staticmethod
    def obtener_detalle(pedido_id: int) -> tuple[bool, dict | None, str]:
        """
        Retorna (True, detalle, "") o (False, None, mensaje_error).

        Uso en la vista:
            ok, detalle, msg = TokensController.obtener_detalle(pedido_id)
        """
        try:
            detalle = TokensModel.obtener_detalle(pedido_id)
            if detalle is None:
                return False, None, "No se encontró el pedido."
            return True, detalle, ""
        except Exception as e:
            return False, None, f"Error al obtener detalle: {str(e)}"

    # ------------------------------------------------------------------
    # CONFIRMAR TOKEN (pendiente → confirmado)
    # ------------------------------------------------------------------
    @staticmethod
    def confirmar_token(page, pedido_id: int) -> tuple[bool, str]:
        """
        Confirma el pedido: pendiente → confirmado.

        Uso en la vista:
            ok, msg = TokensController.confirmar_token(page, pedido_id)
        """
        admin_id = getattr(page, "usuario_id", None)
        if not admin_id:
            return False, "No hay sesión activa."
        try:
            ok = TokensModel.cambiar_estado(pedido_id, "confirmado", admin_id)
            if ok:
                _actualizar_en_memoria(page, pedido_id, "confirmado")
                return True, "Pedido confirmado correctamente"
            return False, "No se pudo confirmar el pedido."
        except Exception as e:
            return False, f"Error al confirmar: {str(e)}"

    # ------------------------------------------------------------------
    # COMPLETAR PEDIDO (confirmado → completado)
    # ------------------------------------------------------------------
    @staticmethod
    def completar_pedido(page, pedido_id: int) -> tuple[bool, str]:
        """
        Marca el pedido como entregado: confirmado → completado.

        Uso en la vista:
            ok, msg = TokensController.completar_pedido(page, pedido_id)
        """
        admin_id = getattr(page, "usuario_id", None)
        if not admin_id:
            return False, "No hay sesión activa."
        try:
            ok = TokensModel.cambiar_estado(pedido_id, "completado", admin_id)
            if ok:
                _actualizar_en_memoria(page, pedido_id, "completado")
                return True, "Pedido marcado como completado"
            return False, "No se pudo completar el pedido."
        except Exception as e:
            return False, f"Error al completar: {str(e)}"

    # ------------------------------------------------------------------
    # CANCELAR PEDIDO
    # ------------------------------------------------------------------
    @staticmethod
    def cancelar_pedido(page, pedido_id: int) -> tuple[bool, str]:
        admin_id = getattr(page, "usuario_id", None)
        if not admin_id:
            return False, "No hay sesión activa."
        try:
            ok = TokensModel.cambiar_estado(pedido_id, "cancelado", admin_id)
            if ok:
                _actualizar_en_memoria(page, pedido_id, "cancelado")
                return True, "Pedido cancelado"
            return False, "No se pudo cancelar el pedido."
        except Exception as e:
            return False, f"Error al cancelar: {str(e)}"


# ── Helper privado ────────────────────────────────────────────────────
def _actualizar_en_memoria(page, pedido_id: int, nuevo_estado: str):
    """Actualiza page.tokens_data y recalcula contadores sin recargar la BD."""
    if hasattr(page, "tokens_data"):
        for t in page.tokens_data:
            if t.get("pedido_id") == pedido_id:
                t["estado_pedido"] = nuevo_estado
                t["estado_token"]  = {
                    "confirmado": "activo",
                    "completado": "usado",
                    "cancelado":  "cancelado",
                }.get(nuevo_estado, "activo")
                break
    page.tokens_contadores = TokensModel.contadores()