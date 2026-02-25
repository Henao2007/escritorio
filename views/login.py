import flet as ft

def login_view(page, go_register, go_dashboard):
    email = ft.TextField(label="Correo electrónico")
    password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True
    )

    def login(e):
        if email.value and password.value:
            page.session.user = email.value
            go_dashboard()

    return ft.Container(
        expand=True,
        bgcolor="#FAF7F2",
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            width=350,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="img/logo.png", width=140),
                email,
                password,
                ft.ElevatedButton("INICIAR SESIÓN", on_click=login),
                ft.TextButton(
                    "¿No tienes cuenta? Regístrate",
                    on_click=lambda e: go_register()
                ),
            ],
        ),
    )
