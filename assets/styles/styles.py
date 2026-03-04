import flet as ft
import threading
import time

# Design Tokens - Colors
COLOR_ORANGE_PRIMARY = "#F97316"
COLOR_ORANGE_DARK = "#EA580C"
COLOR_ORANGE_LIGHT = "#FFEDD5"
COLOR_GREEN_SUCCESS = "#16A34A"
COLOR_GREEN_DARK = "#14532D"
COLOR_GREEN_LIGHT = "#DCFCE7"
COLOR_RED_ERROR = "#DC2626"
COLOR_RED_LIGHT = "#FEF2F2"
COLOR_BLUE_INFO = "#2563EB"
COLOR_BLUE_LIGHT = "#EFF6FF"
COLOR_GRAY_DARK = "#1F2937"
COLOR_GRAY_MEDIUM = "#374151"
COLOR_GRAY_LIGHT = "#6B7280"
COLOR_GRAY_TEXT = "#9CA3AF"
COLOR_GRAY_BORDER = "#E5E7EB"
COLOR_BG_LIGHT = "#FAF8F5"
COLOR_BG_PAGE = "#F5F3EE"
COLOR_BG_SIDEBAR = "#F9FAFB"
COLOR_WHITE = "#FFFFFF"


def show_toast(page: ft.Page, message, title=None, type="success"):
    # Select colors based on type
    if type == "success":
        icon = ft.Icons.CHECK_CIRCLE_ROUNDED
        bg_color = COLOR_GREEN_SUCCESS
        text_color = "white"
    elif type == "error":
        icon = ft.Icons.ERROR_OUTLINE_ROUNDED
        bg_color = COLOR_RED_ERROR
        text_color = "white"
    elif type == "warning":
        icon = ft.Icons.WARNING_AMBER_ROUNDED
        bg_color = "#F59E0B"  # Amber 500
        text_color = "white"
    else:
        icon = ft.Icons.INFO_OUTLINE_ROUNDED
        bg_color = COLOR_BLUE_INFO
        text_color = "white"

    if not title:
        title = "Éxito" if type == "success" else "Error" if type == "error" else "Información"

    # Toast card container (versión segura sin updates individuales)
    toast = ft.Container(
        content=ft.Row(
            spacing=12,
            tight=True,
            controls=[
                ft.Icon(icon, color=text_color, size=24),
                ft.Column(
                    spacing=0,
                    tight=True,
                    controls=[
                        ft.Text(title, size=13, weight="bold", color=text_color),
                        ft.Text(
                            message,
                            color=text_color,
                            size=12,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ],
                ),
            ],
        ),
        bgcolor=bg_color,
        padding=ft.Padding(16, 12, 24, 12),
        border_radius=16,
        shadow=ft.BoxShadow(
            spread_radius=-5,
            blur_radius=20,
            color="#60000000",
            offset=ft.Offset(0, 10),
        ),
        offset=ft.Offset(0, 0),
        animate_offset=None,
    )

    # Positioning overlay
    toast_overlay = ft.Container(
        content=toast,
        alignment=ft.Alignment(1, 1),
        padding=ft.Padding(0, 0, 30, 30),
        width=380,
        height=120,
        bottom=0,
        right=0,
    )

    # Clear any existing toasts before showing a new one
    try:
        page.overlay.clear()
        page.overlay.append(toast_overlay)
        page.update()
    except Exception:
        # En versiones antiguas de Flet es más seguro ignorar errores aquí
        return

    # Auto-remove after duration
    def cleanup():
        time.sleep(1.8)
        try:
            if toast_overlay in page.overlay:
                page.overlay.remove(toast_overlay)
                page.update()
        except Exception:
            pass

    threading.Thread(target=cleanup, daemon=True).start()


def info_row(icon, label_text, text):
    return ft.Container(
        bgcolor=COLOR_BG_LIGHT,
        border_radius=12,
        padding=ft.Padding.symmetric(vertical=10, horizontal=20),
        margin=ft.Margin.only(top=4),
        content=ft.Row(
            spacing=14,
            controls=[
                ft.Icon(icon, size=20, color=COLOR_GRAY_TEXT),
                ft.Column(
                    spacing=0,
                    tight=True,
                    controls=[
                        ft.Text(label_text, size=11, color=COLOR_GRAY_TEXT),
                        ft.Text(text, size=14, weight="bold", color=COLOR_GRAY_MEDIUM),
                    ],
                ),
            ],
        ),
    )


def activity_item(title, subtitle, time_text):
    return ft.Container(
        bgcolor=COLOR_BG_LIGHT,
        border_radius=10,
        padding=ft.Padding.symmetric(vertical=14, horizontal=20),
        margin=ft.Margin.only(top=6),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(title, size=14, weight="bold", color=COLOR_GRAY_MEDIUM),
                        ft.Text(subtitle, size=13, color=COLOR_GRAY_TEXT),
                    ],
                ),
                ft.Text(time_text, size=12, color=COLOR_GRAY_TEXT),
            ],
        ),
    )


