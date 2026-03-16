import re
import flet as ft
from views.styles import show_toast


def forgot_password_view(page: ft.Page, go_login, go_verify_code):
    """Vista inicial para solicitar el correo electrónico y recuperar contraseña."""

    error_text = ft.Text("", size=12, color="red")

    # ── Helpers de tamaño ────────────────────────────────────────────
    def is_mobile():
        return page.width is not None and page.width < 700

    def is_tablet():
        return page.width is not None and 700 <= page.width < 1100

    # ── Validación de email ──────────────────────────────────────────
    # Exige: texto @ texto . texto  (ej: usuario@dominio.com)
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def _email_valido(valor: str) -> bool:
        return bool(EMAIL_RE.match((valor or "").strip()))

    # ── Campo de email ────────────────────────────────────────────────
    email_field = ft.TextField(
        hint_text="ejemplo@correo.com",
        prefix_icon=ft.Icons.MAIL_OUTLINED,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        border_color="#D1D5DB",
        focused_border_color="#F97316",
        filled=True,
        fill_color="#F9FAFB",
        text_style=ft.TextStyle(size=14, color="#111827"),
        hint_style=ft.TextStyle(color="#9CA3AF", size=14),
        content_padding=ft.Padding(left=16, top=12, right=16, bottom=12),
        height=48,
        expand=True,
        on_change=lambda e: _clear_error(),
    )

    def _clear_error():
        if error_text.value:
            error_text.value = ""
            page.update()

    def send_code(e):
        valor = (email_field.value or "").strip()

        if not valor:
            error_text.value = "Por favor, ingresa tu correo electrónico."
            page.update()
            return

        if not _email_valido(valor):
            error_text.value = "El correo debe tener el formato correcto: usuario@dominio.com"
            email_field.border_color = "#EF4444"
            email_field.focused_border_color = "#EF4444"
            page.update()
            return

        # Email válido — resetear estilos y avanzar
        email_field.border_color = "#D1D5DB"
        email_field.focused_border_color = "#F97316"
        error_text.value = ""
        show_toast(page, f"Código de recuperación enviado a {valor}", "Código Enviado")
        go_verify_code()

    # ── Construir tarjeta ─────────────────────────────────────────────
    def build_card():
        mobile     = is_mobile()
        tablet     = is_tablet()
        card_width = (page.width - 24) if mobile else (460 if tablet else 460)
        pad_h      = 18 if mobile else (28 if tablet else 32)
        pad_v      = 20 if mobile else 28

        email_field.height = 48

        return ft.Container(
            width=card_width,
            padding=ft.Padding(pad_h, pad_v, pad_h, pad_v),
            bgcolor="white",
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=20, spread_radius=1,
                color="#E5E7EB", offset=ft.Offset(0, 10),
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
                controls=[
                    # Encabezado: ícono + título + botón cerrar
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                spacing=14,
                                controls=[
                                    ft.Container(
                                        padding=10,
                                        bgcolor="#FEF3C7",
                                        border_radius=999,
                                        content=ft.Icon(
                                            ft.Icons.LOCK_RESET_ROUNDED,
                                            color="#D97706",
                                            size=24 if mobile else 26,
                                        )
                                    ),
                                    ft.Column(
                                        spacing=4,
                                        controls=[
                                            ft.Text(
                                                "Recuperar tu cuenta",
                                                size=16 if mobile else 18,
                                                weight=ft.FontWeight.BOLD,
                                                color="#111827",
                                            ),
                                            ft.Container(
                                                width=card_width - pad_h * 2 - 80,
                                                content=ft.Text(
                                                    "Ingresa tu correo con el formato correcto para recibir el código.",
                                                    size=12 if mobile else 13,
                                                    color="#6B7280",
                                                )
                                            )
                                        ]
                                    )
                                ]
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE_ROUNDED,
                                icon_color="#9CA3AF",
                                icon_size=22,
                                padding=0,
                                margin=ft.Margin(left=0, top=-8, right=-8, bottom=0),
                                tooltip="Cerrar",
                                on_click=lambda e: go_login(),
                            )
                        ]
                    ),
                    ft.Container(height=24 if mobile else 32),
                    # Label campo
                    ft.Text(
                        "Correo electrónico",
                        size=13 if mobile else 14,
                        weight=ft.FontWeight.W_500,
                        color="#374151",
                    ),
                    ft.Container(height=6),
                    # Campo de email (expand para ocupar todo el ancho)
                    ft.Row(controls=[email_field]),
                    ft.Container(height=6),
                    error_text,
                    ft.Container(height=20 if mobile else 24),
                    # Botones
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                        controls=[
                            ft.OutlinedButton(
                                "Cancelar",
                                style=ft.ButtonStyle(
                                    color="#374151",
                                    bgcolor="white",
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    side=ft.BorderSide(1, "#D1D5DB"),
                                    padding=ft.Padding(
                                        left=14, top=16, right=14, bottom=16),
                                ),
                                height=40,
                                on_click=lambda e: go_login(),
                            ),
                            ft.FilledButton(
                                "Enviar Código",
                                style=ft.ButtonStyle(
                                    bgcolor="#F97316",
                                    color="white",
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.Padding(
                                        left=14, top=16, right=14, bottom=16),
                                ),
                                height=40,
                                on_click=send_code,
                            ),
                        ]
                    )
                ]
            )
        )

    # ── Panel izquierdo (logo) ────────────────────────────────────────
    def build_left_side():
        logo_sz = 260 if is_tablet() else 320
        box_sz  = 300 if is_tablet() else 380
        return ft.Container(
            expand=True,
            bgcolor="#FFF9E6",
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Container(
                        width=box_sz, height=box_sz,
                        bgcolor="white", border_radius=30,
                        shadow=ft.BoxShadow(blur_radius=25, spread_radius=1,
                                            color="#E5E7EB", offset=ft.Offset(0, 10)),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Image(src="img/logo.png",
                                         width=logo_sz, height=logo_sz,
                                         fit="contain"),
                    ),
                    ft.Text("SENA FOOD",
                            size=28 if is_tablet() else 30,
                            weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Text("RECUPERAR CONTRASEÑA", size=14, color="#9CA3AF"),
                ],
            ),
        )

    # ── Root reactivo ─────────────────────────────────────────────────
    root_container = ft.Container(expand=True)

    def build_root():
        mobile = is_mobile()
        if mobile:
            inner = ft.Container(
                expand=True,
                bgcolor="#F3F4F6",
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=20),
                        build_card(),
                        ft.Container(height=20),
                    ],
                ),
            )
        else:
            right = ft.Container(
                expand=True,
                bgcolor="#F3F4F6",
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[build_card()],
                ),
            )
            inner = ft.Row(expand=True, controls=[build_left_side(), right])

        return ft.Container(expand=True, bgcolor="#FDFBF5", content=inner)

    root_container.content = build_root()

    def on_resize(e):
        root_container.content = build_root()
        root_container.update()

    page.on_resize = on_resize

    return root_container