import flet as ft
from views.styles import (
    COLOR_ORANGE_PRIMARY, COLOR_ORANGE_LIGHT, COLOR_ORANGE_DARK,
    COLOR_GREEN_SUCCESS, COLOR_GREEN_LIGHT,
    COLOR_BLUE_INFO, COLOR_BLUE_LIGHT,
    COLOR_RED_ERROR, COLOR_RED_LIGHT,
    COLOR_GRAY_DARK, COLOR_GRAY_MEDIUM, COLOR_GRAY_TEXT,
    COLOR_GRAY_BORDER, COLOR_BG_PAGE, COLOR_BG_LIGHT, COLOR_WHITE,
)

# ─── Sample data ──────────────────────────────────────────────────────────────
RECENT_ORDERS = [
    ("ORD-1247", "Pendiente",  "Juan Pérez",    "2 items • 10:30 AM", "$ 18.500"),
    ("ORD-1246", "Completado", "María García",  "1 items • 10:15 AM", "$ 12.000"),
    ("ORD-1245", "Completado", "Carlos Ruiz",   "3 items • 10:00 AM", "$ 24.500"),
    ("ORD-1244", "Pendiente",  "Ana López",     "1 items • 9:45 AM",  "$ 9.500"),
    ("ORD-1243", "Completado", "Pedro Gómez",   "2 items • 9:30 AM",  "$ 15.000"),
]

TOP_PRODUCTS = [
    (1, "Almuerzo Completo", "45 unidades vendidas", "$ 540.000"),
    (2, "Bandeja Paisa",     "32 unidades vendidas", "$ 480.000"),
    (3, "Pollo al Horno",    "26 unidades vendidas", "$ 336.000"),
    (4, "Carne Asada",       "25 unidades vendidas", "$ 375.000"),
    (5, "Pescado Frito",     "18 unidades vendidas", "$ 252.000"),
]


# ─── Helper widgets ───────────────────────────────────────────────────────────

def _stat_card(title: str, value: str, icon: str, icon_color: str,
               subtitle=None, subtitle_icon=None, subtitle_color=None):
    """Top-row stat card (Ingresos, Pedidos, Productos)."""
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
                # Icon top-right row
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(title, size=13, color=COLOR_GRAY_TEXT, weight="w500"),
                        ft.Icon(icon, color=icon_color, size=22),
                    ],
                ),
                # Big value
                ft.Text(value, size=28, weight="bold", color=COLOR_GRAY_DARK),
                # Subtitle / sub-row
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
                # Left: ID + badge + client + meta
                ft.Column(
                    spacing=4,
                    tight=True,
                    expand=True,
                    controls=[
                        ft.Row(
                            spacing=8,
                            tight=True,
                            controls=[
                                ft.Text(order_id, size=13, weight="bold", color=COLOR_GRAY_DARK),
                                _order_badge(status),
                            ],
                        ),
                        ft.Text(client, size=13, weight="w500", color=COLOR_GRAY_MEDIUM),
                        ft.Text(meta,   size=11, color=COLOR_GRAY_TEXT),
                    ],
                ),
                # Right: total
                ft.Text(total, size=14, weight="bold", color=COLOR_ORANGE_PRIMARY),
            ],
        ),
    )


def _top_product_row(rank: int, name: str, units: str, revenue: str):
    return ft.Container(
        bgcolor=COLOR_BG_LIGHT,
        border_radius=12,
        padding=ft.Padding(14, 12, 14, 12),
        margin=ft.Margin(0, 0, 0, 8),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Rank circle
                ft.Container(
                    width=36,
                    height=36,
                    bgcolor=COLOR_ORANGE_PRIMARY,
                    border_radius=18,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(f"#{rank}", size=11, weight="bold", color="white"),
                ),
                ft.Container(width=12),
                # Name + units
                ft.Column(
                    spacing=2,
                    tight=True,
                    expand=True,
                    controls=[
                        ft.Text(name,  size=13, weight="bold",   color=COLOR_GRAY_DARK),
                        ft.Text(units, size=11, color=COLOR_GRAY_TEXT),
                    ],
                ),
                # Revenue
                ft.Text(revenue, size=13, weight="bold", color=COLOR_GRAY_DARK),
            ],
        ),
    )


