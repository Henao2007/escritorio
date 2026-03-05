import flet as ft
from .styles import (
    COLOR_ORANGE_PRIMARY,
    COLOR_GRAY_DARK,
    COLOR_GRAY_MEDIUM,
    COLOR_GRAY_TEXT,
    COLOR_BG_PAGE,
    COLOR_WHITE,
    COLOR_GREEN_SUCCESS,
    COLOR_ORANGE_LIGHT,
    token_card,
    show_toast,
)


def token_view(page: ft.Page):
    verified_panel_ref = ft.Ref[ft.Container]()
    search_border_ref = ft.Ref[ft.Container]()
    token_chip_ref = ft.Ref[ft.Text]()

    # Historial dinámico de tokens
    delivered_tokens = [
        {
            "token_id": "REY-PG-Z7",
            "status": "Entregado",
            "client": "Usuario Demo",
            "order_info": "1 items • $ 8.600",
            "time_text": "08:29 a. m.",
        },
        {
            "token_id": "1PS-AL-VB",
            "status": "Entregado",
            "client": "Usuario Demo",
            "order_info": "1 items • $ 8.600",
            "time_text": "08:49 a. m.",
        },
    ]

    pending_tokens = [
        {
            "token_id": "QHH-8M-WE",
            "status": "Pendiente",
            "client": "Usuario Demo",
            "order_info": "1 items • $ 8.600",
            "time_text": "08:50 a. m.",
        }
    ]

    # ✅ CAMBIO: Ref ahora apunta a ft.Row en lugar de ft.Column
    recent_list_ref = ft.Ref[ft.Row]()
    pending_row_ref = ft.Ref[ft.Row]()
    pending_title_ref = ft.Ref[ft.Text]()

    # Estado simple para el token verificado
    current_token = {"value": None}

    def _rebuild_token_lists():
        """Reconstruye las listas de entregas recientes y pendientes."""
        if recent_list_ref.current:
            recent_list_ref.current.controls = [
                token_card(
                    token_id=t["token_id"],
                    status=t["status"],
                    client=t["client"],
                    order_info=t["order_info"],
                    time_text=t["time_text"],
                )
                for t in delivered_tokens
            ]
            recent_list_ref.current.update()

        if pending_row_ref.current:
            pending_row_ref.current.controls = [
                token_card(
                    token_id=t["token_id"],
                    status=t["status"],
                    client=t["client"],
                    order_info=t["order_info"],
                    time_text=t["time_text"],
                )
                for t in pending_tokens
            ]
            pending_row_ref.current.update()

        if pending_title_ref.current:
            count = len(pending_tokens)
            pending_title_ref.current.value = (
                f"Pedidos Pendientes de Entrega ({count})"
            )
            pending_title_ref.current.update()

    def format_token(raw: str) -> str:
        # Deja solo letras/números y los pone en mayúscula
        chars = "".join(ch for ch in raw.upper() if ch.isalnum())
        # Formato tipo QHH-8M-WE (3-2-2)
        parts = []
        if len(chars) > 0:
            parts.append(chars[:3])
        if len(chars) > 3:
            parts.append(chars[3:5])
        if len(chars) > 5:
            parts.append(chars[5:7])
        return "-".join(parts)

    def on_token_change(e: ft.ControlEvent):
        formatted = format_token(e.control.value or "")
        if formatted != e.control.value:
            e.control.value = formatted
            e.control.update()

    def on_focus(e: ft.ControlEvent):
        if search_border_ref.current:
            search_border_ref.current.border = ft.Border.all(1.5, COLOR_ORANGE_PRIMARY)
            search_border_ref.current.bgcolor = "#FFF7ED"
            search_border_ref.current.update()

    def on_blur(e: ft.ControlEvent):
        if search_border_ref.current:
            search_border_ref.current.border = ft.Border.all(1, "#F3EFEA")
            search_border_ref.current.bgcolor = COLOR_WHITE
            search_border_ref.current.update()

    def on_verify_click(e):
        if not token_input.value:
            show_toast(
                page,
                "Por favor ingresa un token",
                "Campo requerido",
                type="error",
            )
            return

        current_token["value"] = token_input.value
        if verified_panel_ref.current:
            verified_panel_ref.current.visible = True
            verified_panel_ref.current.update()
        if token_chip_ref.current:
            token_chip_ref.current.value = current_token["value"]
            token_chip_ref.current.update()

        show_toast(
            page,
            f"Token {token_input.value} verificado correctamente",
            "Token verificado",
        )

    token_input = ft.TextField(
        hint_text="INGRESA EL TOKEN DEL CLIENTE (EJ: A1B-2C3-4D5)",
        expand=True,
        border=ft.InputBorder.NONE,
        text_size=14,
        color=COLOR_GRAY_MEDIUM,
        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
        on_change=on_token_change,
        on_focus=on_focus,
        on_blur=on_blur,
    )

    search_container = ft.Container(
        ref=search_border_ref,
        bgcolor=COLOR_WHITE,
        padding=ft.Padding(24, 12, 24, 12),
        border_radius=999,
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SEARCH_ROUNDED, color=COLOR_GRAY_TEXT, size=20),
                token_input,
                ft.Text(
                    "0/9",
                    size=11,
                    color=COLOR_GRAY_TEXT,
                ),
                ft.Container(
                    content=ft.Text(
                        "Verificar Token",
                        color="white",
                        weight="bold",
                        size=14,
                    ),
                    bgcolor="#FDBA74",
                    padding=ft.Padding(20, 10, 20, 10),
                    border_radius=18,
                    on_click=on_verify_click,
                ),
            ],
        ),
    )

    def on_confirm_delivery(e):
        """Confirma la entrega del pedido asociado al token verificado."""
        if not current_token["value"]:
            show_toast(
                page,
                "Primero verifica un token antes de confirmar la entrega.",
                "Sin token verificado",
                type="error",
            )
            return

        tk = current_token["value"]

        # Mover de pendientes a entregados si existe
        moved = False
        for i, t in enumerate(pending_tokens):
            if t["token_id"] == tk:
                moved_token = pending_tokens.pop(i)
                moved_token["status"] = "Entregado"
                delivered_tokens.insert(0, moved_token)
                moved = True
                break

        # Si no estaba en pendientes, lo añadimos directamente como entregado
        if not moved:
            delivered_tokens.insert(
                0,
                {
                    "token_id": tk,
                    "status": "Entregado",
                    "client": "Usuario Demo",
                    "order_info": "1 items • $ 8.600",
                    "time_text": "Ahora",
                },
            )

        _rebuild_token_lists()

        show_toast(
            page,
            f"Entrega del token {tk} confirmada correctamente",
            "Pedido entregado",
        )

    verified_panel = ft.Container(
        ref=verified_panel_ref,
        visible=False,
        bgcolor="#ECFDF3",
        border_radius=20,
        padding=24,
        border=ft.Border.all(1, "#BBF7D0"),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Container(
                                    width=32,
                                    height=32,
                                    border_radius=16,
                                    bgcolor="#D1FAE5",
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(
                                        ft.Icons.CHECK_CIRCLE_ROUNDED,
                                        size=20,
                                        color=COLOR_GREEN_SUCCESS,
                                    ),
                                ),
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            "Token Verificado",
                                            size=16,
                                            weight="bold",
                                            color=COLOR_GRAY_DARK,
                                        ),
                                        ft.Text(
                                            "El pedido está listo para entregar al cliente",
                                            size=12,
                                            color=COLOR_GRAY_TEXT,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(
                            bgcolor=COLOR_WHITE,
                            padding=ft.Padding(12, 4, 12, 4),
                            border_radius=999,
                            border=ft.Border.all(1, "#E5E7EB"),
                            content=ft.Text(
                                "QHH-8M-WE",
                                size=13,
                                weight="bold",
                                color=COLOR_GRAY_DARK,
                                ref=token_chip_ref,
                            ),
                        ),
                    ],
                ),
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    border_radius=16,
                    padding=18,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        spacing=8,
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.PERSON_OUTLINE,
                                                size=18,
                                                color=COLOR_GRAY_MEDIUM,
                                            ),
                                            ft.Column(
                                                spacing=2,
                                                controls=[
                                                    ft.Text(
                                                        "Usuario Demo",
                                                        size=14,
                                                        weight="bold",
                                                        color=COLOR_GRAY_DARK,
                                                    ),
                                                    ft.Text(
                                                        "1 items • $ 8.600",
                                                        size=12,
                                                        color=COLOR_GRAY_TEXT,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                        controls=[
                                            ft.Text(
                                                "Método de pago",
                                                size=11,
                                                color=COLOR_GRAY_TEXT,
                                            ),
                                            ft.Text(
                                                "Nequi",
                                                size=13,
                                                weight="bold",
                                                color=COLOR_GRAY_MEDIUM,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=ft.Container(
                        bgcolor=COLOR_GREEN_SUCCESS,
                        border_radius=24,
                        padding=ft.Padding(22, 10, 22, 10),
                        shadow=ft.BoxShadow(
                            blur_radius=18,
                            spread_radius=-4,
                            color="#4016A34A",
                            offset=ft.Offset(0, 6),
                        ),
                        on_click=on_confirm_delivery,
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
                    ),
                ),
            ],
        ),
    )

    main_content = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=24,
        expand=True,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    ft.Text(
                        "Verificación de Tokens",
                        size=28,
                        weight="bold",
                        color="#1E293B",
                    ),
                    ft.Text(
                        "Verifica los tokens de los clientes para entregar pedidos",
                        size=14,
                        color=COLOR_GRAY_TEXT,
                    ),
                ],
            ),
            search_container,
            verified_panel,
            ft.Container(
                bgcolor=COLOR_WHITE,
                padding=24,
                border_radius=16,
                border=ft.Border.all(1, "#F3EFEA"),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Text(
                            "Entregas Recientes",
                            size=16,
                            weight="bold",
                            color=COLOR_GRAY_MEDIUM,
                        ),
                        # ✅ CAMBIO: ft.Column → ft.Row con wrap=True
                        ft.Row(
                            ref=recent_list_ref,
                            wrap=True,
                            spacing=12,
                            run_spacing=12,
                            controls=[
                                token_card(
                                    token_id=t["token_id"],
                                    status=t["status"],
                                    client=t["client"],
                                    order_info=t["order_info"],
                                    time_text=t["time_text"],
                                )
                                for t in delivered_tokens
                            ],
                        ),
                    ],
                ),
            ),
            ft.Container(
                bgcolor=COLOR_WHITE,
                padding=24,
                border_radius=16,
                border=ft.Border.all(1, "#F3EFEA"),
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Text(
                            "Pedidos Pendientes de Entrega (1)",
                            size=16,
                            weight="bold",
                            color=COLOR_GRAY_MEDIUM,
                            ref=pending_title_ref,
                        ),
                        ft.Row(
                            ref=pending_row_ref,
                            wrap=True,
                            spacing=20,
                            run_spacing=12,
                            controls=[
                                token_card(
                                    token_id=t["token_id"],
                                    status=t["status"],
                                    client=t["client"],
                                    order_info=t["order_info"],
                                    time_text=t["time_text"],
                                )
                                for t in pending_tokens
                            ],
                        ),
                    ],
                ),
            ),
            ft.Container(
                alignment=ft.Alignment.CENTER_RIGHT,
                padding=ft.Padding.only(top=4, right=4),
                content=ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_size=18,
                    icon_color=COLOR_GRAY_TEXT,
                    tooltip="Limpiar historial de tokens",
                    on_click=lambda e: (
                        delivered_tokens.clear(),
                        pending_tokens.clear(),
                        _rebuild_token_lists(),
                    ),
                ),
            ),
            ft.Container(height=20),
        ],
    )

    return ft.Container(
        expand=True,
        padding=40,
        bgcolor=COLOR_BG_PAGE,
        content=main_content,
    )