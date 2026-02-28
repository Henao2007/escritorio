import flet as ft


def reportes_view(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Reportes", size=28, weight="bold", color="#1F2937"),
                ft.Text("Reportes y estadísticas", size=16, color="#6B7280"),
            ]
        ),
    )
