import flet as ft

from views.login import login_view
from views.register import register_view
from layout import app_layout
from config.conexion import conectar

def main(page: ft.Page):
    page.title = "SenaFood - Admin"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    def show_login():
        page.clean()
        page.add(login_view(page, show_register, show_app))

    def show_register():
        page.clean()
        page.add(register_view(page, show_login))

    def show_app():
        page.clean()
        page.add(app_layout(page, logout))

    def logout():
        if hasattr(page.session, "user"):
            del page.session.user
        show_login()

    # 🔐 CONTROL DE SESIÓN (CORRECTO)
    if hasattr(page.session, "user"):
        show_app()
    else:
        show_login()


# comprobar BD
# def main(page: ft.Page):
#     # Intentamos conectar usando la función de conexion.py
#     conn = conectar()

#     if conn:
#             page.add(ft.Text("¡Conexión exitosa!"))
#             conn.close()  # cerramos la conexión después
#     else:
#             page.add(ft.Text("Error al conectar a la base de datos"))




ft.run(main, assets_dir="assets")
