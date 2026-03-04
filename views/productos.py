import flet as ft
from views.styles import (
    COLOR_ORANGE_PRIMARY,
    COLOR_ORANGE_LIGHT,
    COLOR_ORANGE_DARK,
    COLOR_GREEN_SUCCESS,
    COLOR_GREEN_LIGHT,
    COLOR_RED_ERROR,
    COLOR_RED_LIGHT,
    COLOR_BLUE_INFO,
    COLOR_BLUE_LIGHT,
    COLOR_GRAY_DARK,
    COLOR_GRAY_MEDIUM,
    COLOR_GRAY_TEXT,
    COLOR_GRAY_BORDER,
    COLOR_BG_PAGE,
    COLOR_BG_LIGHT,
    COLOR_WHITE,
    show_toast,
)

# ─── Sample product data (will be replaced by DB later) ───────────────────────
SAMPLE_PRODUCTS = [
    {
        "id": 1,
        "name": "Almuerzo Ejecutivo",
        "description": "Incluye arroz, carne de res a la plancha, ensalada fresca y bebida natural",
        "price": "$ 8.600",
        "category": "specialty",
        "image": "img/comida1.jpg",
        "available": True,
    },
    {
        "id": 2,
        "name": "Almuerzo Especial Pollo",
        "description": "Incluye arroz, pollo a la plancha marinado, ensalada fresca y bebida natural",
        "price": "$ 8.600",
        "category": "specialty",
        "image": "img/comida2.jpg",
        "available": True,
    },
    {
        "id": 3,
        "name": "Almuerzo Especial Pescado",
        "description": "Incluye arroz, filete de pescado al horno, ensalada fresca y bebida natural",
        "price": "$ 9.500",
        "category": "specialty",
        "image": "img/comida1.jpg",
        "available": True,
    },
    {
        "id": 4,
        "name": "Bandeja Paisa",
        "description": "Frijoles, arroz, chicharrón, carne molida, chorizo, arepa y huevo",
        "price": "$ 12.000",
        "category": "specialty",
        "image": "img/comida2.jpg",
        "available": False,
    },
    {
        "id": 5,
        "name": "Sopa del Día",
        "description": "Sopa tradicional colombiana con verduras frescas y proteína del día",
        "price": "$ 6.500",
        "category": "specialty",
        "image": "img/comida1.jpg",
        "available": True,
    },
    {
        "id": 6,
        "name": "Jugo Natural",
        "description": "Jugo de fruta de temporada preparado al momento con agua o leche",
        "price": "$ 3.000",
        "category": "specialty",
        "image": "img/comida2.jpg",
        "available": True,
    },
]


# ─── Availability badge ───────────────────────────────────────────────────────
def _avail_badge(available: bool, on_click=None):
    return ft.Container(
        bgcolor=COLOR_GREEN_SUCCESS if available else COLOR_RED_ERROR,
        border_radius=20,
        padding=ft.Padding(10, 4, 10, 4),
        on_click=on_click,
        content=ft.Text(
            "Disponible" if available else "No disponible",
            size=11, weight="bold", color="white",
        ),
    )


