import flet as ft

def productos_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Productos", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Gestión de productos del menú"),
        ])
    )