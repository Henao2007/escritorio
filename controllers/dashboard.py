"""
controllers/dashboard.py
Lógica de negocio para el dashboard del administrador.
La vista solo llama estos métodos, nunca toca la BD directamente.
"""

from models.dashboard import DashboardModel


class DashboardController:

    @staticmethod
    def cargar_dashboard(page) -> tuple[bool, str]:
        """
        Llena page.dashboard_data con todos los datos necesarios.

        Estructura de page.dashboard_data:
        {
            "ingresos_hoy":   45000.0,
            "contadores":     { total, pendiente, completado, cancelado, confirmado },
            "pedidos_recientes": [ { id, codigo, cliente_nombre, estado,
                                     total, hora, num_items } ]
        }

        Uso en la vista:
            ok, msg = DashboardController.cargar_dashboard(page)
        """
        try:
            ingresos    = DashboardModel.ingresos_hoy()
            contadores  = DashboardModel.contadores_pedidos()
            recientes   = DashboardModel.pedidos_recientes(limite=5)

            page.dashboard_data = {
                "ingresos_hoy":      ingresos,
                "contadores":        contadores,
                "pedidos_recientes": recientes,
            }
            print(f"[DashboardController] Dashboard cargado — "
                  f"ingresos: {ingresos}, total pedidos: {contadores['total']}")
            return True, ""

        except Exception as e:
            print(f"[DashboardController.cargar_dashboard] ERROR: {e}")
            return False, f"Error al cargar dashboard: {str(e)}"