def stat_card(label, value, value_color=COLOR_ORANGE_PRIMARY):
    return ft.Container(
        bgcolor=COLOR_BG_LIGHT,
        border_radius=12,
        padding=ft.Padding.symmetric(vertical=14, horizontal=20),
        margin=ft.Margin.only(top=8),
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(label, size=13, color=COLOR_GRAY_TEXT),
                ft.Text(value, size=28, weight="bold", color=value_color),
            ],
        ),
    )


def sec_option(
    icon,
    label,
    color=COLOR_GRAY_MEDIUM,
    on_click=None,
    badge_text: str | None = None,
    badge_bg=COLOR_ORANGE_PRIMARY,
    badge_color="white",
):
    controls = [
        ft.Icon(icon, size=18, color=color),
        ft.Text(label, size=15, color=color),
    ]
    if badge_text is not None:
        badge = ft.Container(
            bgcolor=badge_bg,
            border_radius=6,
            padding=ft.Padding.symmetric(vertical=2, horizontal=8),
            content=ft.Text(badge_text, size=11, color=badge_color, weight="bold"),
        )
        controls.append(badge)

    def on_sec_hover(e):
        if e.data == "true":
            e.control.offset = ft.Offset(0.06, 0)
            e.control.scale = 1.02
            e.control.shadow = ft.BoxShadow(
                blur_radius=10, color="#20000000", offset=ft.Offset(0, 5)
            )
        else:
            e.control.offset = ft.Offset(0, 0)
            e.control.scale = 1.0
            e.control.shadow = None
        e.control.update()

    container = ft.Container(
        bgcolor="#FCFAF8" if color != COLOR_RED_ERROR else COLOR_RED_LIGHT,
        border=ft.Border.all(1, "#F3EFEA")
        if color != COLOR_RED_ERROR
        else ft.Border.all(1, "#FECACA"),
        border_radius=12,
        padding=ft.Padding.symmetric(vertical=10, horizontal=16),
        margin=ft.Margin.only(top=6),
        on_click=on_click,
        offset=ft.Offset(0, 0),
        scale=1.0,
        animate_offset=ft.Animation(700, ft.AnimationCurve.EASE_OUT_BACK),
        animate_scale=ft.Animation(700, ft.AnimationCurve.EASE_OUT_BACK),
        on_hover=on_sec_hover,
        content=ft.Row(
            spacing=12,
            alignment=ft.MainAxisAlignment.START,
            controls=controls,
        ),
    )
    return container


def report_stat_card(label, value, subtext=None, trend=None, trend_color=COLOR_GREEN_SUCCESS):
    trend_controls = []
    if trend:
        trend_controls = [
            ft.Row(
                spacing=4,
                controls=[
                    ft.Icon(
                        ft.Icons.TRENDING_UP if trend.startswith("+") else ft.Icons.TRENDING_DOWN,
                        size=14,
                        color=trend_color,
                    ),
                    ft.Text(trend, size=12, weight="600", color=trend_color),
                    ft.Text(
                        "vs período anterior" if "vs" not in trend else "",
                        size=12,
                        color=COLOR_GRAY_TEXT,
                    ),
                ],
            )
        ]
    elif subtext:
        trend_controls = [ft.Text(subtext, size=12, color=COLOR_GRAY_TEXT)]

    return ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=24,
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(label, size=14, color=COLOR_GRAY_TEXT, weight="medium"),
                ft.Text(value, size=32, weight="bold", color=COLOR_GRAY_DARK),
                ft.Column(spacing=2, controls=trend_controls),
            ],
        ),
    )


