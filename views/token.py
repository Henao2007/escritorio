import flet as ft

def token_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Token", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Generación y gestión de tokens"),
        ])
    )