import flet as ft


def pedidos_view(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Pedidos", size=28, weight="bold", color="#1F2937"),
                ft.Text("Gestión de pedidos de clientes", size=16, color="#6B7280"),
            ]
        ),
    )
