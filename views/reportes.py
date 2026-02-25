import flet as ft

def reportes_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Reportes", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Reportes y estadísticas"),
        ])
    )