import flet as ft

def dashboard_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Bienvenido al panel de control de SenaFood"),
        ])
    )