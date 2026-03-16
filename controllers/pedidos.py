"""
controllers/pedidos.py
Lógica de negocio para la gestión de pedidos del administrador.
La vista solo llama estos métodos, nunca toca la BD directamente.
"""

from models.pedidos import PedidosModel


class PedidosController:

    # ------------------------------------------------------------------
    # CARGAR LISTA DE PEDIDOS
    # ------------------------------------------------------------------
    @staticmethod
    def cargar_pedidos(page) -> tuple[bool, str]:
        """
        Llena page.pedidos_data y page.pedidos_contadores.

        Uso en la vista:
            ok, msg = PedidosController.cargar_pedidos(page)
        """
        try:
            pedidos    = PedidosModel.listar_pedidos()
            contadores = PedidosModel.contadores()

            page.pedidos_data       = pedidos
            page.pedidos_contadores = contadores
            print(f"[PedidosController] {len(pedidos)} pedidos cargados.")
            return True, ""
        except Exception as e:
            print(f"[PedidosController.cargar_pedidos] ERROR: {e}")
            return False, f"Error al cargar pedidos: {str(e)}"

    # ------------------------------------------------------------------
    # DETALLE DE UN PEDIDO (modal "Ver")
    # ------------------------------------------------------------------
    @staticmethod
    def obtener_detalle(pedido_id: int) -> tuple[bool, dict | None, str]:
        """
        Retorna (True, detalle_dict, "") o (False, None, mensaje_error).

        Uso en la vista:
            ok, detalle, msg = PedidosController.obtener_detalle(pedido_id)
        """
        try:
            detalle = PedidosModel.obtener_detalle(pedido_id)
            if detalle is None:
                return False, None, "No se encontró el pedido."
            return True, detalle, ""
        except Exception as e:
            return False, None, f"Error al obtener detalle: {str(e)}"

    # ------------------------------------------------------------------
    # CAMBIAR ESTADO
    # ------------------------------------------------------------------
    @staticmethod
    def cambiar_estado(page, pedido_id: int, nuevo_estado: str) -> tuple[bool, str]:
        """
        Valida, persiste y actualiza page.pedidos_data en memoria.

        Uso en la vista:
            ok, msg = PedidosController.cambiar_estado(page, pedido_id, 'completado')
        """
        estados_validos = {"pendiente", "confirmado", "completado", "cancelado"}
        if nuevo_estado not in estados_validos:
            return False, f"Estado '{nuevo_estado}' no válido."

        admin_id = getattr(page, "usuario_id", None)
        if not admin_id:
            return False, "No hay sesión activa."

        try:
            ok = PedidosModel.cambiar_estado(pedido_id, nuevo_estado, admin_id)
            if ok:
                # Actualizar en memoria sin recargar toda la lista
                if hasattr(page, "pedidos_data"):
                    for p in page.pedidos_data:
                        if p["id"] == pedido_id:
                            p["estado"] = nuevo_estado
                            break
                # Recalcular contadores
                page.pedidos_contadores = PedidosModel.contadores()

                labels = {
                    "pendiente":  "Marcado como Pendiente",
                    "confirmado": "Pedido Confirmado",
                    "completado": "Pedido Completado",
                    "cancelado":  "Pedido Cancelado",
                }
                return True, labels.get(nuevo_estado, "Estado actualizado")
            return False, "No se pudo actualizar el estado."
        except Exception as e:
            return False, f"Error al cambiar estado: {str(e)}"

    # ------------------------------------------------------------------
    # GENERAR TOKEN PARA UN PEDIDO NUEVO
    # ------------------------------------------------------------------
    @staticmethod
    def generar_token(pedido_id: int) -> str:
        """
        Genera y guarda un token único tipo 'TK-XXXX'.
        Llamar justo después de insertar el pedido en la BD.

        Uso:
            token = PedidosController.generar_token(nuevo_pedido_id)
        """
        return PedidosModel.generar_token_pedido(pedido_id)

    # ------------------------------------------------------------------
    # BUSCAR PEDIDOS
    # ------------------------------------------------------------------
    @staticmethod
    def buscar(page, termino: str) -> tuple[bool, str]:
        """
        Filtra page.pedidos_data por término de búsqueda.
        Si el término está vacío, recarga todo.

        Uso en la vista (on_search):
            ok, msg = PedidosController.buscar(page, search_field.value)
        """
        if not termino or not termino.strip():
            return PedidosController.cargar_pedidos(page)

        try:
            resultados = PedidosModel.buscar(termino.strip())
            page.pedidos_data = resultados
            return True, f"{len(resultados)} resultado(s) encontrado(s)"
        except Exception as e:
            return False, f"Error en la búsqueda: {str(e)}"