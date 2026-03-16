import flet as ft
from views.styles import show_toast


def verify_code_view(page: ft.Page, go_login, go_reset_password):
    """Segunda vista del flujo de recuperación: ingreso del código enviado."""

    error_text = ft.Text("", size=12, color="red")

    # ── Helpers de tamaño ────────────────────────────────────────────
    def is_mobile():
        return page.width is not None and page.width < 700

    def is_tablet():
        return page.width is not None and 700 <= page.width < 1100

    # ── Campos de código ─────────────────────────────────────────────
    # Se crean primero como lista vacía, luego se puebla
    inputs = []

    def make_input(index):
        def on_change(e):
            raw = e.control.value or ""

            # Filtrar solo dígitos
            digits = "".join(c for c in raw if c.isdigit())

            # Caso: pegaron varios dígitos de golpe
            if len(digits) > 1:
                for offset, d in enumerate(digits):
                    if index + offset < 6:
                        inputs[index + offset].value = d
                # Actualizar UI con todos los valores
                page.update()
                # Enfocar el campo después del último llenado
                next_idx = min(index + len(digits), 5)
                inputs[next_idx].focus()
                page.update()
                _update_counter()
                page.update()
                return

            # Caso: un solo dígito escrito normalmente
            if len(digits) == 1:
                e.control.value = digits
                _update_counter()
                page.update()                  # 1. renderizar el dígito
                if index < 5:
                    inputs[index + 1].focus()  # 2. mover foco
                    page.update()              # 3. aplicar el foco
                return

            # Caso: campo borrado (digits == "")
            e.control.value = ""
            _update_counter()
            page.update()
            if index > 0:
                inputs[index - 1].focus()
                page.update()

        sz = 38 if is_mobile() else 48
        return ft.TextField(
            width=sz,
            height=sz + 4,
            text_size=15 if is_mobile() else 18,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            border_color="#D1D5DB",
            focused_border_color="#F97316",
            filled=True,
            fill_color="#F9FAFB",
            content_padding=0,
            on_change=on_change,
        )

    # Poblar la lista de inputs
    for i in range(6):
        inputs.append(make_input(i))

    digit_counter = ft.Text("0/6 dígitos ingresados", size=12, color="#9CA3AF")

    def _update_counter():
        count = sum(1 for inp in inputs if inp.value)
        digit_counter.value = f"{count}/6 dígitos ingresados"
        verify_button.style.bgcolor = "#22C55E" if count == 6 else "#91D1A6"

    def verify_code(e):
        full_code = "".join([i.value for i in inputs])
        if len(full_code) < 6:
            error_text.value = "Por favor, ingresa el código de 6 dígitos."
            page.update()
            return
        show_toast(page, "Código verificado correctamente", "Acceso concedido")
        go_reset_password()

    verify_button = ft.FilledButton(
        "Verificar Código",
        style=ft.ButtonStyle(
            bgcolor="#91D1A6",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=verify_code,
    )

    # ── Botón volver ─────────────────────────────────────────────────
    def build_back_button():
        return ft.Container(
            padding=ft.Padding(0, 0, 0, 8),
            ink=True,
            on_click=lambda e: go_login(),
            content=ft.Row(
                spacing=4,
                controls=[
                    ft.Icon(ft.Icons.ARROW_BACK_IOS_ROUNDED,
                            size=14, color="#9CA3AF"),
                    ft.Text("Volver", size=13, color="#9CA3AF",
                            weight=ft.FontWeight.W_500),
                ],
            ),
        )

    # ── Tarjeta principal ─────────────────────────────────────────────
    def build_card():
        mobile      = is_mobile()
        tablet      = is_tablet()
        card_width  = (page.width - 24) if mobile else (480 if tablet else 460)
        pad_h       = 18 if mobile else (28 if tablet else 32)
        pad_v       = 18 if mobile else 24
        title_size  = 20 if mobile else 24
        code_size   = 30 if mobile else 40
        box_width   = min((page.width or 400) - 56, 320) if mobile else 320
        inner_width = min((page.width or 400) - 48, 340) if mobile else 340

        inp_sz = 38 if mobile else 48
        for inp in inputs:
            inp.width     = inp_sz
            inp.height    = inp_sz + 4
            inp.text_size = 15 if mobile else 18

        verify_button.width  = card_width - pad_h * 2
        verify_button.height = 46

        return ft.Container(
            width=card_width,
            padding=ft.Padding(pad_h, pad_v, pad_h, pad_v),
            bgcolor="white",
            border_radius=14,
            shadow=ft.BoxShadow(
                blur_radius=20, spread_radius=1,
                color="#E5E7EB", offset=ft.Offset(0, 10),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[build_back_button()],
                    ),
                    ft.Container(height=4),
                    ft.Container(
                        padding=12, bgcolor="#E6F4EA", border_radius=14,
                        content=ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED,
                                        color="#34A853",
                                        size=26 if mobile else 30),
                    ),
                    ft.Container(height=12 if mobile else 16),
                    ft.Text("Código de Verificación",
                            size=title_size, weight=ft.FontWeight.BOLD,
                            color="#1E293B", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=4),
                    ft.Text("Revisa tu correo e ingresa el código",
                            size=12 if mobile else 14, color="#64748B",
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10 if mobile else 14),
                    # Email pill
                    ft.Container(
                        bgcolor="#F8FAFC", border_radius=10,
                        padding=ft.Padding(14, 8, 14, 8),
                        width=inner_width,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER, spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.MAIL_OUTLINE_ROUNDED,
                                        color="#64748B", size=15),
                                ft.Text("admin@senafood.com", color="#334155",
                                        size=13, weight=ft.FontWeight.W_500),
                            ]
                        )
                    ),
                    ft.Container(height=14 if mobile else 20),
                    # Panel demo
                    ft.Container(
                        width=inner_width,
                        bgcolor="#F0F7FF",
                        border=ft.Border.all(1, "#BFDBFE"),
                        border_radius=12,
                        padding=10,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER, spacing=6,
                                    controls=[
                                        ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED,
                                                color="#2563EB", size=16),
                                        ft.Text("CÓDIGO RECIBIDO EN TU EMAIL",
                                                size=11 if mobile else 12,
                                                weight=ft.FontWeight.BOLD,
                                                color="#1E40AF"),
                                    ]
                                ),
                                ft.Container(
                                    bgcolor="white", padding=8, border_radius=10,
                                    border=ft.Border.all(1, "#E2E8F0"),
                                    width=box_width,
                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=6,
                                        controls=[
                                            ft.Text("Código de verificación:",
                                                    size=11, color="#64748B"),
                                            ft.Container(
                                                bgcolor="#2563EB", border_radius=8,
                                                padding=ft.Padding(14, 10, 14, 10),
                                                content=ft.Text(
                                                    "4 6 6 9 6 9",
                                                    size=code_size,
                                                    weight=ft.FontWeight.W_900,
                                                    color="white",
                                                ),
                                            )
                                        ]
                                    )
                                ),
                                ft.Container(
                                    bgcolor="#FEFCE8",
                                    border=ft.Border.all(1, "#FDE047"),
                                    border_radius=8, padding=8,
                                    width=box_width,
                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=2,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                spacing=6,
                                                controls=[
                                                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED,
                                                            size=13, color="#854D0E"),
                                                    ft.Text("COPIA ESTE CÓDIGO ABAJO",
                                                            size=11,
                                                            weight=ft.FontWeight.BOLD,
                                                            color="#854D0E"),
                                                ]
                                            ),
                                            ft.Text("En producción llegaría a tu correo",
                                                    size=10, color="#A16207"),
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                    ft.Container(height=14 if mobile else 20),
                    ft.Text("Ingresa el Código Aquí",
                            size=13 if mobile else 14,
                            color="#475569", weight=ft.FontWeight.W_500),
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6 if mobile else 8,
                        controls=inputs,
                    ),
                    ft.Container(height=8),
                    digit_counter,
                    ft.Container(height=6),
                    error_text,
                    ft.Container(height=14 if mobile else 18),
                    verify_button,
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=2, wrap=True,
                        controls=[
                            ft.Text("¿No recibiste el código?",
                                    size=12 if mobile else 13, color="#64748B"),
                            ft.TextButton(
                                "Reenviar código",
                                style=ft.ButtonStyle(color="#F97316"),
                                on_click=lambda e: show_toast(
                                    page, "Reenviando código...", "Solicitud enviada"),
                            ),
                        ]
                    ),
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
                    ft.Text("VERIFICACIÓN DE CÓDIGO", size=14, color="#9CA3AF"),
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
                        ft.Container(height=16),
                        build_card(),
                        ft.Container(height=16),
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
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=20),
                        build_card(),
                        ft.Container(height=20),
                    ],
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