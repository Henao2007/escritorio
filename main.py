import flet as ft

from views.login import login_view
from views.forgot_password import forgot_password_view
from views.verify_code import verify_code_view
from views.reset_password import reset_password_view
from layout import app_layout


def main(page: ft.Page):
    page.title = "SenaFood - Admin"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    def show_login():
        page.clean()
        page.add(login_view(page, show_forgot_password, show_app, show_forgot_password))

    def show_forgot_password():
        page.clean()
        page.add(forgot_password_view(page, show_login, show_verify_code))

    def show_verify_code():
        page.clean()
        page.add(verify_code_view(page, show_login, show_reset_password))

    def show_reset_password():
        page.clean()
        page.add(reset_password_view(page, show_login))

    def show_app():
        page.clean()
        page.add(app_layout(page, logout))

    def logout():
        if hasattr(page.session, "user"):
            delattr(page.session, "user")
        show_login()

    # 🔐 CONTROL DE SESIÓN (CORRECTO)
    if hasattr(page.session, "user"):
        show_app()
    else:
        show_login()


ft.run(main, assets_dir="assets")