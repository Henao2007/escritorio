import flet as ft


def login_view(page, go_register, go_dashboard):
    """Vista de inicio de sesión principal para escritorio.

    Usa el diseño moderno del proyecto `escritorio-login`, pero mantiene
    el flujo actual: al autenticarse se navega directamente al dashboard
    principal de `escritorio-Proyecto`.
    """

    # Campos de formulario
    email = ft.TextField(
        label="Usuario",
        hint_text="Ingresa tu usuario",
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

    def login(e):
        # Validación mínima: solo comprobamos que haya valores
        if email.value and password.value:
            page.session.user = email.value
            go_dashboard()

    # Tarjeta de credenciales de demostración
    # demo_credentials = ft.Container(
    #     width=320,
    #     padding=15,
    #     bgcolor="#F9FAFB",
    #     border_radius=10,
    #     content=ft.Column(
    #         spacing=4,
    #         controls=[
    #             ft.Text(
    #                 "Credenciales de demostración:",
    #                 size=13,
    #                 weight=ft.FontWeight.BOLD,
    #                 color="#374151",
    #             ),
    #             ft.Text("Usuario: admin", size=12, color="#4B5563"),
    #             ft.Text("Contraseña: sena2024", size=12, color="#4B5563"),
    #         ],
    #     ),
    # )

    # Lado izquierdo: tarjeta con el logo (se mantiene mismo archivo de logo)
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
                        # Se usa el mismo logo principal del proyecto
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
                    weight=ft.FontWeight.NORMAL,
                ),
            ],
        ),
    )

    # Lado derecho: formulario de inicio de sesión
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
                    padding=ft.Padding.all(30),
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
                            ft.Container(
                                width=320,
                                margin=ft.Margin.only(top=10),
                                content=ft.Button(
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

    # Contenedor principal con diseño responsivo simple
    return ft.Container(
        expand=True,
        bgcolor="#FDFBF5",
        content=ft.Row(
            expand=True,
            controls=[left_side, right_side],
        ),
    )
