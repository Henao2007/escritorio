import flet as ft

def perfil_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Perfil", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Gestión de perfil de usuario"),
        ])
    )