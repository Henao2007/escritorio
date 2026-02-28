import flet as ft


def perfil_view(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Mi Perfil", size=28, weight="bold", color="#1F2937"),
                ft.Text(f"Usuario: {page.session.user}", size=16, color="#6B7280"),
            ]
        ),
    )
