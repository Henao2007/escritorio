import flet as ft
from views.styles import (
    COLOR_ORANGE_PRIMARY,
    COLOR_ORANGE_LIGHT,
    COLOR_GRAY_DARK,
    COLOR_GRAY_MEDIUM,
    COLOR_GRAY_TEXT,
    COLOR_GRAY_BORDER,
    COLOR_WHITE,
    COLOR_BG_PAGE,
    COLOR_GREEN_SUCCESS,
    COLOR_BLUE_INFO,
    COLOR_RED_ERROR,
    order_stat_box,
    order_table_row,
)

SAMPLE_ORDERS = [
    ("PED-001", "TK-4821", "María García",    "CC 1234567",  "28 Feb 2025", "09:30", "$45.000", "Completado", False),
    ("PED-002", "TK-4822", "Carlos López",    "CC 9876543",  "28 Feb 2025", "10:15", "$78.500", "Pendiente",  True),
    ("PED-003", "TK-4823", "Ana Martínez",    "CC 5551234",  "28 Feb 2025", "11:00", "$32.000", "Confirmado", True),
    ("PED-004", "TK-4824", "Pedro Rodríguez", "CC 7778899",  "27 Feb 2025", "14:30", "$91.000", "Completado", False),
    ("PED-005", "TK-4825", "Laura Sánchez",   "CC 3334455",  "27 Feb 2025", "16:45", "$55.500", "Cancelado",  False),
    ("PED-006", "TK-4826", "José Torres",     "CC 6667788",  "27 Feb 2025", "17:20", "$23.000", "Pendiente",  True),
]


