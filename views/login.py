import flet as ft
from controllers.login import AdminController


def login_view(page, go_register, go_dashboard):
    """Vista de inicio de sesión principal para escritorio."""

    controller = AdminController()

    # Texto para mostrar errores de login
    error_text = ft.Text("", size=12, color="red")

    # ----------------------------
    # Campos de formulario
    # ----------------------------

    email = ft.TextField(
        label="Correo",
        hint_text="Ingresa tu correo",
        border=ft.InputBorder.UNDERLINE,
        border_color="#E5E7EB",
        filled=True,
        fill_color="white",
        label_style=ft.TextStyle(size=14, color="#374151"),
        hint_style=ft.TextStyle(color="#9CA3AF", size=13),
        text_style=ft.TextStyle(size=14, color="#111827"),
        content_padding=15,
        width=320,
        height=50,
    )

    password = ft.TextField(
        label="Contraseña",
        hint_text="Ingresa tu contraseña",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.UNDERLINE,
        border_color="#E5E7EB",
        filled=True,
        fill_color="white",
        label_style=ft.TextStyle(size=14, color="#374151"),
        hint_style=ft.TextStyle(color="#9CA3AF", size=13),
        text_style=ft.TextStyle(size=14, color="#111827"),
        content_padding=15,
        width=320,
        height=50,
    )

    # ----------------------------
    # Función Login (MVC real)
    # ----------------------------

    def login(e):
        usuario = email.value
        clave = password.value

        resultado = controller.login(usuario, clave)

        if resultado["status"] == "success":
            # Flet session es un objeto; guardamos un atributo
            setattr(page.session, "user", usuario)
            go_dashboard()
        else:
            # Mostrar mensaje de error debajo de "Ingresa tus credenciales"
            error_text.value = "Correo o contraseña incorrectos"
            page.update()

    # ----------------------------
    # Lado izquierdo
    # ----------------------------

    left_side = ft.Container(
        expand=True,
        bgcolor="#FFF9E6",
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Container(
                    width=220,
                    height=220,
                    bgcolor="white",
                    border_radius=30,
                    shadow=ft.BoxShadow(
                        blur_radius=25,
                        spread_radius=1,
                        color="#E5E7EB",
                        offset=ft.Offset(0, 10),
                    ),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Image(
                        src="img/logo.png",
                        width=160,
                        height=160,
                        fit="contain",
                    ),
                ),
                ft.Text(
                    "SENA FOOD",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#111827",
                ),
                ft.Text(
                    "ADMIN",
                    size=16,
                    color="#9CA3AF",
                ),
            ],
        ),
    )

    # ----------------------------
    # Lado derecho (Formulario)
    # ----------------------------

    right_side = ft.Container(
        expand=True,
        bgcolor="#F3F4F6",
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
            controls=[
                ft.Container(
                    width=420,
                    padding=30,
                    bgcolor="white",
                    border_radius=20,
                    shadow=ft.BoxShadow(
                        blur_radius=25,
                        spread_radius=1,
                        color="#E5E7EB",
                        offset=ft.Offset(0, 10),
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=20,
                        controls=[
                            ft.Text(
                                "Panel Administrativo",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color="#111827",
                            ),
                            ft.Text(
                                "Ingresa tus credenciales",
                                size=14,
                                color="#6B7280",
                            ),
                            ft.Column(
                                spacing=15,
                                controls=[email, password],
                            ),
                            error_text,
                            ft.Container(
                                width=320,
                                margin=ft.margin.only(top=10),
                                content=ft.ElevatedButton(
                                    "Continuar",
                                    width=320,
                                    height=48,
                                    style=ft.ButtonStyle(
                                        bgcolor="#F97316",
                                        color="white",
                                        shape=ft.RoundedRectangleBorder(
                                            radius=12
                                        ),
                                    ),
                                    on_click=login,
                                ),
                            ),
                        ],
                    ),
                ),
                ft.TextButton(
                    "¿Olvidaste tu contraseña?",
                    on_click=lambda e: go_register(),
                    style=ft.ButtonStyle(color="#6B7280"),
                ),
            ],
        ),
    )

    # ----------------------------
    # Vista principal
    # ----------------------------

    return ft.Container(
        expand=True,
        bgcolor="#FDFBF5",
        content=ft.Row(
            expand=True,
            controls=[left_side, right_side],
        ),
    )