def chart_bar(label, value_text, percentage, color=COLOR_ORANGE_PRIMARY):
    return ft.Column(
        spacing=8,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(label, size=14, weight="500", color=COLOR_GRAY_DARK),
                    ft.Text(value_text, size=13, weight="bold", color=COLOR_GRAY_DARK),
                ],
            ),
            ft.Container(
                height=8,
                bgcolor="#F3F4F6",
                border_radius=4,
                content=ft.Row(
                    [
                        ft.Container(
                            width=percentage * 2,  # simplificación visual
                            expand=percentage,
                            bgcolor=color,
                            border_radius=4,
                        ),
                        ft.Container(expand=100 - percentage),
                    ]
                ),
            ),
        ],
    )


def filter_pill(label, selected=False, on_click=None):
    def on_hover(e):
        if not e.control.data:  # data almacena el estado 'selected'
            e.control.bgcolor = COLOR_ORANGE_LIGHT if e.data == "true" else "transparent"
            e.control.update()

    return ft.Container(
        padding=ft.Padding(16, 8, 16, 8),
        border_radius=12,
        bgcolor=COLOR_ORANGE_PRIMARY if selected else "transparent",
        border=None if selected else ft.Border.all(1, "#E5E7EB"),
        shadow=ft.BoxShadow(color="#40F97316", blur_radius=6, offset=ft.Offset(0, 2))
        if selected
        else None,
        on_click=on_click,
        on_hover=on_hover,
        data=selected,  # Usa data para el estado de selección
        content=ft.Text(
            label,
            size=13,
            weight="bold" if selected else "medium",
            color="white" if selected else COLOR_GRAY_MEDIUM,
        ),
        animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
    )


def token_card(token_id, status, client, order_info, time_text):
    return ft.Container(
        width=280,
        bgcolor="#FFF7ED",  # Very light orange/peach
        border_radius=16,
        padding=20,
        border=ft.Border.all(1, "#FFEDD5"),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            bgcolor="white",
                            padding=ft.Padding(12, 6, 12, 6),
                            border_radius=8,
                            border=ft.Border.all(1, "#E5E7EB"),
                            content=ft.Text(
                                token_id, weight="bold", size=14, color=COLOR_GRAY_DARK
                            ),
                        ),
                        ft.Container(
                            bgcolor="#FFEDD5",  # Badge bg
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=6,
                            content=ft.Text(
                                status,
                                size=10,
                                weight="bold",
                                color=COLOR_ORANGE_PRIMARY,
                            ),
                        ),
                    ],
                ),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Cliente", size=10, color=COLOR_GRAY_TEXT),
                        ft.Text(client, size=13, weight="bold", color=COLOR_GRAY_MEDIUM),
                    ],
                ),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Pedido", size=10, color=COLOR_GRAY_TEXT),
                        ft.Row(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    order_info,
                                    size=13,
                                    weight="bold",
                                    color=COLOR_GRAY_MEDIUM,
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Hora", size=10, color=COLOR_GRAY_TEXT),
                        ft.Text(
                            time_text, size=13, weight="bold", color=COLOR_GRAY_MEDIUM
                        ),
                    ],
                ),
            ],
        ),
    )