# ─── Product card ─────────────────────────────────────────────────────────────
def _product_card(product: dict, on_edit, on_delete, on_toggle):
    avail = product["available"]
    card_ref = ft.Ref[ft.Container]()

    def on_hover(e):
        card_ref.current.shadow = ft.BoxShadow(
            blur_radius=24, spread_radius=0,
            color="#30000000", offset=ft.Offset(0, 8)
        ) if e.data == "true" else ft.BoxShadow(
            blur_radius=8, spread_radius=0,
            color="#18000000", offset=ft.Offset(0, 2)
        )
        card_ref.current.update()

    return ft.Container(
        ref=card_ref,
        width=310,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        border=ft.Border.all(1, "#F3EFEA"),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(
            blur_radius=8, spread_radius=0,
            color="#18000000", offset=ft.Offset(0, 2)
        ),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        on_hover=on_hover,
        content=ft.Column(
            spacing=0,
            controls=[
                # Image + availability badge
                ft.Stack(
                    height=185,
                    controls=[
                        ft.Container(
                            expand=True,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=product["image"],
                                width=310,
                                height=185,
                                fit=ft.BoxFit.COVER,
                            ),
                        ),
                        ft.Container(
                            top=12,
                            right=12,
                            content=_avail_badge(
                                avail, on_click=lambda e, p=product: on_toggle(p)
                            ),
                        ),
                    ],
                ),
                # Card body
                ft.Container(
                    padding=ft.Padding(16, 14, 16, 14),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            # Category badge
                            ft.Container(
                                bgcolor=COLOR_ORANGE_LIGHT,
                                border_radius=6,
                                padding=ft.Padding(8, 3, 8, 3),
                                content=ft.Text(
                                    product["category"],
                                    size=11, weight="bold",
                                    color=COLOR_ORANGE_PRIMARY,
                                ),
                            ),
                            # Name
                            ft.Text(
                                product["name"],
                                size=15, weight="bold",
                                color=COLOR_GRAY_DARK,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            # Description
                            ft.Text(
                                product["description"],
                                size=12, color=COLOR_GRAY_TEXT,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            # Price + action buttons
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        product["price"],
                                        size=16, weight="bold",
                                        color=COLOR_GRAY_DARK,
                                    ),
                                    ft.Row(
                                        spacing=6,
                                        controls=[
                                            # Edit
                                            ft.Container(
                                                width=34, height=34,
                                                bgcolor=COLOR_BLUE_LIGHT,
                                                border_radius=8,
                                                alignment=ft.Alignment.CENTER,
                                                tooltip="Editar producto",
                                                on_click=lambda _, p=product: on_edit(p),
                                                content=ft.Icon(
                                                    ft.Icons.EDIT_OUTLINED,
                                                    size=16, color=COLOR_BLUE_INFO,
                                                ),
                                            ),
                                            # Delete
                                            ft.Container(
                                                width=34, height=34,
                                                bgcolor=COLOR_RED_LIGHT,
                                                border_radius=8,
                                                alignment=ft.Alignment.CENTER,
                                                tooltip="Eliminar producto",
                                                on_click=lambda _, p=product: on_delete(p),
                                                content=ft.Icon(
                                                    ft.Icons.DELETE_OUTLINE_ROUNDED,
                                                    size=16, color=COLOR_RED_ERROR,
                                                ),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )


# ─── Field builder ────────────────────────────────────────────────────────────
def _field(hint: str, value: str = "", multiline=False, min_lines=3, max_lines=4,
           ref=None):
    return ft.TextField(
        value=value,
        hint_text=hint,
        border=ft.InputBorder.OUTLINE,
        border_color=COLOR_GRAY_BORDER,
        focused_border_color=COLOR_ORANGE_PRIMARY,
        border_radius=10,
        text_size=13,
        content_padding=ft.Padding(14, 12, 14, 12),
        multiline=multiline,
        min_lines=min_lines if multiline else None,
        max_lines=max_lines if multiline else None,
        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
        ref=ref,
        expand=True,
    )


# ─── Modal shared structure ──────────────────────────────────────────────────
def _modal_shell(title: str, subtitle: str, body_controls,
                  actions, on_close, icon=None, icon_color=None):
    """Centered white card dialog with blurred backdrop."""
    return ft.Stack(
        expand=True,
        controls=[
            # Backdrop
            ft.Container(
                expand=True,
                bgcolor="#80000000",
                on_click=on_close,
            ),
            # Centered dialog
            ft.Container(
                alignment=ft.Alignment.CENTER,
                expand=True,
                content=ft.Container(
                    width=540,
                    bgcolor=COLOR_WHITE,
                    border_radius=20,
                    padding=ft.Padding(32, 28, 32, 28),
                    shadow=ft.BoxShadow(
                        blur_radius=40, spread_radius=0,
                        color="#50000000", offset=ft.Offset(0, 16),
                    ),
                    animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
                    scale=ft.Scale(1.0),
                    content=ft.Column(
                        spacing=20,
                        tight=True,
                        controls=[
                            # Title row
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            *(
                                                [ft.Icon(icon, color=icon_color, size=22)]
                                                if icon else []
                                            ),
                                            ft.Column(
                                                spacing=2, tight=True,
                                                controls=[
                                                    ft.Text(title, size=20, weight="bold",
                                                            color=COLOR_GRAY_DARK),
                                                    ft.Text(subtitle, size=12,
                                                            color=COLOR_GRAY_TEXT),
                                                ],
                                            ),
                                        ],
                                    ),
                                    ft.Container(
                                        width=28, height=28,
                                        bgcolor="#F3F4F6",
                                        border_radius=14,
                                        alignment=ft.Alignment.CENTER,
                                        on_click=on_close,
                                        content=ft.Icon(ft.Icons.CLOSE_ROUNDED,
                                                        size=16, color=COLOR_GRAY_DARK),
                                    ),
                                ],
                            ),
                            # Body
                            ft.Column(
                                spacing=14,
                                tight=True,
                                controls=body_controls,
                            ),
                            # Actions
                            ft.Row(
                                spacing=12,
                                controls=actions,
                            ),
                        ],
                    ),
                ),
            ),
        ],
    )


# ─── Main view ────────────────────────────────────────────────────────────────
def productos_view(page: ft.Page):
    products = list(SAMPLE_PRODUCTS)  # mutable local list (will hit DB later)

    # ── Refs para la grilla ────────────────────────────────────────────────────
    grid_ref    = ft.Ref[ft.Row]()
    modal_layer = ft.Ref[ft.Stack]()

    # ── Close modal ────────────────────────────────────────────────────────────
    def close_modal(e=None):
        if modal_layer.current and len(modal_layer.current.controls) > 1:
            modal_layer.current.controls = modal_layer.current.controls[:1]
            modal_layer.current.update()

    # ── Rebuild grid ───────────────────────────────────────────────────────────
    def refresh_grid(query: str = ""):
        q = query.strip().lower()
        filtered = [
            p for p in products
            if not q or q in p["name"].lower() or q in p["category"].lower()
        ]
        grid_ref.current.controls = [
            _product_card(p, open_edit_modal, open_delete_modal, toggle_avail)
            for p in filtered
        ]
        grid_ref.current.update()

    def on_search(e):
        refresh_grid(e.control.value)

    # ── Toggle availability ────────────────────────────────────────────────────
    def toggle_avail(product: dict):
        # Alterna el estado disponible / no disponible y solo refresca la grilla
        # (se evita usar `show_toast` aquí para no provocar errores de control
        # no adjunto en algunas versiones de Flet).
        product["available"] = not product["available"]
        refresh_grid()

    # ── CREATE modal ──────────────────────────────────────────────────────────
    def open_create_modal(e=None):
        f_name  = ft.Ref[ft.TextField]()
        f_desc  = ft.Ref[ft.TextField]()
        f_price = ft.Ref[ft.TextField]()
        f_cat   = ft.Ref[ft.TextField]()
        f_img   = ft.Ref[ft.TextField]()

        def open_img_picker(ev):
            # Mensaje informativo: escribe la ruta manualmente
            show_toast(
                page,
                "Escribe la ruta de la imagen en el campo de texto.\nEj: img/comida1.jpg",
                "Agregar imagen",
                type="info",
            )

        def do_create(e=None):
            name  = f_name.current.value.strip()
            price = f_price.current.value.strip()
            if not name or not price:
                return
            new_id = max((p["id"] for p in products), default=0) + 1
            products.append({
                "id": new_id,
                "name": name,
                "description": f_desc.current.value.strip() or "Sin descripción",
                "price": f"$ {price}",
                "category": f_cat.current.value.strip() or "specialty",
                "image": f_img.current.value.strip() or "img/comida1.jpg",
                "available": True,
            })
            close_modal()
            refresh_grid()

        modal = _modal_shell(
            title="Nuevo Producto",
            subtitle="Completa los datos para crear un nuevo producto",
            on_close=close_modal,
            body_controls=[
                ft.Column([
                    ft.Text("Nombre del producto *", size=12, weight="bold",
                            color=COLOR_GRAY_DARK),
                    _field("Ej: Almuerzo Completo", ref=f_name),
                ], spacing=6, tight=True),
                ft.Column([
                    ft.Text("Descripción", size=12, weight="bold",
                            color=COLOR_GRAY_DARK),
                    _field("Describe el producto...", multiline=True, ref=f_desc),
                ], spacing=6, tight=True),
                ft.Row([
                    ft.Column([
                        ft.Text("Precio (COP) *", size=12, weight="bold",
                                color=COLOR_GRAY_DARK),
                        _field("12000", ref=f_price),
                    ], spacing=6, tight=True, expand=True),
                    ft.Column([
                        ft.Text("Categoría *", size=12, weight="bold",
                                color=COLOR_GRAY_DARK),
                        _field("specialty", ref=f_cat),
                    ], spacing=6, tight=True, expand=True),
                ], spacing=12),
                ft.Column(
                    [
                        ft.Text(
                            "Imagen del producto",
                            size=12,
                            weight="bold",
                            color=COLOR_GRAY_DARK,
                        ),
                        _field("img/comida1.jpg", ref=f_img, value=""),
                        ft.Container(
                            on_click=open_img_picker,
                            content=ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.IMAGE_OUTLINED,
                                        size=16,
                                        color=COLOR_ORANGE_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Subir imagen desde tu dispositivo",
                                        size=12,
                                        color=COLOR_ORANGE_PRIMARY,
                                        weight="bold",
                                    ),
                                ],
                                spacing=6,
                            ),
                        ),
                    ],
                    spacing=6,
                    tight=True,
                ),
            ],
            actions=[
                ft.Container(
                    expand=True,
                    content=ft.Button(
                        "Cancelar",
                        on_click=close_modal,
                        style=ft.ButtonStyle(
                            color=COLOR_GRAY_DARK,
                            bgcolor={"": "#F3F4F6"},
                            padding=ft.Padding(0, 14, 0, 14),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=0,
                        ),
                    ),
                ),
                ft.Container(
                    expand=True,
                    content=ft.Button(
                        "Crear Producto",
                        on_click=do_create,
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor={"": COLOR_ORANGE_PRIMARY,
                                     "hovered": COLOR_ORANGE_DARK},
                            padding=ft.Padding(0, 14, 0, 14),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=0,
                        ),
                    ),
                ),
            ],
        )
        modal_layer.current.controls = modal_layer.current.controls[:1] + [modal]
        modal_layer.current.update()

    # ── EDIT modal ────────────────────────────────────────────────────────────
    def open_edit_modal(product: dict):
        f_name  = ft.Ref[ft.TextField]()
        f_desc  = ft.Ref[ft.TextField]()
        f_price = ft.Ref[ft.TextField]()
        f_cat   = ft.Ref[ft.TextField]()
        f_img   = ft.Ref[ft.TextField]()
        preview = ft.Ref[ft.Image]()
        prev_container = ft.Ref[ft.Container]()

        raw_price = product["price"].replace("$ ", "").replace(".", "")

        def on_url_change(e):
            url = e.control.value.strip()
            if url and prev_container.current:
                prev_container.current.visible = True
                preview.current.src = url
                prev_container.current.update()

        def open_img_picker_edit(ev):
            # Mensaje informativo: escribe o pega la URL manualmente
            show_toast(
                page,
                "Pega la URL de la imagen o escribe la ruta local en el campo de texto.",
                "Cambiar imagen",
                type="info",
            )

        def do_update(e=None):
            product["name"]        = f_name.current.value.strip()  or product["name"]
            product["description"] = f_desc.current.value.strip()  or product["description"]
            product["price"]       = f"$ {f_price.current.value.strip()}" or product["price"]
            product["category"]    = f_cat.current.value.strip()   or product["category"]
            new_img = f_img.current.value.strip()
            if new_img:
                product["image"] = new_img
            close_modal()
            refresh_grid()

        preview_img_url = product["image"]

        modal = _modal_shell(
            title="Editar Producto",
            subtitle="Actualiza la información del producto",
            on_close=close_modal,
            body_controls=[
                ft.Column([
                    ft.Text("Nombre del producto *", size=12, weight="bold",
                            color=COLOR_GRAY_DARK),
                    _field("Nombre", value=product["name"], ref=f_name),
                ], spacing=6, tight=True),
                ft.Column([
                    ft.Text("Descripción", size=12, weight="bold",
                            color=COLOR_GRAY_DARK),
                    _field("Describe el producto...", multiline=True,
                           value=product["description"], ref=f_desc),
                ], spacing=6, tight=True),
                ft.Row([
                    ft.Column([
                        ft.Text("Precio (COP) *", size=12, weight="bold",
                                color=COLOR_GRAY_DARK),
                        _field("Precio", value=raw_price, ref=f_price),
                    ], spacing=6, tight=True, expand=True),
                    ft.Column([
                        ft.Text("Categoría *", size=12, weight="bold",
                                color=COLOR_GRAY_DARK),
                        _field("specialty", value=product["category"], ref=f_cat),
                    ], spacing=6, tight=True, expand=True),
                ], spacing=12),
                ft.Column([
                    ft.Text("URL de Imagen", size=12, weight="bold",
                            color=COLOR_GRAY_DARK),
                    ft.TextField(
                        value=preview_img_url,
                        hint_text="https://...",
                        border=ft.InputBorder.OUTLINE,
                        border_color=COLOR_GRAY_BORDER,
                        focused_border_color=COLOR_ORANGE_PRIMARY,
                        border_radius=10,
                        text_size=13,
                        content_padding=ft.Padding(14, 12, 14, 12),
                        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
                        on_change=on_url_change,
                        ref=f_img,
                        expand=True,
                    ),
                    ft.Container(
                        on_click=open_img_picker_edit,
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.IMAGE_OUTLINED,
                                    size=16,
                                    color=COLOR_ORANGE_PRIMARY,
                                ),
                                ft.Text(
                                    "Subir imagen desde tu dispositivo",
                                    size=12,
                                    color=COLOR_ORANGE_PRIMARY,
                                    weight="bold",
                                ),
                            ],
                            spacing=6,
                        ),
                    ),
                    # Image preview
                    ft.Container(
                        ref=prev_container,
                        visible=True,
                        border_radius=12,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        height=140,
                        content=ft.Image(
                            ref=preview,
                            src=preview_img_url,
                            fit=ft.BoxFit.COVER,
                            width=476,
                        ),
                    ),
                ], spacing=6, tight=True),
            ],
            actions=[
                ft.Container(
                    expand=True,
                    content=ft.Button(
                        "Cancelar",
                        on_click=close_modal,
                        style=ft.ButtonStyle(
                            color=COLOR_GRAY_DARK,
                            bgcolor={"": "#F3F4F6"},
                            padding=ft.Padding(0, 14, 0, 14),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=0,
                        ),
                    ),
                ),
                ft.Container(
                    expand=True,
                    content=ft.Button(
                        "Actualizar",
                        on_click=do_update,
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor={"": COLOR_ORANGE_PRIMARY,
                                     "hovered": COLOR_ORANGE_DARK},
                            padding=ft.Padding(0, 14, 0, 14),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=0,
                        ),
                    ),
                ),
            ],
        )
        modal_layer.current.controls = modal_layer.current.controls[:1] + [modal]
        modal_layer.current.update()

    # ── DELETE modal ──────────────────────────────────────────────────────────
    def open_delete_modal(product: dict):
        def do_delete(e=None):
            products.remove(product)
            close_modal()
            refresh_grid()

        modal = _modal_shell(
            title="Eliminar Producto",
            subtitle="¿Estás seguro de eliminar este producto? Esta acción no se puede deshacer.",
            icon=ft.Icons.WARNING_AMBER_ROUNDED,
            icon_color=COLOR_RED_ERROR,
            on_close=close_modal,
            body_controls=[
                # Product preview card inside delete modal
                ft.Container(
                    bgcolor=COLOR_BG_LIGHT,
                    border_radius=14,
                    padding=ft.Padding(16, 14, 16, 14),
                    content=ft.Row(
                        spacing=14,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=70, height=60,
                                border_radius=10,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                content=ft.Image(
                                    src=product["image"],
                                    width=70, height=60,
                                    fit=ft.BoxFit.COVER,
                                ),
                            ),
                            ft.Column(
                                spacing=4, tight=True, expand=True,
                                controls=[
                                    ft.Container(
                                        bgcolor=COLOR_ORANGE_LIGHT,
                                        border_radius=6,
                                        padding=ft.Padding(8, 2, 8, 2),
                                        content=ft.Text(
                                            "Especialidades", size=10,
                                            weight="bold",
                                            color=COLOR_ORANGE_PRIMARY,
                                        ),
                                    ),
                                    ft.Text(product["name"], size=14,
                                            weight="bold", color=COLOR_GRAY_DARK),
                                    ft.Text(product["description"], size=11,
                                            color=COLOR_GRAY_TEXT,
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(product["price"], size=14,
                                            weight="bold", color=COLOR_GRAY_DARK),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
            actions=[
                ft.Container(
                    expand=True,
                    content=ft.Button(
                        "Cancelar",
                        on_click=close_modal,
                        style=ft.ButtonStyle(
                            color=COLOR_GRAY_DARK,
                            bgcolor={"": "#F3F4F6"},
                            padding=ft.Padding(0, 14, 0, 14),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=0,
                        ),
                    ),
                ),
                ft.Container(
                    expand=True,
                    content=ft.Button(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED,
                                        color="white", size=16),
                                ft.Text("Eliminar", color="white",
                                        size=14, weight="bold"),
                            ],
                        ),
                        on_click=do_delete,
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor={"": COLOR_RED_ERROR, "hovered": "#B91C1C"},
                            padding=ft.Padding(0, 14, 0, 14),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=0,
                        ),
                    ),
                ),
            ],
        )
        modal_layer.current.controls = modal_layer.current.controls[:1] + [modal]
        modal_layer.current.update()

    # ── Product grid ──────────────────────────────────────────────────────────
    products_grid = ft.Row(
        ref=grid_ref,
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[
            _product_card(p, open_edit_modal, open_delete_modal, toggle_avail)
            for p in products
        ],
    )

    # ── Page skeleton ─────────────────────────────────────────────────────────
    page_content = ft.Container(
        expand=True,
        bgcolor=COLOR_BG_PAGE,
        padding=ft.Padding(32, 28, 32, 28),
        content=ft.Column(
            expand=True,
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                # Header
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text("Gestión de Productos", size=26,
                                        weight="bold", color=COLOR_GRAY_DARK),
                                ft.Text("Administra el menú y disponibilidad de productos",
                                        size=14, color=COLOR_GRAY_TEXT),
                            ],
                        ),
                        ft.Container(
                            on_click=open_create_modal,
                            bgcolor=COLOR_ORANGE_PRIMARY,
                            border_radius=12,
                            padding=ft.Padding(20, 12, 20, 12),
                            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                            content=ft.Row(
                                spacing=8,
                                tight=True,
                                controls=[
                                    ft.Icon(ft.Icons.ADD_ROUNDED,
                                            color="white", size=18),
                                    ft.Text("Nuevo Producto", size=14,
                                            weight="bold", color="white"),
                                ],
                            ),
                        ),
                    ],
                ),

                # Search bar
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    border_radius=12,
                    border=ft.Border.all(1, COLOR_GRAY_BORDER),
                    padding=ft.Padding(16, 0, 16, 0),
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SEARCH_ROUNDED,
                                    color=COLOR_GRAY_TEXT, size=20),
                            ft.TextField(
                                hint_text="Buscar productos por nombre o categoría...",
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

                # Product cards grid
                products_grid,
            ],
        ),
    )

    # ── Stack: page + modal layer ─────────────────────────────────────────────
    return ft.Stack(
        ref=modal_layer,
        expand=True,
        controls=[page_content],
    )