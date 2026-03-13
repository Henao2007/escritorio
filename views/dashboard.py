import flet as ft
from views.styles import (
    COLOR_ORANGE_PRIMARY, COLOR_ORANGE_LIGHT, COLOR_ORANGE_DARK,
    COLOR_GREEN_SUCCESS, COLOR_GREEN_LIGHT,
    COLOR_BLUE_INFO, COLOR_BLUE_LIGHT,
    COLOR_RED_ERROR, COLOR_RED_LIGHT,
    COLOR_GRAY_DARK, COLOR_GRAY_MEDIUM, COLOR_GRAY_TEXT,
    COLOR_GRAY_BORDER, COLOR_BG_PAGE, COLOR_BG_LIGHT, COLOR_WHITE,
)
from controllers.dashboard import DashboardController


# ─── Helper widgets ───────────────────────────────────────────────────────────

def _stat_card(title: str, value: str, icon: str, icon_color: str,
               subtitle=None, subtitle_icon=None, subtitle_color=None):
    subtitle_row = []
    if subtitle:
        sub_controls = []
        if subtitle_icon:
            sub_controls.append(
                ft.Icon(subtitle_icon, size=13, color=subtitle_color or COLOR_GREEN_SUCCESS)
            )
        sub_controls.append(
            ft.Text(subtitle, size=12, color=subtitle_color or COLOR_GREEN_SUCCESS, weight="w500")
        )
        subtitle_row = [ft.Row(sub_controls, spacing=4, tight=True)]

    return ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=ft.Padding(20, 18, 20, 18),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(title, size=13, color=COLOR_GRAY_TEXT, weight="w500"),
                        ft.Icon(icon, color=icon_color, size=22),
                    ],
                ),
                ft.Text(value, size=28, weight="bold", color=COLOR_GRAY_DARK),
                *subtitle_row,
            ],
        ),
    )


def _order_badge(status: str):
    colors = {
        "Completado": (COLOR_GREEN_LIGHT,  COLOR_GREEN_SUCCESS),
        "Pendiente":  (COLOR_ORANGE_LIGHT, COLOR_ORANGE_PRIMARY),
        "Cancelado":  (COLOR_RED_LIGHT,    COLOR_RED_ERROR),
        "Confirmado": (COLOR_BLUE_LIGHT,   COLOR_BLUE_INFO),
    }
    bg, fg = colors.get(status, ("#F3F4F6", COLOR_GRAY_DARK))
    return ft.Container(
        bgcolor=bg,
        border_radius=20,
        padding=ft.Padding(10, 3, 10, 3),
        content=ft.Text(status, size=11, weight="bold", color=fg),
    )


def _recent_order_row(order_id: str, status: str, client: str, meta: str, total: str):
    return ft.Container(
        bgcolor=COLOR_BG_LIGHT,
        border_radius=12,
        padding=ft.Padding(16, 12, 16, 12),
        margin=ft.Margin(0, 0, 0, 8),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=4, tight=True, expand=True,
                    controls=[
                        ft.Row(
                            spacing=8, tight=True,
                            controls=[
                                ft.Text(order_id, size=13, weight="bold", color=COLOR_GRAY_DARK),
                                _order_badge(status),
                            ],
                        ),
                        ft.Text(client, size=13, weight="w500", color=COLOR_GRAY_MEDIUM),
                        ft.Text(meta,   size=11, color=COLOR_GRAY_TEXT),
                    ],
                ),
                ft.Text(total, size=14, weight="bold", color=COLOR_ORANGE_PRIMARY),
            ],
        ),
    )


def _status_stat(icon: str, color: str, count: str, label: str):
    icon_bg = {
        COLOR_ORANGE_PRIMARY: "#FFF7ED",
        COLOR_GREEN_SUCCESS:  "#F0FDF4",
        COLOR_RED_ERROR:      "#FEF2F2",
        COLOR_BLUE_INFO:      "#EFF6FF",
    }.get(color, "#F9FAFB")

    return ft.Container(
        bgcolor=COLOR_BG_LIGHT,
        border_radius=12,
        padding=ft.Padding(16, 14, 16, 14),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=46, height=46, bgcolor=icon_bg,
                    border_radius=23, alignment=ft.Alignment.CENTER,
                    content=ft.Icon(icon, color=color, size=22),
                ),
                ft.Column(
                    spacing=2, tight=True,
                    controls=[
                        ft.Text(count, size=26, weight="bold", color=COLOR_GRAY_DARK),
                        ft.Text(label, size=13, color=COLOR_GRAY_TEXT),
                    ],
                ),
            ],
        ),
    )