def order_status_badge(status: str):
    colors = {
        "Completado": (COLOR_GREEN_LIGHT, COLOR_GREEN_SUCCESS),
        "Confirmado": (COLOR_BLUE_LIGHT, COLOR_BLUE_INFO),
        "Pendiente": (COLOR_ORANGE_LIGHT, COLOR_ORANGE_PRIMARY),
        "Cancelado": (COLOR_RED_LIGHT, COLOR_RED_ERROR),
    }
    bg, fg = colors.get(status, ("#F3F4F6", COLOR_GRAY_DARK))

    return ft.Container(
        content=ft.Text(status, size=11, weight="bold", color=fg),
        bgcolor=bg,
        padding=ft.Padding(12, 5, 12, 5),
        border_radius=20,
        alignment=ft.Alignment.CENTER,
    )


def order_stat_box(label: str, count: str, icon: str, color: str):
    # Light icon background tint
    icon_bg = {
        COLOR_ORANGE_PRIMARY: "#FFF7ED",
        COLOR_GREEN_SUCCESS: "#F0FDF4",
        COLOR_BLUE_INFO: "#EFF6FF",
        COLOR_RED_ERROR: "#FEF2F2",
    }.get(color, "#F9FAFB")

    return ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=ft.Padding(20, 18, 20, 18),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=48,
                    height=48,
                    bgcolor=icon_bg,
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(icon, color=color, size=22),
                ),
                ft.Column(
                    spacing=2,
                    tight=True,
                    controls=[
                        ft.Text(count, size=26, weight="bold", color=COLOR_GRAY_DARK),
                        ft.Text(label, size=13, color=COLOR_GRAY_TEXT),
                    ],
                ),
            ],
        ),
    )


def _show_status_toast(page: ft.Page, message: str):
    """Tarjeta blanca tipo toast en la esquina inferior derecha."""
    toast_content = ft.Container(
        bgcolor=COLOR_WHITE,
        border_radius=12,
        padding=ft.Padding(16, 12, 20, 12),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color="#25000000",
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            spacing=10,
            tight=True,
            controls=[
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE_ROUNDED,
                    color=COLOR_GREEN_SUCCESS,
                    size=20,
                ),
                ft.Text(message, size=13, weight="w600", color=COLOR_GRAY_DARK),
            ],
        ),
        offset=ft.Offset(0, 0.3),
        opacity=0,
        animate_offset=ft.Animation(350, ft.AnimationCurve.EASE_OUT),
        animate_opacity=ft.Animation(350, ft.AnimationCurve.EASE_OUT),
    )

    overlay = ft.Container(
        content=toast_content,
        alignment=ft.Alignment.BOTTOM_RIGHT,
        padding=ft.Padding(0, 0, 24, 24),
        bottom=0,
        right=0,
        width=280,
        height=80,
    )

    page.overlay.clear()
    page.overlay.append(overlay)
    page.update()

    toast_content.offset = ft.Offset(0, 0)
    toast_content.opacity = 1
    toast_content.update()

    def cleanup():
        import time as _time

        _time.sleep(2.2)
        try:
            toast_content.opacity = 0
            toast_content.offset = ft.Offset(0, 0.3)
            toast_content.update()
            _time.sleep(0.35)
            if overlay in page.overlay:
                page.overlay.remove(overlay)
                page.update()
        except:
            pass

    import threading as _threading

    _threading.Thread(target=cleanup, daemon=True).start()


def order_table_row(
    order_id,
    token,
    client,
    doc,
    date,
    time_str,
    total,
    status,
    show_complete=False,
    page: ft.Page | None = None,
    on_view=None,
    on_status_change=None,
):
    """
    Fila para la tabla de pedidos.
    - show_complete=True  → muestra el botón verde \"Completar\"
    - on_view: callback opcional para el botón de ver detalle
    """

    status_ref = ft.Ref[ft.Container]()
    complete_btn_ref = ft.Ref[ft.Container]()
    current_status = [status]  # mutable cell

    def on_complete(e):
        # Avanza estado: Pendiente/Confirmado → Completado
        current_status[0] = "Completado"
        # Actualiza badge
        status_badge = order_status_badge(current_status[0])
        status_ref.current.content = status_badge.content
        status_ref.current.bgcolor = status_badge.bgcolor
        status_ref.current.update()
        # Oculta botón completar
        complete_btn_ref.current.visible = False
        complete_btn_ref.current.update()
        # Toast blanco
        if page:
            _show_status_toast(page, "Pedido completado")
        # Notifica al exterior (vista de pedidos) para que actualice su modelo
        if on_status_change:
            try:
                on_status_change(current_status[0])
            except Exception:
                # Evita que un error externo rompa la interacción del usuario
                pass

    def on_view_click(e):
        if on_view:
            on_view(
                {
                    "order_id": order_id,
                    "token": token,
                    "client": client,
                    "doc": doc,
                    "date": date,
                    "time": time_str,
                    "total": total,
                    "status": current_status[0],
                }
            )

    return ft.Container(
        padding=ft.Padding(20, 14, 20, 14),
        border=ft.Border(bottom=ft.BorderSide(1, "#F3F4F6")),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # ID & Token
                ft.Container(
                    width=170,
                    content=ft.Column(
                        [
                            ft.Text(
                                order_id,
                                weight="bold",
                                size=13,
                                color=COLOR_GRAY_DARK,
                            ),
                            ft.Row(
                                [
                                    ft.Text("token:", size=11, color=COLOR_GRAY_TEXT),
                                    ft.Text(
                                        token,
                                        size=11,
                                        weight="bold",
                                        color=COLOR_ORANGE_PRIMARY,
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=2,
                        tight=True,
                    ),
                ),
                # Cliente
                ft.Container(
                    width=190,
                    content=ft.Column(
                        [
                            ft.Text(
                                client,
                                weight="bold",
                                size=13,
                                color=COLOR_GRAY_DARK,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.DESCRIPTION_OUTLINED,
                                        size=11,
                                        color=COLOR_GRAY_TEXT,
                                    ),
                                    ft.Text(doc, size=11, color=COLOR_GRAY_TEXT),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=2,
                        tight=True,
                    ),
                ),
                # Fecha / Hora
                ft.Container(
                    width=160,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.CALENDAR_MONTH_OUTLINED,
                                        size=13,
                                        color=COLOR_RED_ERROR,
                                    ),
                                    ft.Text(
                                        date,
                                        size=12,
                                        weight="w500",
                                        color=COLOR_GRAY_MEDIUM,
                                    ),
                                ],
                                spacing=4,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.ACCESS_TIME_OUTLINED,
                                        size=12,
                                        color=COLOR_GRAY_TEXT,
                                    ),
                                    ft.Text(
                                        time_str,
                                        size=12,
                                        color=COLOR_GRAY_TEXT,
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=3,
                        tight=True,
                    ),
                ),
                # Total
                ft.Container(
                    width=100,
                    content=ft.Text(
                        total, weight="bold", size=14, color=COLOR_ORANGE_PRIMARY
                    ),
                ),
                # Estado  (badge actualizable)
                ft.Container(
                    ref=status_ref,
                    width=120,
                    bgcolor=order_status_badge(status).bgcolor,
                    padding=ft.Padding(12, 5, 12, 5),
                    border_radius=20,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        status,
                        size=11,
                        weight="bold",
                        color=order_status_badge(status).content.color,
                    ),
                ),
                # Acciones
                ft.Container(
                    width=160,
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.VISIBILITY_OUTLINED,
                                            size=15,
                                            color=COLOR_GRAY_MEDIUM,
                                        ),
                                        ft.Text(
                                            "Ver",
                                            size=12,
                                            weight="bold",
                                            color=COLOR_GRAY_MEDIUM,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                bgcolor="#F3F4F6",
                                padding=ft.Padding(10, 6, 10, 6),
                                border_radius=8,
                                on_click=on_view_click,
                            ),
                            ft.Container(
                                ref=complete_btn_ref,
                                content=ft.Text(
                                    "Completar",
                                    size=12,
                                    weight="bold",
                                    color="white",
                                ),
                                bgcolor=COLOR_GREEN_SUCCESS,
                                padding=ft.Padding(10, 6, 10, 6),
                                border_radius=8,
                                visible=show_complete,
                                on_click=on_complete,
                            ),
                        ],
                        spacing=8,
                    ),
                ),
            ],
        ),
    )

