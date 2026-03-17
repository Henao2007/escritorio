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
    show_toast,
)
from controllers.pedidos import PedidosController


def pedidos_view(page: ft.Page):
    rows_col    = ft.Ref[ft.Column]()
    modal_layer = ft.Ref[ft.Stack]()
    stats_ref   = ft.Ref[ft.Container]()

    ok, msg = PedidosController.cargar_pedidos(page)
    if not ok:
        page.pedidos_data       = []
        page.pedidos_contadores = {"pendiente": 0, "confirmado": 0, "completado": 0}

    search_state = {"value": ""}

    def is_mobile():
        return (page.width or 1200) < 700

    def _h_pad():
        return 14 if is_mobile() else 28

    def _v_pad():
        return 16 if is_mobile() else 24

    def _get_orders():
        result = []
        for p in getattr(page, "pedidos_data", []):
            pedido_id  = p.get("id") or p.get("pedido_id") or 0
            estado_raw = (p.get("estado") or "pendiente").lower()
            result.append({
                "id":            pedido_id,
                "order_id":      p.get("codigo") or f"PED-{pedido_id}",
                "token":         p.get("token") or "—",
                "client":        p.get("cliente_nombre") or p.get("nombre") or "—",
                "doc":           p.get("cliente_documento") or "—",
                "date":          p.get("fecha") or "—",
                "time":          p.get("hora") or "—",
                "total":         f"${float(p.get('total') or 0):,.0f}".replace(",", "."),
                "status":        estado_raw.capitalize(),
                "show_complete": estado_raw == "confirmado",
            })
        return result

    def _get_contadores():
        return getattr(page, "pedidos_contadores",
                       {"pendiente": 0, "confirmado": 0, "completado": 0, "cancelado": 0})

    def _status_badge(status: str):
        cfg = {
            "Completado": ("#DCFCE7", COLOR_GREEN_SUCCESS),
            "Confirmado": ("#EFF6FF", COLOR_BLUE_INFO),
            "Pendiente":  ("#FEF3C7", COLOR_ORANGE_PRIMARY),
            "Cancelado":  ("#FEE2E2", COLOR_RED_ERROR),
        }
        bg, fg = cfg.get(status, ("#F3F4F6", COLOR_GRAY_DARK))
        # tight=True + padding horizontal pequeño → badge solo ocupa lo que necesita
        return ft.Container(
            bgcolor=bg,
            border_radius=20,
            padding=ft.Padding(12, 4, 12, 4),
            content=ft.Text(status, size=11, weight="bold", color=fg),
        )

    # ── Cabecera proporcional ─────────────────────────────────────────
    def _build_table_header():
        if is_mobile():
            return ft.Container(height=0)
        return ft.Container(
            bgcolor="#F9FAFB",
            padding=ft.Padding(20, 11, 20, 11),
            border_radius=ft.BorderRadius(12, 12, 0, 0),
            border=ft.Border(bottom=ft.BorderSide(1, "#EFEFEF")),
            content=ft.Row(spacing=0, controls=[
                # Pedido/Token: 3 partes
                ft.Container(expand=3, content=ft.Text(
                    "PEDIDO / TOKEN", size=11, weight="bold", color=COLOR_GRAY_TEXT)),
                # Cliente: 3 partes (antes 4, sobraba mucho)
                ft.Container(expand=3, content=ft.Text(
                    "CLIENTE", size=11, weight="bold", color=COLOR_GRAY_TEXT)),
                # Fecha/Hora: 2 partes
                ft.Container(expand=2, content=ft.Text(
                    "FECHA / HORA", size=11, weight="bold", color=COLOR_GRAY_TEXT)),
                # Total: 2 partes
                ft.Container(expand=2, content=ft.Text(
                    "TOTAL", size=11, weight="bold", color=COLOR_GRAY_TEXT)),
                # Estado: ancho fijo compacto
                ft.Container(width=110,
                    padding=ft.Padding(0, 0, 12, 0),
                    content=ft.Text(
                    "ESTADO", size=11, weight="bold", color=COLOR_GRAY_TEXT)),
                # Acciones: solo lo necesario
                ft.Container(width=160, content=ft.Text(
                    "ACCIONES", size=11, weight="bold", color=COLOR_GRAY_TEXT)),
            ]),
        )

    # ── Fila de pedido ────────────────────────────────────────────────
    def _build_row(order: dict):
        status_badge_ref = ft.Ref[ft.Container]()
        complete_btn_ref = ft.Ref[ft.Container]()

        def on_complete(e):
            ok2, _ = PedidosController.cambiar_estado(page, order["id"], "completado")
            if ok2:
                order["status"]        = "Completado"
                order["show_complete"] = False
                nb = _status_badge("Completado")
                status_badge_ref.current.bgcolor       = nb.bgcolor
                status_badge_ref.current.content.color = nb.content.color
                status_badge_ref.current.content.value = "Completado"
                status_badge_ref.current.update()
                complete_btn_ref.current.visible = False
                complete_btn_ref.current.update()
                _refresh_contadores()
                show_toast(page, f'Pedido {order["order_id"]} marcado como completado',
                           title="Pedido Completado", type="success")
            else:
                show_toast(page, "Error al completar el pedido", type="error")

        init_badge = _status_badge(order["status"])
        # badge NO tiene expand — ocupa solo su contenido
        status_box = ft.Container(
            ref=status_badge_ref,
            bgcolor=init_badge.bgcolor,
            border_radius=20,
            padding=ft.Padding(12, 4, 12, 4),
            content=ft.Text(order["status"], size=11, weight="bold",
                            color=init_badge.content.color),
        )

        btn_ver = ft.Container(
            on_click=lambda e, o=order: show_detail(o),
            bgcolor="#F3F4F6", border_radius=8,
            padding=ft.Padding(10, 6, 10, 6),
            content=ft.Row(spacing=4, tight=True, controls=[
                ft.Icon(ft.Icons.VISIBILITY_OUTLINED, size=14, color=COLOR_GRAY_MEDIUM),
                ft.Text("Ver", size=12, weight="bold", color=COLOR_GRAY_MEDIUM),
            ]),
        )

        btn_completar = ft.Container(
            ref=complete_btn_ref,
            visible=order["show_complete"],
            on_click=on_complete,
            bgcolor=COLOR_GREEN_SUCCESS, border_radius=8,
            padding=ft.Padding(10, 6, 10, 6),
            content=ft.Row(spacing=4, tight=True, controls=[
                ft.Icon(ft.Icons.CHECK_ROUNDED, size=14, color="white"),
                ft.Text("Completar", size=12, weight="bold", color="white"),
            ]),
        )

        # ── Móvil ─────────────────────────────────────────────────────
        if is_mobile():
            return ft.Container(
                bgcolor=COLOR_WHITE, border_radius=12,
                border=ft.Border.all(1, "#F3EFEA"),
                padding=ft.Padding(14, 12, 14, 12),
                margin=ft.Margin(0, 0, 0, 8),
                content=ft.Column(spacing=8, controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Column(spacing=2, tight=True, controls=[
                            ft.Text(order["order_id"], size=13,
                                    weight="bold", color=COLOR_GRAY_DARK),
                            ft.Row(spacing=4, controls=[
                                ft.Text("Token:", size=11, color=COLOR_GRAY_TEXT),
                                ft.Text(order["token"], size=11, weight="bold",
                                        color=COLOR_ORANGE_PRIMARY),
                            ]),
                        ]),
                        status_box,
                    ]),
                    ft.Divider(height=1, color="#F3F4F6"),
                    ft.Row(spacing=6, controls=[
                        ft.Icon(ft.Icons.PERSON_OUTLINE, size=13, color=COLOR_GRAY_TEXT),
                        ft.Text(order["client"], size=12, weight="bold",
                                color=COLOR_GRAY_DARK, expand=True,
                                overflow=ft.TextOverflow.ELLIPSIS),
                    ]),
                    ft.Row(spacing=16, controls=[
                        ft.Row(spacing=4, controls=[
                            ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED,
                                    size=12, color=COLOR_GRAY_TEXT),
                            ft.Text(order["date"], size=11, color=COLOR_GRAY_TEXT),
                        ]),
                        ft.Row(spacing=4, controls=[
                            ft.Icon(ft.Icons.ACCESS_TIME_OUTLINED,
                                    size=12, color=COLOR_GRAY_TEXT),
                            ft.Text(order["time"], size=11, color=COLOR_GRAY_TEXT),
                        ]),
                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text(order["total"], size=15,
                                weight="bold", color=COLOR_ORANGE_PRIMARY),
                        ft.Row(spacing=8, controls=[btn_ver, btn_completar]),
                    ]),
                ]),
            )

        # ── Desktop ───────────────────────────────────────────────────
        return ft.Container(
            bgcolor=COLOR_WHITE,
            padding=ft.Padding(20, 12, 20, 12),
            border=ft.Border(bottom=ft.BorderSide(1, "#F5F5F5")),
            content=ft.Row(
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Pedido + Token — expand=3
                    ft.Container(expand=3, content=ft.Column(
                        spacing=2, tight=True, controls=[
                            ft.Text(order["order_id"], size=13, weight="bold",
                                    color=COLOR_GRAY_DARK,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Row(spacing=3, controls=[
                                ft.Text("Token:", size=11, color=COLOR_GRAY_TEXT),
                                ft.Text(order["token"], size=11, weight="bold",
                                        color=COLOR_ORANGE_PRIMARY,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                            ]),
                        ])),
                    # Cliente — expand=3 (igual que cabecera)
                    ft.Container(expand=3, content=ft.Column(
                        spacing=2, tight=True, controls=[
                            ft.Text(order["client"], size=13, weight="bold",
                                    color=COLOR_GRAY_DARK,
                                    overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
                            ft.Text(order["doc"], size=11, color=COLOR_GRAY_TEXT,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                        ])),
                    # Fecha/Hora — expand=2
                    ft.Container(expand=2, content=ft.Column(
                        spacing=2, tight=True, controls=[
                            ft.Row(spacing=4, controls=[
                                ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED,
                                        size=12, color=COLOR_GRAY_TEXT),
                                ft.Text(order["date"], size=12, color=COLOR_GRAY_MEDIUM,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                            ]),
                            ft.Row(spacing=4, controls=[
                                ft.Icon(ft.Icons.ACCESS_TIME_OUTLINED,
                                        size=12, color=COLOR_GRAY_TEXT),
                                ft.Text(order["time"], size=11, color=COLOR_GRAY_TEXT),
                            ]),
                        ])),
                    # Total — expand=2
                    ft.Container(expand=2, content=ft.Text(
                        order["total"], size=14, weight="bold",
                        color=COLOR_ORANGE_PRIMARY)),
                    # Estado — ancho fijo compacto, alineado con cabecera
                    ft.Container(width=110,
                        padding=ft.Padding(0, 0, 12, 0),
                        content=status_box),
                    # Acciones — ancho fijo igual que cabecera, botones pegados al badge
                    ft.Container(width=160, content=ft.Row(
                        spacing=8, tight=True,
                        controls=[btn_ver, btn_completar])),
                ],
            ),
        )

    def build_rows(query: str = ""):
        orders = _get_orders()
        q = (query or "").strip().lower()
        filtered = [o for o in orders if not q
                    or q in o["order_id"].lower()
                    or q in o["client"].lower()
                    or q in o["token"].lower()
                    or q in o["doc"].lower()
                    or q in o["total"].lower()
                    or q in o["status"].lower()
                    or q in o["date"].lower()
                    or q in o["time"].lower()]
        if not filtered:
            return [ft.Container(
                padding=ft.Padding(20, 60, 20, 60),
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED,
                                size=52, color="#D1D5DB"),
                        ft.Text("No se encontraron pedidos",
                                size=15, color=COLOR_GRAY_TEXT, weight="w500"),
                        ft.Text("Los pedidos aparecerán aquí cuando los clientes realicen compras",
                                size=12, color="#D1D5DB",
                                text_align=ft.TextAlign.CENTER),
                    ],
                ),
            )]
        return [_build_row(o) for o in filtered]

    def _refresh_rows(query: str = ""):
        if rows_col.current:
            rows_col.current.controls = build_rows(query)
            rows_col.current.update()

    def _refresh_contadores():
        if stats_ref.current:
            stats_ref.current.content = _build_stats(_get_contadores())
            stats_ref.current.update()

    def _build_stats(c: dict):
        boxes = [
            order_stat_box("Pendientes",  str(c.get("pendiente",  0)),
                           ft.Icons.SCHEDULE_OUTLINED,   COLOR_ORANGE_PRIMARY),
            order_stat_box("Confirmados", str(c.get("confirmado", 0)),
                           ft.Icons.CHECK_CIRCLE_OUTLINE, COLOR_BLUE_INFO),
            order_stat_box("Completados", str(c.get("completado", 0)),
                           ft.Icons.CHECK_CIRCLE_ROUNDED, COLOR_GREEN_SUCCESS),
        ]
        return ft.Row(controls=boxes, spacing=14, expand=True)

    # ── Modal detalle ─────────────────────────────────────────────────
    def close_modal(e=None):
        if modal_layer.current and len(modal_layer.current.controls) > 1:
            modal_layer.current.controls = modal_layer.current.controls[:1]
            modal_layer.current.update()

    def _order_detail_modal(order: dict, detalle: dict):
        pedido      = detalle["pedido"]
        items       = detalle["items"]
        status_text = order.get("status", "Pendiente")
        status_cfg  = {
            "Completado": ("#DCFCE7", COLOR_GREEN_SUCCESS),
            "Confirmado": ("#EFF6FF", COLOR_BLUE_INFO),
            "Pendiente":  ("#FEF3C7", COLOR_ORANGE_PRIMARY),
            "Cancelado":  ("#FEE2E2", COLOR_RED_ERROR),
        }
        status_bg, status_fg = status_cfg.get(status_text, ("#F3F4F6", COLOR_GRAY_DARK))

        item_rows = []
        for it in items:
            img_src = it.get("imagen", "")
            item_rows.append(ft.Container(
                bgcolor="#FAFAFA", border_radius=10,
                padding=ft.Padding(10, 8, 10, 8),
                content=ft.Row(spacing=10,
                               vertical_alignment=ft.CrossAxisAlignment.CENTER,
                               controls=[
                    ft.Container(
                        width=52, height=52, border_radius=8,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        bgcolor="#F3F4F6",
                        content=ft.Image(src=img_src, fit=ft.BoxFit.COVER)
                                if img_src else
                                ft.Icon(ft.Icons.FASTFOOD_OUTLINED,
                                        size=22, color=COLOR_GRAY_TEXT),
                    ),
                    ft.Column(spacing=2, expand=True, controls=[
                        ft.Text(it["menu_nombre"], size=13,
                                weight="bold", color=COLOR_GRAY_DARK),
                        ft.Container(
                            bgcolor=COLOR_ORANGE_LIGHT, border_radius=6,
                            padding=ft.Padding(6, 1, 6, 1),
                            content=ft.Text(f"x{it['cantidad']}", size=11,
                                            weight="bold", color=COLOR_ORANGE_PRIMARY),
                        ),
                    ]),
                    ft.Column(spacing=1,
                              horizontal_alignment=ft.CrossAxisAlignment.END,
                              controls=[
                        ft.Text(f"${float(it['subtotal']):,.0f}".replace(",", "."),
                                size=13, weight="bold", color=COLOR_ORANGE_PRIMARY),
                        ft.Text(f"c/u ${float(it['precio_unitario']):,.0f}".replace(",", "."),
                                size=10, color=COLOR_GRAY_TEXT),
                    ]),
                ]),
            ))
            item_rows.append(ft.Divider(height=1, color="#F0F0F0"))

        def on_completar(e):
            ok2, _ = PedidosController.cambiar_estado(page, order["id"], "completado")
            if ok2:
                order["status"]        = "Completado"
                order["show_complete"] = False
                _refresh_rows(search_state["value"])
                _refresh_contadores()
                close_modal()
                show_toast(page, f'Pedido {pedido["codigo"]} marcado como completado',
                           title="Pedido Completado", type="success")
            else:
                close_modal()
                show_toast(page, "Error al completar el pedido", type="error")

        modal_w = min((page.width or 600) - 32, 540)
        pad     = 16 if is_mobile() else 22

        card = ft.Container(
            width=modal_w,
            bgcolor=COLOR_WHITE, border_radius=20,
            padding=ft.Padding(pad, pad, pad, pad),
            shadow=ft.BoxShadow(blur_radius=40, spread_radius=0,
                                color="#50000000", offset=ft.Offset(0, 16)),
            content=ft.Column(
                spacing=12, tight=True,
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           vertical_alignment=ft.CrossAxisAlignment.CENTER,
                           controls=[
                        ft.Column(spacing=2, tight=True, controls=[
                            ft.Text("Detalle del Pedido", size=17,
                                    weight="bold", color=COLOR_GRAY_DARK),
                            ft.Text(f"Pedido {pedido['codigo']}",
                                    size=12, color=COLOR_GRAY_TEXT),
                        ]),
                        ft.Container(
                            width=28, height=28, bgcolor="#F3F4F6",
                            border_radius=14, alignment=ft.Alignment(0, 0),
                            on_click=close_modal,
                            content=ft.Icon(ft.Icons.CLOSE_ROUNDED,
                                            size=16, color=COLOR_GRAY_DARK),
                        ),
                    ]),
                    ft.Container(
                        bgcolor="#F9FAFB", border_radius=12,
                        padding=ft.Padding(12, 10, 12, 10),
                        content=ft.Column(spacing=6, controls=[
                            ft.Row(spacing=8, controls=[
                                ft.Icon(ft.Icons.PERSON_OUTLINE,
                                        size=15, color=COLOR_GRAY_MEDIUM),
                                ft.Text(pedido["cliente_nombre"], size=13,
                                        weight="bold", color=COLOR_GRAY_DARK,
                                        expand=True),
                                ft.Container(
                                    bgcolor=status_bg, border_radius=20,
                                    padding=ft.Padding(10, 3, 10, 3),
                                    content=ft.Text(status_text, size=11,
                                                    weight="bold", color=status_fg),
                                ),
                            ]),
                            ft.Row(spacing=14, wrap=True, controls=[
                                ft.Row(spacing=4, controls=[
                                    ft.Icon(ft.Icons.BADGE_OUTLINED,
                                            size=12, color=COLOR_GRAY_TEXT),
                                    ft.Text(pedido["cliente_documento"],
                                            size=11, color=COLOR_GRAY_TEXT),
                                ]),
                                ft.Row(spacing=4, controls=[
                                    ft.Icon(ft.Icons.ACCESS_TIME_OUTLINED,
                                            size=12, color=COLOR_GRAY_TEXT),
                                    ft.Text(f"{pedido['fecha']} {pedido['hora']}",
                                            size=11, color=COLOR_GRAY_TEXT),
                                ]),
                                ft.Row(spacing=4, controls=[
                                    ft.Icon(ft.Icons.PHONE_OUTLINED,
                                            size=12, color=COLOR_GRAY_TEXT),
                                    ft.Text(pedido.get("cliente_telefono", "—"),
                                            size=11, color=COLOR_GRAY_TEXT),
                                ]),
                            ]),
                        ]),
                    ),
                    ft.Container(
                        bgcolor="#F9FAFB", border_radius=12,
                        padding=ft.Padding(10, 8, 10, 4),
                        content=ft.Column(spacing=0, controls=item_rows or [
                            ft.Text("Sin ítems registrados",
                                    size=13, color=COLOR_GRAY_TEXT)
                        ]),
                    ),
                    ft.Container(
                        bgcolor="#F0FDF4", border_radius=12,
                        border=ft.Border.all(1, "#BBF7D0"),
                        padding=ft.Padding(12, 10, 12, 10),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(spacing=8, controls=[
                                    ft.Container(
                                        width=36, height=36, border_radius=8,
                                        bgcolor="#DCFCE7",
                                        alignment=ft.Alignment(0, 0),
                                        content=ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED,
                                                        size=16, color=COLOR_GREEN_SUCCESS),
                                    ),
                                    ft.Column(spacing=1, tight=True, controls=[
                                        ft.Text("Total del pedido", size=12,
                                                weight="bold", color="#166534"),
                                        ft.Text("Pago registrado", size=11,
                                                color="#4ADE80"),
                                    ]),
                                ]),
                                ft.Text(order["total"], size=17,
                                        weight="bold", color=COLOR_GREEN_SUCCESS),
                            ],
                        ),
                    ),
                    ft.Row(alignment=ft.MainAxisAlignment.END, controls=[
                        ft.Container(
                            padding=ft.Padding(18, 10, 18, 10),
                            border_radius=24, bgcolor=COLOR_GREEN_SUCCESS,
                            shadow=ft.BoxShadow(blur_radius=14, spread_radius=-4,
                                                color="#4016A34A", offset=ft.Offset(0, 5)),
                            on_click=on_completar if order.get("show_complete")
                                     else close_modal,
                            content=ft.Row(spacing=8, controls=[
                                ft.Icon(ft.Icons.CHECK_ROUNDED, size=15, color="white"),
                                ft.Text("Confirmar Entrega"
                                        if order.get("show_complete") else "Cerrar",
                                        size=13, weight="bold", color="white"),
                            ]),
                        ),
                    ]),
                ],
            ),
        )
        return ft.Stack(expand=True, controls=[
            ft.Container(expand=True, bgcolor="#40000000",
                         blur=ft.Blur(12, 12), on_click=close_modal),
            ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=card),
        ])

    def show_detail(order: dict):
        pedido_id = order.get("id")
        if not pedido_id:
            for p in getattr(page, "pedidos_data", []):
                if p.get("codigo") == order.get("order_id"):
                    pedido_id = p["id"]
                    break
        if not pedido_id:
            return
        ok2, detalle, msg2 = PedidosController.obtener_detalle(pedido_id)
        if not ok2 or detalle is None:
            return
        order["id"] = pedido_id
        modal = _order_detail_modal(order, detalle)
        if not modal_layer.current:
            return
        if len(modal_layer.current.controls) > 1:
            modal_layer.current.controls[1] = modal
        else:
            modal_layer.current.controls.append(modal)
        modal_layer.current.update()

    def on_search(e):
        search_state["value"] = e.control.value or ""
        # Búsqueda local sobre los datos ya cargados — no hace llamada al backend
        # para que funcione con fecha, estado, total, etc. en tiempo real
        _refresh_rows(search_state["value"])

    c = _get_contadores()

    # ── Contenido interior ────────────────────────────────────────────
    inner_col = ft.Column(
        spacing=16,
        controls=[
            ft.Column(spacing=4, controls=[
                ft.Text("Gestión de Pedidos",
                        size=24, weight="bold", color=COLOR_GRAY_DARK),
                ft.Text("Administra y confirma los pedidos de clientes",
                        size=13, color=COLOR_GRAY_TEXT),
            ]),
            ft.Container(ref=stats_ref, content=_build_stats(c)),
            ft.Container(
                bgcolor=COLOR_WHITE, border_radius=12,
                border=ft.Border.all(1, COLOR_GRAY_BORDER),
                padding=ft.Padding(14, 0, 14, 0),
                content=ft.Row(spacing=10, controls=[
                    ft.Icon(ft.Icons.SEARCH_ROUNDED, color=COLOR_GRAY_TEXT, size=18),
                    ft.TextField(
                        hint_text="Buscar por ID, cliente, estado, total, fecha (ej: 13 Mar 2026)...",
                        border=ft.InputBorder.NONE,
                        expand=True, height=44, text_size=13,
                        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
                        on_change=on_search,
                    ),
                ]),
            ),
            # Tabla — crece con el contenido, scroll interno
            ft.Container(
                bgcolor=COLOR_WHITE,
                border_radius=16,
                border=ft.Border.all(1, "#F3EFEA"),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        _build_table_header(),
                        ft.Column(
                            ref=rows_col,
                            spacing=0,
                            controls=build_rows(),
                        ),
                    ],
                ),
            ),
        ],
    )

    # ── Mismo patrón: Stack + top=0 para anclar al tope ──────────────
    def on_resize(e):
        if stats_ref.current:
            stats_ref.current.content = _build_stats(_get_contadores())
        _refresh_rows(search_state["value"])
        page.update()

    page.on_resize = on_resize

    base = ft.Stack(
        expand=True,
        controls=[
            ft.Container(expand=True, bgcolor=COLOR_BG_PAGE),
            ft.Container(
                top=0, left=0, right=0, bottom=0,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=0,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(_h_pad(), _v_pad(), _h_pad(), _v_pad()),
                            content=inner_col,
                        ),
                    ],
                ),
            ),
        ],
    )

    return ft.Stack(
        ref=modal_layer,
        expand=True,
        controls=[base],
    )