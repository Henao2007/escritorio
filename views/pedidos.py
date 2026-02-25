import flet as ft

def pedidos_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Pedidos", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Gestión de pedidos de clientes"),
        ])
    )