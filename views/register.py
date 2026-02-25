import flet as ft

def register_view(page, go_login):
    documento = ft.TextField(
        label="Número de documento",
        hint_text="Ingresa tu número de documento",
        border=ft.InputBorder.UNDERLINE,
        border_color="#D1D5DB",
        filled=True,
        fill_color="white",
        label_style=ft.TextStyle(
            size=14,
            color="#374151"
        ),
        hint_style=ft.TextStyle(color="#9CA3AF", size=12),
        text_style=ft.TextStyle(size=14, color="#111827"),
        content_padding=15,
        width=350,
        height=50
    )

    nombre = ft.TextField(
        label="Nombre completo",
        hint_text="Ingresa tu nombre completo",
        border=ft.InputBorder.UNDERLINE,
        border_color="#D1D5DB",
        filled=True,
        fill_color="white",
        label_style=ft.TextStyle(
            size=14,
            color="#374151"
        ),
        hint_style=ft.TextStyle(color="#9CA3AF", size=12),
        text_style=ft.TextStyle(size=14, color="#111827"),
        content_padding=15,
        width=350,
        height=50
    )

    email = ft.TextField(
        label="Correo electrónico",
        hint_text="Ingresa tu correo electrónico",
        border=ft.InputBorder.UNDERLINE,
        border_color="#D1D5DB",
        filled=True,
        fill_color="white",
        label_style=ft.TextStyle(
            size=14,
            color="#374151"
        ),
        hint_style=ft.TextStyle(color="#9CA3AF", size=12),
        text_style=ft.TextStyle(size=14, color="#111827"),
        content_padding=15,
        width=350,
        height=50
    )

    password = ft.TextField(
        label="Contraseña",
        hint_text="Crea una contraseña segura",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.UNDERLINE,
        border_color="#D1D5DB",
        filled=True,
        fill_color="white",
        label_style=ft.TextStyle(
            size=14,
            color="#374151"
        ),
        hint_style=ft.TextStyle(color="#9CA3AF", size=12),
        text_style=ft.TextStyle(size=14, color="#111827"),
        content_padding=15,
        width=350,
        height=50
    )

    def register(e):
        if all([documento.value, nombre.value, email.value, password.value]):
            go_login()

    return ft.Container(
        expand=True,
        bgcolor="#FAF7F2",
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
            controls=[
                # Logo y título
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    controls=[
                        ft.Image(
                            src="img/logo.png",
                            width=120,
                            height=120,
                            fit="contain",
                        ),
                        ft.Text(
                            "SENA FOOD",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="#1F2937"
                        ),
                    ]
                ),
                
                # Formulario
                ft.Container(
                    width=400,
                    padding=ft.padding.all(30),
                    bgcolor="white",
                    border_radius=15,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.Text(
                                "Registro de Usuario",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color="#1F2937"
                            ),
                            
                            # Campos
                            ft.Column(
                                width=350,
                                spacing=15,
                                controls=[
                                    documento,
                                    nombre,
                                    email,
                                    password,
                                ]
                            ),
                            
                            # Checkbox
                            ft.Container(
                                width=350,
                                content=ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.Checkbox(
                                            value=False,
                                            check_color="white",
                                            fill_color="#F97316"
                                        ),
                                        ft.Text(
                                            "Acepto términos y condiciones",
                                            size=13,
                                            color="#6B7280"
                                        )
                                    ]
                                )
                            ),
                            
                            # Botón
                            ft.Container(
                                width=350,
                                margin=ft.margin.only(top=10),
                                content=ft.ElevatedButton(
                                    "REGISTRARME",
                                    width=350,
                                    height=48,
                                    style=ft.ButtonStyle(
                                        color="white",
                                        bgcolor="#F97316",
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=register
                                )
                            ),
                            
                            # Enlace
                            ft.Container(
                                margin=ft.margin.only(top=15),
                                content=ft.TextButton(
                                    "¿Ya tienes cuenta? Inicia sesión",
                                    style=ft.ButtonStyle(
                                        color="#6B7280",
                                    ),
                                    on_click=lambda e: go_login()
                                )
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )