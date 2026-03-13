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
from controllers.pedidos import PedidosController


def pedidos_view(page: ft.Page):
    rows_col    = ft.Ref[ft.Column]()
    modal_layer = ft.Ref[ft.Stack]()

    # ── Cargar datos reales desde la BD ──────────────────────────────
    ok, msg = PedidosController.cargar_pedidos(page)
    if not ok:
        print(f"[pedidos_view] {msg}")
        page.pedidos_data       = []
        page.pedidos_contadores = {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0}
    else:
        raw = getattr(page, "pedidos_data", [])
        print(f">>> [pedidos_view] primer pedido raw: {raw[0] if raw else 'VACÍO'}")

    def _get_orders():
        """Convierte page.pedidos_data al formato que usa la vista."""
        result = []
        for p in getattr(page, "pedidos_data", []):
            print(f">>> [_get_orders] claves disponibles: {list(p.keys())}")
            # Buscar el id con distintos nombres posibles
            pedido_id = p.get("id") or p.get("pedido_id") or p.get("ID") or 0
            estado_raw = (p.get("estado") or "pendiente").lower()
            estado_ui  = estado_raw.capitalize()
            show_complete = estado_raw in ("pendiente", "confirmado")
            result.append({
                "id":            pedido_id,
                "order_id":      p.get("codigo") or f"PED-{pedido_id}",
                "token":         "",
                "client":        p.get("cliente_nombre") or p.get("nombre") or "",
                "doc":           p.get("cliente_documento") or "",
                "date":          p.get("fecha") or "",
                "time":          p.get("hora") or "",
                "total":         f"${float(p.get('total') or 0):,.0f}".replace(",", "."),
                "status":        estado_ui,
                "show_complete": show_complete,
            })
        return result

    # ── Contadores ───────────────────────────────────────────────────
    def _get_contadores():
        return getattr(page, "pedidos_contadores",
                       {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0})

    stats_container = ft.Ref[ft.Row]()

    def _refresh_contadores():
        c = _get_contadores()
        if stats_container.current:
            stats_container.current.controls = _build_stats_row(c)
            stats_container.current.update()

    # ── Modal ─────────────────────────────────────────────────────────
    def close_modal(e=None):
        if modal_layer.current and len(modal_layer.current.controls) > 1:
            modal_layer.current.controls = modal_layer.current.controls[:1]
            modal_layer.current.update()

    def _order_detail_modal(order: dict, detalle: dict):
        pedido  = detalle["pedido"]
        items   = detalle["items"]
        status_text = order.get("status", "Pendiente")

        status_color_bg = {
            "Completado": "#DCFCE7", "Confirmado": "#EFF6FF",
            "Pendiente":  "#FEF3C7", "Cancelado":  "#FEE2E2",
        }.get(status_text, "#F3F4F6")

        status_color_fg = {
            "Completado": COLOR_GREEN_SUCCESS, "Confirmado": COLOR_BLUE_INFO,
            "Pendiente":  COLOR_ORANGE_PRIMARY, "Cancelado": COLOR_RED_ERROR,
        }.get(status_text, COLOR_GRAY_DARK)

        # ── Construir filas de ítems con imagen ──────────────────────
        item_rows = []
        for it in items:
            img_src = it.get("imagen", "")
            item_rows.append(
                ft.Container(
                    bgcolor="#FAFAFA", border_radius=12,
                    padding=ft.Padding(12, 10, 12, 10),
                    content=ft.Row(
                        spacing=14,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Imagen del plato
                            ft.Container(
                                width=64, height=64, border_radius=10,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                bgcolor="#F3F4F6",
                                content=ft.Image(src=img_src, fit=ft.BoxFit.COVER)
                                        if img_src else
                                        ft.Icon(ft.Icons.FASTFOOD_OUTLINED, size=28, color=COLOR_GRAY_TEXT),
                            ),
                            # Nombre + descripción + cantidad
                            ft.Column(spacing=2, expand=True, controls=[
                                ft.Text(it["menu_nombre"], size=13, weight="bold", color=COLOR_GRAY_DARK),
                                ft.Text(it.get("descripcion", ""), size=11, color=COLOR_GRAY_TEXT),
                                ft.Container(
                                    bgcolor=COLOR_ORANGE_LIGHT, border_radius=8,
                                    padding=ft.Padding(8, 2, 8, 2),
                                    width=90,
                                    content=ft.Text(f"Cantidad: {it['cantidad']}", size=11,
                                                    weight="bold", color=COLOR_ORANGE_PRIMARY),
                                ),
                            ]),
                            # Precio
                            ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                ft.Text(
                                    f"${float(it['subtotal']):,.0f}".replace(",", "."),
                                    size=15, weight="bold", color=COLOR_ORANGE_PRIMARY,
                                ),
                                ft.Text(
                                    f"c/u ${float(it['precio_unitario']):,.0f}".replace(",", "."),
                                    size=11, color=COLOR_GRAY_TEXT,
                                ),
                            ]),
                        ]
                    )
                )
            )
            item_rows.append(ft.Divider(height=1, color="#F0F0F0"))

        # Imagen del primer ítem (para el panel izquierdo del modal)
        primera_imagen = items[0]["imagen"] if items else ""

        def on_completar(e):
            ok, msg = PedidosController.cambiar_estado(page, order["id"], "completado")
            if ok:
                order["status"]        = "Completado"
                order["show_complete"] = False
                _refresh_rows(search_state["value"])
                _refresh_contadores()
            close_modal()

        card = ft.Container(
            width=640,
            bgcolor=COLOR_WHITE,
            border_radius=20,
            padding=ft.Padding(28, 24, 28, 24),
            shadow=ft.BoxShadow(blur_radius=40, spread_radius=0,
                                color="#50000000", offset=ft.Offset(0, 16)),
            content=ft.Column(
                spacing=18, tight=True,
                controls=[
                    # ── Cabecera ──────────────────────────────────────
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(spacing=4, controls=[
                                ft.Text("Detalle del Pedido", size=20, weight="bold", color=COLOR_GRAY_DARK),
                                ft.Text(
                                    f"Pedido {pedido['codigo']}",
                                    size=13, color=COLOR_GRAY_TEXT,
                                ),
                            ]),
                            ft.Container(
                                width=28, height=28, bgcolor="#F3F4F6",
                                border_radius=14, alignment=ft.Alignment.CENTER,
                                on_click=close_modal,
                                content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color=COLOR_GRAY_DARK),
                            ),
                        ],
                    ),
                    # ── Info cliente + imagen ─────────────────────────
                    ft.Row(
                        spacing=18, vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Container(
                                width=160, height=130, border_radius=14,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                bgcolor="#F3F4F6",
                                content=ft.Image(src=primera_imagen, fit=ft.BoxFit.COVER)
                                        if primera_imagen else
                                        ft.Icon(ft.Icons.FASTFOOD_OUTLINED, size=48, color=COLOR_GRAY_TEXT),
                            ),
                            ft.Column(spacing=10, expand=True, controls=[
                                ft.Row(spacing=8, controls=[
                                    ft.Icon(ft.Icons.PERSON_OUTLINE, size=18, color=COLOR_GRAY_MEDIUM),
                                    ft.Text(pedido["cliente_nombre"], size=15, weight="bold", color=COLOR_GRAY_DARK),
                                ]),
                                ft.Row(spacing=10, controls=[
                                    ft.Row(spacing=4, controls=[
                                        ft.Icon(ft.Icons.ACCESS_TIME_OUTLINED, size=14, color=COLOR_GRAY_TEXT),
                                        ft.Text(f"{pedido['fecha']} • {pedido['hora']}", size=12, color=COLOR_GRAY_TEXT),
                                    ]),
                                    ft.Row(spacing=4, controls=[
                                        ft.Icon(ft.Icons.BADGE_OUTLINED, size=14, color=COLOR_GRAY_TEXT),
                                        ft.Text(pedido["cliente_documento"], size=12, color=COLOR_GRAY_TEXT),
                                    ]),
                                ]),
                                ft.Row(spacing=4, controls=[
                                    ft.Icon(ft.Icons.PHONE_OUTLINED, size=14, color=COLOR_GRAY_TEXT),
                                    ft.Text(pedido.get("cliente_telefono", ""), size=12, color=COLOR_GRAY_TEXT),
                                ]),
                                ft.Container(
                                    bgcolor=status_color_bg, border_radius=20,
                                    padding=ft.Padding(12, 4, 12, 4),
                                    content=ft.Row(spacing=6, controls=[
                                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=14, color=status_color_fg),
                                        ft.Text(status_text, size=11, weight="bold", color=status_color_fg),
                                    ]),
                                ),
                            ]),
                        ],
                    ),
                    # ── Ítems ─────────────────────────────────────────
                    ft.Container(
                        bgcolor="#F9FAFB", border_radius=12,
                        padding=ft.Padding(14, 10, 14, 10),
                        content=ft.Column(spacing=8, controls=item_rows if item_rows else [
                            ft.Text("Sin ítems registrados", size=13, color=COLOR_GRAY_TEXT)
                        ]),
                    ),
                    # ── Comprobante de pago ───────────────────────────
                    ft.Container(
                        bgcolor="#F0FDF4",
                        border_radius=12,
                        border=ft.Border.all(1, "#BBF7D0"),
                        padding=ft.Padding(16, 12, 16, 12),
                        content=ft.Row(
                            spacing=14,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=48, height=48, border_radius=10,
                                    bgcolor="#DCFCE7",
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED,
                                                    size=26, color=COLOR_GREEN_SUCCESS),
                                ),
                                ft.Column(spacing=2, expand=True, controls=[
                                    ft.Text("Comprobante de Pago", size=13,
                                            weight="bold", color="#166534"),
                                    ft.Text("Pago registrado en el sistema",
                                            size=11, color="#4ADE80"),
                                ]),
                                ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                    ft.Text("TOTAL", size=11, color="#166534", weight="bold"),
                                    ft.Text(order["total"], size=18,
                                            weight="bold", color=COLOR_GREEN_SUCCESS),
                                ]),
                            ]
                        )
                    ),
                    # ── Botón ─────────────────────────────────────────
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Container(
                                padding=ft.Padding(22, 12, 22, 12),
                                border_radius=24, bgcolor=COLOR_GREEN_SUCCESS,
                                shadow=ft.BoxShadow(blur_radius=18, spread_radius=-4,
                                                    color="#4016A34A", offset=ft.Offset(0, 6)),
                                on_click=on_completar if order.get("show_complete") else close_modal,
                                content=ft.Row(spacing=8, controls=[
                                    ft.Icon(ft.Icons.CHECK_ROUNDED, size=18, color="white"),
                                    ft.Text(
                                        "Confirmar Entrega" if order.get("show_complete") else "Cerrar",
                                        size=14, weight="bold", color="white",
                                    ),
                                ]),
                            )
                        ],
                    ),
                ],
            ),
        )

        return ft.Stack(
            expand=True,
            controls=[
                ft.Container(expand=True, bgcolor="#40000000",
                             blur=ft.Blur(12, 12), on_click=close_modal),
                ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=card),
            ],
        )

    # ── Cambiar estado desde la tabla ────────────────────────────────
    def on_status_change(pedido_id: int, order_id_str: str, nuevo_estado_ui: str):
        nuevo_estado_db = nuevo_estado_ui.lower()
        ok, msg = PedidosController.cambiar_estado(page, pedido_id, nuevo_estado_db)
        if ok:
            _refresh_rows(search_state["value"])
            _refresh_contadores()

    # ── Mostrar modal con datos reales ───────────────────────────────
    def show_detail(order: dict):
        # styles.py pasa un dict sin "id" — lo resolvemos buscando por codigo
        pedido_id = order.get("id")
        if not pedido_id:
            # Buscar el id real en page.pedidos_data por codigo (ej: "PED-001")
            order_id_str = order.get("order_id", "")
            for p in getattr(page, "pedidos_data", []):
                if p.get("codigo") == order_id_str:
                    pedido_id = p["id"]
                    break
        if not pedido_id:
            print(f"[show_detail] No se pudo resolver el id del pedido: {order}")
            return

        ok, detalle, msg = PedidosController.obtener_detalle(pedido_id)
        if not ok or detalle is None:
            print(f"[show_detail] {msg}")
            return
        # Enriquecer order con el id para que el modal pueda usarlo
        order["id"] = pedido_id
        modal = _order_detail_modal(order, detalle)
        if not modal_layer.current:
            return
        if len(modal_layer.current.controls) > 1:
            modal_layer.current.controls[1] = modal
        else:
            modal_layer.current.controls.append(modal)
        modal_layer.current.update()

    search_state = {"value": ""}

    def _refresh_rows(query: str = ""):
        if rows_col.current:
            rows_col.current.controls = build_rows(query)
            rows_col.current.update()

    def build_rows(query: str = ""):
        orders = _get_orders()
        q = (query or "").strip().lower()
        filtered = [
            o for o in orders
            if not q
            or q in o["order_id"].lower()
            or q in o["client"].lower()
            or q in o["token"].lower()
            or q in o["doc"].lower()
        ]

        rows = []
        for o in filtered:
            # Copia fija del dict completo para que el lambda capture el valor correcto
            _snap = {
                "id":            o["id"],
                "order_id":      o["order_id"],
                "token":         o["token"],
                "client":        o["client"],
                "doc":           o["doc"],
                "date":          o["date"],
                "time":          o["time"],
                "total":         o["total"],
                "status":        o["status"],
                "show_complete": o["show_complete"],
            }
            row = order_table_row(
                _snap["order_id"],
                _snap["token"],
                _snap["client"],
                _snap["doc"],
                _snap["date"],
                _snap["time"],
                _snap["total"],
                _snap["status"],
                _snap["show_complete"],
                page=page,
                on_view=lambda snap=_snap: show_detail(snap),
                on_status_change=lambda ns, snap=_snap: on_status_change(snap["id"], snap["order_id"], ns),
            )
            rows.append(row)
        return rows

    def on_search(e):
        search_state["value"] = e.control.value or ""
        if search_state["value"].strip():
            PedidosController.buscar(page, search_state["value"])
        else:
            PedidosController.cargar_pedidos(page)
        _refresh_rows(search_state["value"])

    # ── Contadores ───────────────────────────────────────────────────
    def _build_stats_row(c: dict):
        return [
            order_stat_box("Pendientes",  str(c["pendiente"]),  ft.Icons.SCHEDULE_OUTLINED,   COLOR_ORANGE_PRIMARY),
            order_stat_box("Confirmados", str(c["confirmado"]), ft.Icons.CHECK_CIRCLE_OUTLINE, COLOR_BLUE_INFO),
            order_stat_box("Completados", str(c["completado"]), ft.Icons.CHECK_CIRCLE_ROUNDED, COLOR_GREEN_SUCCESS),
            order_stat_box("Cancelados",  str(c["cancelado"]),  ft.Icons.CANCEL_OUTLINED,      COLOR_RED_ERROR),
        ]

    c = _get_contadores()
    stats_row = ft.Row(ref=stats_container, spacing=16, controls=_build_stats_row(c))

    # ── Cabecera de tabla ────────────────────────────────────────────
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
        bgcolor=COLOR_WHITE, border_radius=16,
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Column(
            spacing=0,
            controls=[
                table_header,
                ft.Column(ref=rows_col, spacing=0, controls=build_rows()),
            ],
        ),
    )

    base_content = ft.Container(
        expand=True, bgcolor=COLOR_BG_PAGE,
        padding=ft.Padding(32, 28, 32, 28),
        content=ft.Column(
            expand=True, spacing=14,
            controls=[
                ft.Column(spacing=4, controls=[
                    ft.Text("Gestión de Pedidos", size=26, weight="bold", color=COLOR_GRAY_DARK),
                    ft.Text("Administra y confirma los pedidos de clientes", size=14, color=COLOR_GRAY_TEXT),
                ]),
                stats_row,
                ft.Container(
                    bgcolor=COLOR_WHITE, border_radius=12,
                    border=ft.Border.all(1, COLOR_GRAY_BORDER),
                    padding=ft.Padding(16, 0, 16, 0),
                    content=ft.Row(spacing=10, controls=[
                        ft.Icon(ft.Icons.SEARCH_ROUNDED, color=COLOR_GRAY_TEXT, size=20),
                        ft.TextField(
                            hint_text="Buscar por ID, cliente o documento...",
                            border=ft.InputBorder.NONE,
                            expand=True, height=48, text_size=14,
                            hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
                            on_change=on_search,
                        ),
                    ]),
                ),
                # Tabla scrolleable que crece con los pedidos
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        controls=[orders_table],
                    ),
                ),
            ],
        ),
    )

    return ft.Stack(
        ref=modal_layer,
        expand=True,
        controls=[base_content],
    )