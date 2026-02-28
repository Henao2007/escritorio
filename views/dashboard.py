import flet as ft


def dashboard_view(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard"),
                ft.Text(f"Bienvenido, {page.session.user}"),
            ]
        ),
    )
