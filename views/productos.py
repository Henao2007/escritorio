import flet as ft


def productos_view(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Productos", size=28, weight="bold"),
                ft.Text("Gestión de productos del menú"),
            ]
        ),
    )
