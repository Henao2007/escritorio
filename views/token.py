import flet as ft
from views.styles import (
    COLOR_ORANGE_PRIMARY,
    COLOR_ORANGE_LIGHT,
    COLOR_GRAY_DARK,
    COLOR_GRAY_MEDIUM,
    COLOR_GRAY_TEXT,
    COLOR_BG_PAGE,
    COLOR_BG_LIGHT,
    COLOR_WHITE,
    COLOR_GREEN_SUCCESS,
    COLOR_BLUE_INFO,
    COLOR_BLUE_LIGHT,
    COLOR_RED_ERROR,
    COLOR_RED_LIGHT,
    COLOR_GRAY_BORDER,
    show_toast,
)
from controllers.tokens import TokensController


def token_view(page: ft.Page):
    verified_panel_ref   = ft.Ref[ft.Container]()
    search_border_ref    = ft.Ref[ft.Container]()
    token_chip_ref       = ft.Ref[ft.Text]()
    recent_list_ref      = ft.Ref[ft.Row]()
    pending_row_ref      = ft.Ref[ft.Row]()
    pending_title_ref    = ft.Ref[ft.Text]()
    modal_layer          = ft.Ref[ft.Stack]()

    verified_client_ref  = ft.Ref[ft.Text]()
    verified_items_ref   = ft.Ref[ft.Text]()
    verified_payment_ref = ft.Ref[ft.Text]()

    current_token     = {"value": None}
    current_pedido_id = {"value": None}
    current_detalle   = {"value": None}

    # ── Cargar tokens desde la BD ─────────────────────────────────────
    ok, msg = TokensController.cargar_tokens(page)
    if not ok:
        print(f"[token_view] {msg}")
        page.tokens_data = []

    def _get_delivered():
        return [t for t in getattr(page, "tokens_data", [])
                if t.get("estado_pedido", "").lower() == "completado"]

    def _get_pending():
        return [t for t in getattr(page, "tokens_data", [])
                if t.get("estado_pedido", "").lower() in ("pendiente", "confirmado")]

    # ── Modal de detalle ──────────────────────────────────────────────
    def close_modal(e=None):
        if modal_layer.current and len(modal_layer.current.controls) > 1:
            modal_layer.current.controls = modal_layer.current.controls[:1]
            modal_layer.current.update()

    def open_modal_for_pedido(pedido_id: int):
        ok, detalle, msg_d = TokensController.obtener_detalle(pedido_id)
        if not ok or not detalle:
            show_toast(page, msg_d, type="error")
            return
        _show_modal(detalle)

    def _show_modal(detalle: dict):
        pedido    = detalle["pedido"]
        items     = detalle["items"]
        estado    = pedido.get("estado_pedido", "pendiente").lower()
        token_str = pedido.get("token", "—")

        estado_colors = {
            "pendiente":  ("#FEF3C7", COLOR_ORANGE_PRIMARY),
            "confirmado": (COLOR_BLUE_LIGHT, COLOR_BLUE_INFO),
            "completado": ("#DCFCE7", COLOR_GREEN_SUCCESS),
            "cancelado":  (COLOR_RED_LIGHT, COLOR_RED_ERROR),
        }
        bg_e, fg_e = estado_colors.get(estado, ("#F3F4F6", COLOR_GRAY_DARK))

        def _field(label, value):
            """Campo estilo input de solo lectura."""
            return ft.Container(
                expand=True,
                border=ft.Border.all(1, "#E5E7EB"),
                border_radius=8,
                padding=ft.Padding(12, 8, 12, 8),
                bgcolor=COLOR_WHITE,
                content=ft.Column(spacing=2, controls=[
                    ft.Text(label, size=10, color=COLOR_GRAY_TEXT),
                    ft.Text(value or "—", size=13, weight="bold", color=COLOR_GRAY_DARK),
                ])
            )

        def _field_dark(label, value):
            """Campo oscuro para sección cliente."""
            return ft.Container(
                expand=True,
                border=ft.Border.all(1, "#334155"),
                border_radius=8,
                padding=ft.Padding(12, 8, 12, 8),
                bgcolor="#1E3A5F",
                content=ft.Column(spacing=2, controls=[
                    ft.Text(label, size=10, color="#94A3B8"),
                    ft.Text(value or "—", size=13, weight="bold", color="white"),
                ])
            )

        def _item_row(it):
            img_src = it.get("imagen", "")
            subtotal = f"$ {float(it['subtotal']):,.0f}".replace(",", ".")
            precio   = f"$ {float(it['precio_unitario']):,.0f}".replace(",", ".")
            return ft.Column(spacing=4, controls=[
                ft.Text(it["menu_nombre"], size=14, weight="bold",
                        color=COLOR_ORANGE_PRIMARY),
                ft.Text(it.get("descripcion", ""), size=12, color=COLOR_GRAY_TEXT),
                ft.Text(
                    f"Cantidad: {it['cantidad']} x {precio}",
                    size=12, color=COLOR_GRAY_MEDIUM,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(subtotal, size=16, weight="bold",
                                color=COLOR_ORANGE_PRIMARY),
                    ]
                ),
            ])

        card = ft.Container(
            width=540, bgcolor=COLOR_WHITE, border_radius=16,
            shadow=ft.BoxShadow(blur_radius=40, spread_radius=0,
                                color="#50000000", offset=ft.Offset(0, 16)),
            content=ft.Column(
                spacing=0, tight=True,
                controls=[
                    # ── Cabecera blanca ───────────────────────────────
                    ft.Container(
                        padding=ft.Padding(24, 20, 24, 16),
                        border=ft.Border(
                            bottom=ft.BorderSide(1, "#F3F4F6")),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Column(spacing=4, controls=[
                                    ft.Text("Detalles del Pedido", size=20,
                                            weight="bold", color=COLOR_GRAY_DARK),
                                    ft.Text(
                                        "Información completa del pedido y cliente",
                                        size=12, color=COLOR_GRAY_TEXT),
                                ]),
                                ft.Container(
                                    width=28, height=28, border_radius=14,
                                    bgcolor="#F3F4F6",
                                    alignment=ft.Alignment.CENTER,
                                    on_click=close_modal,
                                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED,
                                                    size=16, color=COLOR_GRAY_DARK),
                                ),
                            ],
                        ),
                    ),
                    # ── Cuerpo scrolleable ────────────────────────────
                    ft.Container(
                        height=600,
                        content=ft.ListView(
                            expand=True, padding=ft.Padding(24, 16, 24, 24),
                            spacing=16,
                            controls=[
                                # Token naranja
                                ft.Container(
                                    bgcolor=COLOR_ORANGE_PRIMARY,
                                    border_radius=12,
                                    padding=ft.Padding(20, 18, 20, 18),
                                    content=ft.Column(
                                        spacing=4,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("TOKEN DE PEDIDO", size=11,
                                                    weight="bold", color="#FFDBB5",
                                                    text_align=ft.TextAlign.CENTER),
                                            ft.Text(token_str, size=34,
                                                    weight="bold", color="white",
                                                    text_align=ft.TextAlign.CENTER,
                                                    font_family="monospace"),
                                            ft.Text(
                                                f"ID: {pedido.get('codigo', '')}",
                                                size=12, color="#FFDBB5",
                                                text_align=ft.TextAlign.CENTER),
                                        ]
                                    )
                                ),
                                # Sección cliente (oscura)
                                ft.Container(
                                    bgcolor="#1E3A5F",
                                    border_radius=12,
                                    padding=ft.Padding(16, 14, 16, 14),
                                    content=ft.Column(spacing=12, controls=[
                                        ft.Row(spacing=10, controls=[
                                            ft.Container(
                                                width=34, height=34, border_radius=17,
                                                bgcolor=COLOR_ORANGE_PRIMARY,
                                                alignment=ft.Alignment.CENTER,
                                                content=ft.Icon(ft.Icons.PERSON,
                                                                size=18, color="white"),
                                            ),
                                            ft.Text("Información del Cliente",
                                                    size=14, weight="bold",
                                                    color="white"),
                                        ]),
                                        ft.Row(spacing=10, controls=[
                                            _field_dark("Nombre",
                                                        pedido.get("cliente_nombre", "")),
                                            _field_dark("Documento",
                                                        pedido.get("cliente_documento", "")),
                                        ]),
                                        ft.Container(
                                            border=ft.Border.all(1, "#334155"),
                                            border_radius=8,
                                            padding=ft.Padding(12, 8, 12, 8),
                                            bgcolor="#1E3A5F",
                                            content=ft.Column(spacing=2, controls=[
                                                ft.Text("Email", size=10,
                                                        color="#94A3B8"),
                                                ft.Text(
                                                    pedido.get("cliente_email", "—"),
                                                    size=13, weight="bold",
                                                    color="white"),
                                            ])
                                        ),
                                    ])
                                ),
                                # Sección info pedido
                                ft.Container(
                                    bgcolor=COLOR_WHITE,
                                    border_radius=12,
                                    border=ft.Border.all(1, "#F3F4F6"),
                                    padding=ft.Padding(16, 14, 16, 14),
                                    content=ft.Column(spacing=12, controls=[
                                        ft.Row(spacing=10, controls=[
                                            ft.Container(
                                                width=34, height=34, border_radius=17,
                                                bgcolor="#DCFCE7",
                                                alignment=ft.Alignment.CENTER,
                                                content=ft.Icon(
                                                    ft.Icons.RECEIPT_LONG_OUTLINED,
                                                    size=18, color=COLOR_GREEN_SUCCESS),
                                            ),
                                            ft.Text("Información del Pedido",
                                                    size=14, weight="bold",
                                                    color=COLOR_GRAY_DARK),
                                        ]),
                                        ft.Row(spacing=10, controls=[
                                            _field("Fecha", pedido.get("fecha", "")),
                                            _field("Hora",  pedido.get("hora", "")),
                                        ]),
                                        ft.Row(spacing=10, controls=[
                                            _field("Método de Pago",
                                                   pedido.get("metodo_pago", "")),
                                            ft.Container(
                                                expand=True,
                                                border=ft.Border.all(1, "#E5E7EB"),
                                                border_radius=8,
                                                padding=ft.Padding(12, 8, 12, 8),
                                                bgcolor=COLOR_WHITE,
                                                content=ft.Column(spacing=4, controls=[
                                                    ft.Text("Estado", size=10,
                                                            color=COLOR_GRAY_TEXT),
                                                    ft.Container(
                                                        bgcolor=bg_e, border_radius=6,
                                                        padding=ft.Padding(8, 3, 8, 3),
                                                        content=ft.Text(
                                                            estado.capitalize(),
                                                            size=12, weight="bold",
                                                            color=fg_e),
                                                    )
                                                ])
                                            ),
                                        ]),
                                    ])
                                ),
                                # Comprobante de pago
                                ft.Container(
                                    bgcolor="#F5F3FF",
                                    border_radius=12,
                                    border=ft.Border.all(1, "#DDD6FE"),
                                    padding=ft.Padding(16, 14, 16, 14),
                                    content=ft.Column(spacing=10, controls=[
                                        ft.Row(spacing=10, controls=[
                                            ft.Container(
                                                width=34, height=34, border_radius=17,
                                                bgcolor="#EDE9FE",
                                                alignment=ft.Alignment.CENTER,
                                                content=ft.Icon(
                                                    ft.Icons.PAYMENT_OUTLINED,
                                                    size=18, color="#7C3AED"),
                                            ),
                                            ft.Text(
                                                f"Comprobante de Pago "
                                                f"{pedido.get('metodo_pago', '')}",
                                                size=14, weight="bold",
                                                color="#4C1D95"),
                                        ]),
                                        ft.Container(
                                            bgcolor="#EDE9FE", border_radius=10,
                                            height=100, alignment=ft.Alignment.CENTER,
                                            content=ft.Column(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                spacing=4,
                                                controls=[
                                                    ft.Icon(ft.Icons.IMAGE_OUTLINED,
                                                            size=32, color="#7C3AED"),
                                                    ft.Text(
                                                        "Comprobante no disponible",
                                                        size=11, color="#7C3AED"),
                                                ]
                                            )
                                        ),
                                    ])
                                ),
                                # Productos
                                ft.Container(
                                    bgcolor=COLOR_WHITE,
                                    border_radius=12,
                                    border=ft.Border.all(1, "#F3F4F6"),
                                    padding=ft.Padding(16, 14, 16, 14),
                                    content=ft.Column(spacing=12, controls=[
                                        ft.Row(spacing=10, controls=[
                                            ft.Container(
                                                width=34, height=34, border_radius=17,
                                                bgcolor=COLOR_ORANGE_LIGHT,
                                                alignment=ft.Alignment.CENTER,
                                                content=ft.Icon(
                                                    ft.Icons.FASTFOOD_OUTLINED,
                                                    size=18, color=COLOR_ORANGE_PRIMARY),
                                            ),
                                            ft.Text("Productos del Pedido", size=14,
                                                    weight="bold", color=COLOR_GRAY_DARK),
                                        ]),
                                        *([_item_row(it) for it in items]
                                          if items else [
                                            ft.Text("Sin ítems registrados",
                                                    size=13, color=COLOR_GRAY_TEXT)
                                          ]),
                                        ft.Divider(height=1, color="#F3F4F6"),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text("Total del Pedido", size=14,
                                                        weight="bold",
                                                        color=COLOR_GRAY_DARK),
                                                ft.Text(
                                                    f"$ {float(pedido.get('total', 0)):,.0f}"
                                                    .replace(",", "."),
                                                    size=20, weight="bold",
                                                    color=COLOR_ORANGE_PRIMARY),
                                            ]
                                        ),
                                    ])
                                ),
                                # Botón cerrar
                                ft.Container(
                                    height=44, border_radius=22,
                                    bgcolor=COLOR_WHITE,
                                    border=ft.Border.all(1, "#E5E7EB"),
                                    on_click=close_modal,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("Cerrar", size=14,
                                                    color=COLOR_GRAY_MEDIUM,
                                                    weight="bold")
                                        ],
                                    ),
                                ),
                            ]
                        )
                    ),
                ]
            )
        )

        modal = ft.Stack(
            expand=True,
            controls=[
                ft.Container(expand=True, bgcolor="#60000000",
                             on_click=close_modal),
                ft.Container(
                    expand=True, alignment=ft.Alignment.CENTER,
                    content=card,
                ),
            ],
        )

        if not modal_layer.current:
            return
        if len(modal_layer.current.controls) > 1:
            modal_layer.current.controls[1] = modal
        else:
            modal_layer.current.controls.append(modal)
        modal_layer.current.update()

    # ── Token card con botón Ver Detalles ─────────────────────────────
    def _token_card_with_detail(t: dict):
        estado = t.get("estado_pedido", "pendiente").lower()
        status_label = {
            "completado": "Entregado",
            "confirmado": "Confirmado",
            "pendiente":  "Pendiente",
            "cancelado":  "Cancelado",
        }.get(estado, estado.capitalize())

        estado_colors = {
            "pendiente":  ("#FEF3C7", COLOR_ORANGE_PRIMARY),
            "confirmado": (COLOR_BLUE_LIGHT, COLOR_BLUE_INFO),
            "completado": ("#DCFCE7", COLOR_GREEN_SUCCESS),
            "cancelado":  (COLOR_RED_LIGHT, COLOR_RED_ERROR),
        }
        bg_e, fg_e = estado_colors.get(estado, ("#F3F4F6", COLOR_GRAY_DARK))
        total  = f"$ {float(t.get('total', 0)):,.0f}".replace(",", ".")
        pid    = t.get("pedido_id")

        return ft.Container(
            width=280, bgcolor="#FFF7ED", border_radius=16, padding=20,
            border=ft.Border.all(1, "#FFEDD5"),
            content=ft.Column(spacing=12, controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            bgcolor=COLOR_WHITE,
                            padding=ft.Padding(12, 6, 12, 6),
                            border_radius=8,
                            border=ft.Border.all(1, "#E5E7EB"),
                            content=ft.Text(t.get("token", ""), weight="bold",
                                            size=13, color=COLOR_GRAY_DARK),
                        ),
                        ft.Container(
                            bgcolor=bg_e,
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=6,
                            content=ft.Text(status_label, size=10,
                                            weight="bold", color=fg_e),
                        ),
                    ],
                ),
                ft.Column(spacing=4, controls=[
                    ft.Text("Cliente", size=10, color=COLOR_GRAY_TEXT),
                    ft.Text(t.get("cliente_nombre", ""), size=13,
                            weight="bold", color=COLOR_GRAY_MEDIUM),
                ]),
                ft.Column(spacing=4, controls=[
                    ft.Text("Pedido", size=10, color=COLOR_GRAY_TEXT),
                    ft.Text(f"1 items • {total}", size=13,
                            weight="bold", color=COLOR_GRAY_MEDIUM),
                ]),
                ft.Column(spacing=4, controls=[
                    ft.Text("Hora", size=10, color=COLOR_GRAY_TEXT),
                    ft.Text(t.get("fecha_generacion", ""), size=13,
                            weight="bold", color=COLOR_GRAY_MEDIUM),
                ]),
                # Botón Ver Detalles
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    border_radius=8,
                    border=ft.Border.all(1, "#E5E7EB"),
                    padding=ft.Padding(0, 8, 0, 8),
                    on_click=lambda e, p=pid: open_modal_for_pedido(p),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6,
                        controls=[
                            ft.Icon(ft.Icons.VISIBILITY_OUTLINED,
                                    size=14, color=COLOR_GRAY_MEDIUM),
                            ft.Text("Ver Detalles", size=12,
                                    color=COLOR_GRAY_MEDIUM),
                        ]
                    )
                ),
            ]),
        )

    def _rebuild_token_lists():
        if recent_list_ref.current:
            delivered = _get_delivered()
            recent_list_ref.current.controls = (
                [_token_card_with_detail(t) for t in delivered]
                if delivered else
                [ft.Text("No hay entregas recientes", size=13,
                         color=COLOR_GRAY_TEXT)]
            )
            recent_list_ref.current.update()

        if pending_row_ref.current:
            pending = _get_pending()
            pending_row_ref.current.controls = (
                [_token_card_with_detail(t) for t in pending]
                if pending else
                [ft.Text("Sin pedidos pendientes", size=13,
                         color=COLOR_GRAY_TEXT)]
            )
            pending_row_ref.current.update()

        if pending_title_ref.current:
            pending_title_ref.current.value = (
                f"Pedidos Pendientes de Entrega ({len(_get_pending())})"
            )
            pending_title_ref.current.update()

    # ── Campo de búsqueda ─────────────────────────────────────────────
    def on_token_change(e):
        chars = "".join(ch for ch in (e.control.value or "").upper()
                        if ch.isalnum() or ch == "-")
        if chars != e.control.value:
            e.control.value = chars
            e.control.update()

    def on_focus(e):
        if search_border_ref.current:
            search_border_ref.current.border = ft.Border.all(1.5, COLOR_ORANGE_PRIMARY)
            search_border_ref.current.bgcolor = "#FFF7ED"
            search_border_ref.current.update()

    def on_blur(e):
        if search_border_ref.current:
            search_border_ref.current.border = ft.Border.all(1, "#F3EFEA")
            search_border_ref.current.bgcolor = COLOR_WHITE
            search_border_ref.current.update()

    def on_verify_click(e):
        token_val = (token_input.value or "").strip().upper()
        if not token_val:
            show_toast(page, "Por favor ingresa un token",
                       "Campo requerido", type="error")
            return

        encontrado = None
        for t in getattr(page, "tokens_data", []):
            if t.get("token", "").upper() == token_val:
                encontrado = t
                break

        if encontrado is None:
            show_toast(page, f"Token '{token_val}' no encontrado",
                       "Token inválido", type="error")
            return

        estado = encontrado.get("estado_pedido", "").lower()
        if estado == "completado":
            show_toast(page, "Este pedido ya fue entregado",
                       "Token usado", type="error")
            return
        if estado == "cancelado":
            show_toast(page, "Este pedido fue cancelado",
                       "Token cancelado", type="error")
            return

        current_token["value"]     = token_val
        current_pedido_id["value"] = encontrado.get("pedido_id")

        ok, detalle, msg_d = TokensController.obtener_detalle(
            encontrado.get("pedido_id"))
        if ok and detalle:
            current_detalle["value"] = detalle
            pedido  = detalle["pedido"]
            items   = detalle["items"]
            total   = f"$ {float(pedido.get('total', 0)):,.0f}".replace(",", ".")
            n_items = len(items)
            metodo  = pedido.get("metodo_pago", "No registrado")
            cliente = pedido.get("cliente_nombre", "—")
        else:
            current_detalle["value"] = None
            total   = f"$ {float(encontrado.get('total', 0)):,.0f}".replace(",", ".")
            n_items = 0
            metodo  = "—"
            cliente = encontrado.get("cliente_nombre", "—")

        if token_chip_ref.current:
            token_chip_ref.current.value = token_val
            token_chip_ref.current.update()
        if verified_client_ref.current:
            verified_client_ref.current.value = cliente
            verified_client_ref.current.update()
        if verified_items_ref.current:
            verified_items_ref.current.value = (
                f"{n_items} item{'s' if n_items != 1 else ''} • {total}"
            )
            verified_items_ref.current.update()
        if verified_payment_ref.current:
            verified_payment_ref.current.value = metodo
            verified_payment_ref.current.update()

        if verified_panel_ref.current:
            verified_panel_ref.current.visible = True
            verified_panel_ref.current.update()

        show_toast(page, f"Token {token_val} verificado correctamente",
                   "Token verificado")

    token_input = ft.TextField(
        hint_text="INGRESA EL TOKEN DEL CLIENTE (EJ: TK-A3F2B1)",
        expand=True, border=ft.InputBorder.NONE, text_size=14,
        color=COLOR_GRAY_MEDIUM,
        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
        on_change=on_token_change, on_focus=on_focus, on_blur=on_blur,
    )

    search_container = ft.Container(
        ref=search_border_ref,
        bgcolor=COLOR_WHITE, padding=ft.Padding(24, 12, 24, 12),
        border_radius=999, border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Row(
            spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SEARCH_ROUNDED, color=COLOR_GRAY_TEXT, size=20),
                token_input,
                ft.Container(
                    content=ft.Text("Verificar Token", color="white",
                                    weight="bold", size=14),
                    bgcolor=COLOR_ORANGE_PRIMARY,
                    padding=ft.Padding(20, 10, 20, 10),
                    border_radius=18, on_click=on_verify_click,
                ),
            ],
        ),
    )

    # ── Confirmar → pendiente a confirmado ────────────────────────────
    def on_confirm_delivery(e):
        pedido_id = current_pedido_id["value"]
        if not pedido_id:
            show_toast(page, "Primero verifica un token", "Sin token", type="error")
            return

        ok, msg = TokensController.confirmar_token(page, pedido_id)
        if ok:
            if verified_panel_ref.current:
                verified_panel_ref.current.visible = False
                verified_panel_ref.current.update()
            token_input.value = ""
            token_input.update()
            current_token["value"]     = None
            current_pedido_id["value"] = None
            current_detalle["value"]   = None
            _rebuild_token_lists()
            show_toast(page, "Pedido confirmado correctamente", "Confirmado ✓")
        else:
            show_toast(page, msg, "Error", type="error")

    def on_ver_detalle_panel(e):
        if current_detalle["value"]:
            _show_modal(current_detalle["value"])

    # ── Panel verde ───────────────────────────────────────────────────
    verified_panel = ft.Container(
        ref=verified_panel_ref, visible=False,
        bgcolor="#ECFDF3", border_radius=20, padding=24,
        border=ft.Border.all(1, "#BBF7D0"),
        content=ft.Column(spacing=14, controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(spacing=10, controls=[
                        ft.Container(
                            width=32, height=32, border_radius=16,
                            bgcolor="#D1FAE5", alignment=ft.Alignment.CENTER,
                            content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED,
                                            size=20, color=COLOR_GREEN_SUCCESS),
                        ),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Token Verificado", size=16, weight="bold",
                                    color=COLOR_GRAY_DARK),
                            ft.Text("El pedido está listo para confirmar",
                                    size=12, color=COLOR_GRAY_TEXT),
                        ]),
                    ]),
                    ft.Container(
                        bgcolor=COLOR_WHITE, padding=ft.Padding(12, 4, 12, 4),
                        border_radius=999, border=ft.Border.all(1, "#E5E7EB"),
                        content=ft.Text("—", size=13, weight="bold",
                                        color=COLOR_GRAY_DARK, ref=token_chip_ref),
                    ),
                ],
            ),
            ft.Container(
                bgcolor=COLOR_WHITE, border_radius=16, padding=18,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(spacing=8, controls=[
                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=18,
                                    color=COLOR_GRAY_MEDIUM),
                            ft.Column(spacing=2, controls=[
                                ft.Text("—", size=14, weight="bold",
                                        color=COLOR_GRAY_DARK,
                                        ref=verified_client_ref),
                                ft.Text("—", size=12, color=COLOR_GRAY_TEXT,
                                        ref=verified_items_ref),
                            ]),
                        ]),
                        ft.Column(
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Text("Método de pago", size=11, color=COLOR_GRAY_TEXT),
                                ft.Text("—", size=13, weight="bold",
                                        color=COLOR_GRAY_MEDIUM,
                                        ref=verified_payment_ref),
                            ]
                        ),
                    ],
                ),
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END, spacing=12,
                controls=[
                    ft.Container(
                        bgcolor=COLOR_WHITE, border_radius=24,
                        padding=ft.Padding(20, 10, 20, 10),
                        border=ft.Border.all(1, COLOR_GRAY_BORDER),
                        on_click=on_ver_detalle_panel,
                        content=ft.Row(spacing=8, controls=[
                            ft.Icon(ft.Icons.VISIBILITY_OUTLINED,
                                    size=16, color=COLOR_GRAY_MEDIUM),
                            ft.Text("Ver detalles", size=14, weight="bold",
                                    color=COLOR_GRAY_MEDIUM),
                        ]),
                    ),
                    ft.Container(
                        bgcolor=COLOR_GREEN_SUCCESS, border_radius=24,
                        padding=ft.Padding(22, 10, 22, 10),
                        shadow=ft.BoxShadow(blur_radius=18, spread_radius=-4,
                                            color="#4016A34A", offset=ft.Offset(0, 6)),
                        on_click=on_confirm_delivery,
                        content=ft.Row(spacing=8, controls=[
                            ft.Icon(ft.Icons.CHECK_ROUNDED, size=18, color="white"),
                            ft.Text("Confirmar Entrega del Pedido", size=14,
                                    weight="bold", color="white"),
                        ]),
                    ),
                ]
            ),
        ]),
    )

    main_content = ft.Column(
        scroll=ft.ScrollMode.AUTO, spacing=24, expand=True,
        controls=[
            ft.Column(spacing=4, controls=[
                ft.Text("Verificación de Tokens", size=28, weight="bold",
                        color="#1E293B"),
                ft.Text("Verifica los tokens de los clientes para confirmar pedidos",
                        size=14, color=COLOR_GRAY_TEXT),
            ]),
            search_container,
            verified_panel,
            ft.Container(
                bgcolor=COLOR_WHITE, padding=24, border_radius=16,
                border=ft.Border.all(1, "#F3EFEA"),
                content=ft.Column(spacing=15, controls=[
                    ft.Text("Entregas Recientes", size=16, weight="bold",
                            color=COLOR_GRAY_MEDIUM),
                    ft.Row(
                        ref=recent_list_ref, wrap=True,
                        spacing=12, run_spacing=12,
                        controls=(
                            [_token_card_with_detail(t) for t in _get_delivered()]
                            or [ft.Text("No hay entregas recientes", size=13,
                                        color=COLOR_GRAY_TEXT)]
                        ),
                    ),
                ]),
            ),
            ft.Container(
                bgcolor=COLOR_WHITE, padding=24, border_radius=16,
                border=ft.Border.all(1, "#F3EFEA"),
                content=ft.Column(spacing=20, controls=[
                    ft.Text(
                        f"Pedidos Pendientes de Entrega ({len(_get_pending())})",
                        size=16, weight="bold", color=COLOR_GRAY_MEDIUM,
                        ref=pending_title_ref,
                    ),
                    ft.Row(
                        ref=pending_row_ref, wrap=True,
                        spacing=20, run_spacing=12,
                        controls=(
                            [_token_card_with_detail(t) for t in _get_pending()]
                            or [ft.Text("Sin pedidos pendientes", size=13,
                                        color=COLOR_GRAY_TEXT)]
                        ),
                    ),
                ]),
            ),
            ft.Container(height=20),
        ],
    )

    base_content = ft.Container(
        expand=True, padding=40, bgcolor=COLOR_BG_PAGE,
        content=main_content,
    )

    return ft.Stack(
        ref=modal_layer, expand=True,
        controls=[base_content],
    )