def _status_stat(icon: str, color: str, count: str, label: str):
    """Bottom 'Estado de Pedidos' box."""
    icon_bg = {
        COLOR_ORANGE_PRIMARY: "#FFF7ED",
        COLOR_GREEN_SUCCESS:  "#F0FDF4",
        COLOR_RED_ERROR:      "#FEF2F2",
        COLOR_BLUE_INFO:      "#EFF6FF",
    }.get(color, "#F9FAFB")

    return ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=ft.Padding(22, 18, 22, 18),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=46,
                    height=46,
                    bgcolor=icon_bg,
                    border_radius=23,
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


# ─── Main view ────────────────────────────────────────────────────────────────

def dashboard_view(page: ft.Page = None):

    # ── Top stat cards ────────────────────────────────────────────────────────
    top_cards = ft.Row(
        spacing=16,
        expand=True,
        controls=[
            _stat_card(
                "Ingresos Totales", "$ 2.850.000",
                ft.Icons.ATTACH_MONEY_ROUNDED, COLOR_ORANGE_PRIMARY,
                subtitle="+12.5% vs mes anterior",
                subtitle_icon=ft.Icons.TRENDING_UP_ROUNDED,
                subtitle_color=COLOR_GREEN_SUCCESS,
            ),
            _stat_card(
                "Ingresos Hoy", "$ 425.000",
                ft.Icons.ATTACH_MONEY_ROUNDED, COLOR_GREEN_SUCCESS,
                subtitle="Última actualización: ahora",
                subtitle_color=COLOR_GRAY_TEXT,
            ),
            _stat_card(
                "Pedidos Totales", "156",
                ft.Icons.RECEIPT_LONG_OUTLINED, COLOR_BLUE_INFO,
                subtitle="✓ 142  ◷ 8",
                subtitle_color=COLOR_GRAY_TEXT,
            ),
            _stat_card(
                "Productos Activos", "24",
                ft.Icons.RESTAURANT_MENU_ROUNDED, COLOR_GRAY_TEXT,
                subtitle="En menú disponible",
                subtitle_color=COLOR_GRAY_TEXT,
            ),
        ],
    )

    # ── Recent orders panel ───────────────────────────────────────────────────
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
                *[_recent_order_row(*o) for o in RECENT_ORDERS],
            ],
        ),
    )

    # ── Top products panel ────────────────────────────────────────────────────
    top_products_panel = ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=ft.Padding(22, 20, 22, 20),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Text("Productos Más Vendidos", size=16, weight="bold", color=COLOR_GRAY_DARK),
                ft.Container(height=14),
                *[_top_product_row(*p) for p in TOP_PRODUCTS],
            ],
        ),
    )

    # ── Middle row (orders + products side by side) ───────────────────────────
    middle_row = ft.Row(
        spacing=20,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[recent_orders_panel, top_products_panel],
    )

    # ── Bottom status row ─────────────────────────────────────────────────────
    status_section = ft.Container(
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=ft.Padding(22, 20, 22, 20),
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Text("Estado de Pedidos", size=16, weight="bold", color=COLOR_GRAY_DARK),
                ft.Row(
                    spacing=16,
                    expand=True,
                    controls=[
                        _status_stat(ft.Icons.SCHEDULE_OUTLINED,       COLOR_ORANGE_PRIMARY, "8",   "Pendientes"),
                        _status_stat(ft.Icons.CHECK_CIRCLE_OUTLINE,    COLOR_GREEN_SUCCESS,  "142", "Completados"),
                        _status_stat(ft.Icons.CANCEL_OUTLINED,         COLOR_RED_ERROR,      "6",   "Cancelados"),
                    ],
                ),
            ],
        ),
    )

    # ── Full page layout ──────────────────────────────────────────────────────
    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_PAGE,
        padding=ft.Padding(32, 28, 32, 28),
        content=ft.Column(
            expand=True,
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                # Header
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Dashboard", size=26, weight="bold", color=COLOR_GRAY_DARK),
                        ft.Text(
                            "Bienvenido al panel de administración de SENA FOOD",
                            size=14,
                            color=COLOR_GRAY_TEXT,
                        ),
                    ],
                ),

                # Top stat cards
                top_cards,

                # Middle: recent orders + top products
                middle_row,

                # Bottom: status summary
                status_section,
            ],
        ),
    )