# ─── Main view ────────────────────────────────────────────────────────────────

def dashboard_view(page: ft.Page = None):
    if page:
        page.bgcolor = COLOR_BG_PAGE
        page.padding = 0
        page.update()

    # ── Cargar datos reales desde la BD ──────────────────────────────
    ok, msg = DashboardController.cargar_dashboard(page)
    if not ok:
        print(f"[dashboard_view] {msg}")
        page.dashboard_data = {
            "ingresos_hoy":      0.0,
            "contadores":        {"total": 0, "pendiente": 0, "completado": 0, "cancelado": 0, "confirmado": 0},
            "pedidos_recientes": [],
        }

    data       = getattr(page, "dashboard_data", {})
    contadores = data.get("contadores", {})
    recientes  = data.get("pedidos_recientes", [])
    ingresos   = data.get("ingresos_hoy", 0.0)

    # ── Formatear ingresos ────────────────────────────────────────────
    ingresos_fmt = f"$ {ingresos:,.0f}".replace(",", ".")

    # ── Subtítulo de pedidos totales ──────────────────────────────────
    total       = contadores.get("total", 0)
    completados = contadores.get("completado", 0)
    pendientes  = contadores.get("pendiente", 0)
    cancelados  = contadores.get("cancelado", 0)
    subtitulo_pedidos = f"✓ {completados}  ◷ {pendientes}"

    # ── Top stat cards ────────────────────────────────────────────────
    top_cards = ft.Row(
        spacing=16, expand=True,
        controls=[
            _stat_card(
                "Ingresos Hoy", ingresos_fmt,
                ft.Icons.ATTACH_MONEY_ROUNDED, COLOR_GREEN_SUCCESS,
                subtitle="Última actualización: ahora",
                subtitle_color=COLOR_GRAY_TEXT,
            ),
            _stat_card(
                "Pedidos Totales", str(total),
                ft.Icons.RECEIPT_LONG_OUTLINED, COLOR_BLUE_INFO,
                subtitle=subtitulo_pedidos,
                subtitle_color=COLOR_GRAY_TEXT,
            ),
        ],
    )

    # ── Pedidos recientes desde la BD ────────────────────────────────
    def _build_recent_rows():
        rows = []
        for p in recientes:
            estado_raw = (p.get("estado") or "pendiente").lower()
            estado_ui  = estado_raw.capitalize()
            num_items  = int(p.get("num_items") or 0)
            hora       = p.get("hora") or ""
            meta       = f"{num_items} item{'s' if num_items != 1 else ''} • {hora}"
            total_fmt  = f"$ {float(p.get('total') or 0):,.0f}".replace(",", ".")
            rows.append(_recent_order_row(
                p.get("codigo", ""),
                estado_ui,
                p.get("cliente_nombre", ""),
                meta,
                total_fmt,
            ))
        if not rows:
            rows.append(ft.Text("Sin pedidos recientes", size=13, color=COLOR_GRAY_TEXT))
        return rows

    recent_orders_panel = ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=ft.Padding(22, 20, 22, 20),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Text("Pedidos Recientes", size=16, weight="bold", color=COLOR_GRAY_DARK),
                ft.Container(height=14),
                *_build_recent_rows(),
            ],
        ),
    )

    # ── Estado de pedidos desde la BD ────────────────────────────────
    status_panel = ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=ft.Padding(22, 20, 22, 20),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Text("Estado de Pedidos", size=16, weight="bold", color=COLOR_GRAY_DARK),
                ft.Container(height=2),
                _status_stat(ft.Icons.SCHEDULE_OUTLINED,    COLOR_ORANGE_PRIMARY, str(pendientes),  "Pendientes"),
                _status_stat(ft.Icons.CHECK_CIRCLE_OUTLINE, COLOR_GREEN_SUCCESS,  str(completados), "Completados"),
                _status_stat(ft.Icons.CANCEL_OUTLINED,      COLOR_RED_ERROR,      str(cancelados),  "Cancelados"),
            ],
        ),
    )

    middle_row = ft.Row(
        spacing=20, expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[recent_orders_panel, status_panel],
    )

    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_PAGE,
        padding=ft.Padding(32, 28, 32, 28),
        content=ft.Column(
            expand=True, spacing=24,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(spacing=4, controls=[
                    ft.Text("Dashboard", size=26, weight="bold", color=COLOR_GRAY_DARK),
                    ft.Text(
                        "Bienvenido al panel de administración de SENA FOOD",
                        size=14, color=COLOR_GRAY_TEXT,
                    ),
                ]),
                top_cards,
                middle_row,
            ],
        ),
    )