def pedidos_view(page: ft.Page):
    rows_col = ft.Ref[ft.Column]()
    modal_layer = ft.Ref[ft.Stack]()

    orders = [
        {
            "order_id": o[0],
            "token": o[1],
            "client": o[2],
            "doc": o[3],
            "date": o[4],
            "time": o[5],
            "total": o[6],
            "status": o[7],
            "show_complete": o[8],
        }
        for o in SAMPLE_ORDERS
    ]

    search_state = {"value": ""}

    def close_modal(e=None):
        if modal_layer.current and len(modal_layer.current.controls) > 1:
            modal_layer.current.controls = modal_layer.current.controls[:1]
            modal_layer.current.update()

    def _order_detail_modal(order: dict, on_confirm=None):
        product_name = "Almuerzo Especial Pollo (x1)"
        product_img = "img/comida1.jpg"
        payment_method = "Nequi"
        status_text = order.get("status", "Pendiente")

        status_color_bg = {
            "Completado": "#DCFCE7",
            "Confirmado": "#EFF6FF",
            "Pendiente": "#FEF3C7",
            "Cancelado": "#FEE2E2",
        }.get(status_text, "#F3F4F6")

        status_color_fg = {
            "Completado": COLOR_GREEN_SUCCESS,
            "Confirmado": COLOR_BLUE_INFO,
            "Pendiente": COLOR_ORANGE_PRIMARY,
            "Cancelado": COLOR_RED_ERROR,
        }.get(status_text, COLOR_GRAY_DARK)

        def confirm_and_close(e):
            if on_confirm:
                on_confirm(order)
            close_modal(e)

        card = ft.Container(
            width=640,
            bgcolor=COLOR_WHITE,
            border_radius=20,
            padding=ft.Padding(28, 24, 28, 24),
            shadow=ft.BoxShadow(
                blur_radius=40,
                spread_radius=0,
                color="#50000000",
                offset=ft.Offset(0, 16),
            ),
            content=ft.Column(
                spacing=18,
                tight=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        "Detalle del Pedido",
                                        size=20,
                                        weight="bold",
                                        color=COLOR_GRAY_DARK,
                                    ),
                                    ft.Text(
                                        f"Pedido {order['order_id']} • Token {order['token']}",
                                        size=13,
                                        color=COLOR_GRAY_TEXT,
                                    ),
                                ],
                            ),
                            ft.Container(
                                width=28,
                                height=28,
                                bgcolor="#F3F4F6",
                                border_radius=14,
                                alignment=ft.Alignment.CENTER,
                                on_click=confirm_and_close,
                                content=ft.Icon(
                                    ft.Icons.CLOSE_ROUNDED,
                                    size=16,
                                    color=COLOR_GRAY_DARK,
                                ),
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=18,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Container(
                                width=180,
                                height=150,
                                border_radius=16,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                content=ft.Image(
                                    src=product_img,
                                    fit=ft.BoxFit.COVER,
                                ),
                            ),
                            ft.Column(
                                spacing=12,
                                expand=True,
                                controls=[
                                    ft.Row(
                                        spacing=8,
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.PERSON_OUTLINE,
                                                size=18,
                                                color=COLOR_GRAY_MEDIUM,
                                            ),
                                            ft.Text(
                                                order["client"],
                                                size=15,
                                                weight="bold",
                                                color=COLOR_GRAY_DARK,
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Row(
                                                spacing=4,
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.ACCESS_TIME_OUTLINED,
                                                        size=14,
                                                        color=COLOR_GRAY_TEXT,
                                                    ),
                                                    ft.Text(
                                                        f"{order['date']} • {order['time']}",
                                                        size=12,
                                                        color=COLOR_GRAY_TEXT,
                                                    ),
                                                ],
                                            ),
                                            ft.Row(
                                                spacing=4,
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.RECEIPT_LONG_OUTLINED,
                                                        size=14,
                                                        color=COLOR_GRAY_TEXT,
                                                    ),
                                                    ft.Text(
                                                        order["doc"],
                                                        size=12,
                                                        color=COLOR_GRAY_TEXT,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    ft.Container(
                                        bgcolor="#F9FAFB",
                                        border_radius=12,
                                        padding=ft.Padding(14, 10, 14, 10),
                                        content=ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                    controls=[
                                                        ft.Text(
                                                            product_name,
                                                            size=14,
                                                            weight="bold",
                                                            color=COLOR_GRAY_DARK,
                                                        ),
                                                        ft.Text(
                                                            order["total"],
                                                            size=16,
                                                            weight="bold",
                                                            color=COLOR_ORANGE_PRIMARY,
                                                        ),
                                                    ],
                                                ),
                                                ft.Row(
                                                    spacing=10,
                                                    controls=[
                                                        ft.Row(
                                                            spacing=4,
                                                            controls=[
                                                                ft.Icon(
                                                                    ft.Icons.PAYMENTS_OUTLINED,
                                                                    size=14,
                                                                    color=COLOR_GRAY_TEXT,
                                                                ),
                                                                ft.Text(
                                                                    f"Método de pago: {payment_method}",
                                                                    size=12,
                                                                    color=COLOR_GRAY_TEXT,
                                                                ),
                                                            ],
                                                        ),
                                                        ft.Container(
                                                            bgcolor=status_color_bg,
                                                            border_radius=20,
                                                            padding=ft.Padding(12, 4, 12, 4),
                                                            content=ft.Row(
                                                                spacing=6,
                                                                controls=[
                                                                    ft.Icon(
                                                                        ft.Icons.CHECK_CIRCLE_ROUNDED,
                                                                        size=14,
                                                                        color=status_color_fg,
                                                                    ),
                                                                    ft.Text(
                                                                        status_text,
                                                                        size=11,
                                                                        weight="bold",
                                                                        color=status_color_fg,
                                                                    ),
                                                                ],
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Container(
                                padding=ft.Padding(22, 12, 22, 12),
                                border_radius=24,
                                bgcolor=COLOR_GREEN_SUCCESS,
                                shadow=ft.BoxShadow(
                                    blur_radius=18,
                                    spread_radius=-4,
                                    color="#4016A34A",
                                    offset=ft.Offset(0, 6),
                                ),
                                on_click=close_modal,
                                content=ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.CHECK_ROUNDED,
                                            size=18,
                                            color="white",
                                        ),
                                        ft.Text(
                                            "Confirmar Entrega del Pedido",
                                            size=14,
                                            weight="bold",
                                            color="white",
                                        ),
                                    ],
                                ),
                            )
                        ],
                    ),
                ],
            ),
        )

        return ft.Stack(
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor="#40000000",
                    blur=ft.Blur(12, 12),
                    on_click=close_modal,
                ),
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                    content=card,
                ),
            ],
            expand=True,
        )

    def update_order_status(order_id: str, new_status: str):
        for o in orders:
            if o["order_id"] == order_id:
                o["status"] = new_status
                if new_status == "Completado":
                    o["show_complete"] = False
                break
        rows_col.current.controls = build_rows(search_state["value"])
        rows_col.current.update()

    def show_detail(order: dict):
        def on_confirm_from_modal(o: dict):
            update_order_status(o["order_id"], "Completado")

        modal = _order_detail_modal(order, on_confirm=on_confirm_from_modal)
        if not modal_layer.current:
            return
        if len(modal_layer.current.controls) > 1:
            modal_layer.current.controls[1] = modal
        else:
            modal_layer.current.controls.append(modal)
        modal_layer.current.update()

    def build_rows(query: str = ""):
        q = (query or "").strip().lower()
        filtered = [
            o
            for o in orders
            if not q
            or q in o["order_id"].lower()
            or q in o["client"].lower()
            or q in o["token"].lower()
        ]

        rows = []
        for o in filtered:
            order_dict = dict(o)

            def make_on_status_change(oid=o["order_id"]):
                return lambda _new_status: update_order_status(oid, _new_status)

            row = order_table_row(
                o["order_id"],
                o["token"],
                o["client"],
                o["doc"],
                o["date"],
                o["time"],
                o["total"],
                o["status"],
                o["show_complete"],
                page=page,
                on_view=lambda data=order_dict: show_detail(data),
                on_status_change=make_on_status_change(),
            )
            rows.append(row)

        return rows

    def on_search(e):
        search_state["value"] = e.control.value or ""
        rows_col.current.controls = build_rows(search_state["value"])
        rows_col.current.update()

    # ── Stats row ────────────────────────────────────────────────────────────
    # ✅ CAMBIO: quitado expand=True para que no consuma espacio extra
    stats_row = ft.Row(
        spacing=16,
        controls=[
            order_stat_box("Pendientes",  "1", ft.Icons.SCHEDULE_OUTLINED,    COLOR_ORANGE_PRIMARY),
            order_stat_box("Confirmados", "0", ft.Icons.CHECK_CIRCLE_OUTLINE, COLOR_BLUE_INFO),
            order_stat_box("Completados", "1", ft.Icons.CHECK_CIRCLE_ROUNDED, COLOR_GREEN_SUCCESS),
            order_stat_box("Cancelados",  "1", ft.Icons.CANCEL_OUTLINED,      COLOR_RED_ERROR),
        ],
    )

    def header_cell(label, width):
        return ft.Container(
            width=width,
            content=ft.Text(label, size=12, weight="bold", color=COLOR_GRAY_TEXT),
        )

    table_header = ft.Container(
        padding=ft.Padding(20, 12, 20, 12),
        bgcolor="#F9FAFB",
        border=ft.Border(bottom=ft.BorderSide(1, "#F3F4F6")),
        border_radius=ft.BorderRadius(top_left=12, top_right=12, bottom_left=0, bottom_right=0),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                header_cell("PEDIDO / TOKEN", 170),
                header_cell("CLIENTE",         190),
                header_cell("FECHA / HORA",    160),
                header_cell("TOTAL",           100),
                header_cell("ESTADO",          120),
                header_cell("ACCIONES",        160),
            ],
        ),
    )

    orders_table = ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=0,
            controls=[
                table_header,
                ft.Column(
                    ref=rows_col,
                    spacing=0,
                    controls=build_rows(),
                ),
            ],
        ),
    )

    base_content = ft.Container(
        expand=True,
        bgcolor=COLOR_BG_PAGE,
        padding=ft.Padding(32, 28, 32, 28),
        content=ft.Column(
            expand=True,
            # ✅ CAMBIO: spacing reducido de 24 → 14
            spacing=14,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(
                            "Gestión de Pedidos",
                            size=26,
                            weight="bold",
                            color=COLOR_GRAY_DARK,
                        ),
                        ft.Text(
                            "Administra y confirma los pedidos de clientes",
                            size=14,
                            color=COLOR_GRAY_TEXT,
                        ),
                    ],
                ),
                stats_row,
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    border_radius=12,
                    border=ft.Border.all(1, COLOR_GRAY_BORDER),
                    padding=ft.Padding(16, 0, 16, 0),
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.SEARCH_ROUNDED,
                                color=COLOR_GRAY_TEXT,
                                size=20,
                            ),
                            ft.TextField(
                                hint_text="Buscar por ID, cliente o documento...",
                                border=ft.InputBorder.NONE,
                                expand=True,
                                height=48,
                                text_size=14,
                                hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
                                on_change=on_search,
                            ),
                        ],
                        spacing=10,
                    ),
                ),
                orders_table,
            ],
        ),
    )

    return ft.Stack(
        ref=modal_layer,
        expand=True,
        controls=[base_content],
    )