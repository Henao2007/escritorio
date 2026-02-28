import flet as ft


def token_view(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Token", size=28, weight="bold", color="#1F2937"),
                ft.Text("Generación y gestión de tokens", size=16, color="#6B7280"),
            ]
        ),
    )
