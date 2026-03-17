import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog
import flet as ft
from controllers.menu import MenuController
from views.styles import (
    COLOR_ORANGE_PRIMARY,
    COLOR_ORANGE_LIGHT,
    COLOR_ORANGE_DARK,
    COLOR_GREEN_SUCCESS,
    COLOR_RED_ERROR,
    COLOR_RED_LIGHT,
    COLOR_BLUE_INFO,
    COLOR_BLUE_LIGHT,
    COLOR_GRAY_DARK,
    COLOR_GRAY_TEXT,
    COLOR_GRAY_BORDER,
    COLOR_BG_PAGE,
    COLOR_BG_LIGHT,
    COLOR_WHITE,
    show_toast,
)

controller = MenuController()
ASSETS_IMG_DIR = "assets/img"


def open_file_dialog(callback):
    def _run():
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.webp *.gif"),
                ("Todos los archivos", "*.*"),
            ],
        )
        root.destroy()
        if path:
            filename = os.path.basename(path)
            dest = os.path.join(ASSETS_IMG_DIR, filename)
            shutil.copy2(path, dest)
            callback(f"img/{filename}")
    threading.Thread(target=_run, daemon=True).start()


def _avail_badge(available: bool, on_click=None):
    return ft.Container(
        bgcolor=COLOR_GREEN_SUCCESS if available else COLOR_RED_ERROR,
        border_radius=20,
        padding=ft.Padding(10, 4, 10, 4),
        on_click=on_click,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        content=ft.Text(
            "Disponible" if available else "No disponible",
            size=11, weight="bold", color="white",
        ),
    )


def _product_card(product: dict, on_edit, on_delete, on_toggle):
    avail    = product["available"]
    card_ref = ft.Ref[ft.Container]()

    def on_hover(e):
        card_ref.current.scale  = 1.03 if e.data == "true" else 1.0
        card_ref.current.shadow = (
            ft.BoxShadow(blur_radius=28, spread_radius=2,
                         color="#35000000", offset=ft.Offset(0, 10))
            if e.data == "true" else
            ft.BoxShadow(blur_radius=8, spread_radius=0,
                         color="#18000000", offset=ft.Offset(0, 2))
        )
        card_ref.current.update()

    return ft.Container(
        ref=card_ref,
        width=300,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        border=ft.Border.all(1, "#F3EFEA"),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        scale=1.0,
        shadow=ft.BoxShadow(blur_radius=8, spread_radius=0,
                             color="#18000000", offset=ft.Offset(0, 2)),
        animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
        on_hover=on_hover,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Stack(
                    height=180,
                    controls=[
                        ft.Container(
                            expand=True,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=product["image"],
                                width=300, height=180,
                                fit=ft.BoxFit.COVER,
                            ),
                        ),
                        ft.Container(
                            top=10, right=10,
                            content=_avail_badge(
                                avail,
                                on_click=lambda e, p=product: on_toggle(p),
                            ),
                        ),
                    ],
                ),
                ft.Container(
                    padding=ft.Padding(14, 12, 14, 14),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Container(
                                bgcolor=COLOR_ORANGE_LIGHT, border_radius=6,
                                padding=ft.Padding(8, 3, 8, 3),
                                content=ft.Row(spacing=4, tight=True, controls=[
                                    ft.Icon(ft.Icons.INVENTORY_2_OUTLINED,
                                            size=12, color=COLOR_ORANGE_PRIMARY),
                                    ft.Text(f"Stock: {product.get('stock', 0)}",
                                            size=11, weight="bold",
                                            color=COLOR_ORANGE_PRIMARY),
                                ]),
                            ),
                            ft.Text(product["name"], size=14, weight="bold",
                                    color=COLOR_GRAY_DARK, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Text(product["description"], size=12,
                                    color=COLOR_GRAY_TEXT, max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(product["price"], size=15,
                                            weight="bold", color=COLOR_GRAY_DARK),
                                    ft.Row(spacing=6, controls=[
                                        ft.Container(
                                            width=32, height=32,
                                            bgcolor=COLOR_BLUE_LIGHT,
                                            border_radius=8,
                                            alignment=ft.Alignment(0, 0),
                                            tooltip="Editar producto",
                                            on_click=lambda _, p=product: on_edit(p),
                                            content=ft.Icon(ft.Icons.EDIT_OUTLINED,
                                                            size=15, color=COLOR_BLUE_INFO),
                                        ),
                                        ft.Container(
                                            width=32, height=32,
                                            bgcolor=COLOR_RED_LIGHT,
                                            border_radius=8,
                                            alignment=ft.Alignment(0, 0),
                                            tooltip="Eliminar producto",
                                            on_click=lambda _, p=product: on_delete(p),
                                            content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED,
                                                            size=15, color=COLOR_RED_ERROR),
                                        ),
                                    ]),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )


def _field(hint: str, value: str = "", multiline=False, min_lines=3, max_lines=4,
           ref=None, input_filter=None):
    return ft.TextField(
        value=value, hint_text=hint,
        border=ft.InputBorder.OUTLINE, border_color=COLOR_GRAY_BORDER,
        focused_border_color=COLOR_ORANGE_PRIMARY, border_radius=10, text_size=13,
        content_padding=ft.Padding(14, 12, 14, 12),
        multiline=multiline,
        min_lines=min_lines if multiline else None,
        max_lines=max_lines if multiline else None,
        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
        ref=ref, expand=True, input_filter=input_filter,
    )


def _modal_shell(title, subtitle, body_controls, actions, on_close,
                 icon=None, icon_color=None, height=None):
    return ft.Stack(
        expand=True,
        controls=[
            ft.Container(expand=True, bgcolor="#80000000", on_click=on_close),
            ft.Container(
                alignment=ft.Alignment(0, 0), expand=True,
                content=ft.Container(
                    width=520,
                    # height=None → el modal se ajusta al contenido automáticamente
                    height=height,
                    bgcolor=COLOR_WHITE,
                    border_radius=20,
                    padding=ft.Padding(28, 24, 28, 24),
                    shadow=ft.BoxShadow(blur_radius=40, spread_radius=0,
                                        color="#50000000", offset=ft.Offset(0, 16)),
                    content=ft.Column(
                        spacing=18, tight=True,
                        scroll=ft.ScrollMode.ADAPTIVE,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    ft.Row(spacing=10, controls=[
                                        *([ft.Icon(icon, color=icon_color, size=22)] if icon else []),
                                        ft.Column(spacing=2, tight=True, controls=[
                                            ft.Text(title, size=20, weight="bold",
                                                    color=COLOR_GRAY_DARK),
                                            ft.Text(subtitle, size=12,
                                                    color=COLOR_GRAY_TEXT),
                                        ]),
                                    ]),
                                    ft.Container(
                                        width=28, height=28, bgcolor="#F3F4F6",
                                        border_radius=14,
                                        alignment=ft.Alignment(0, 0),
                                        on_click=on_close,
                                        content=ft.Icon(ft.Icons.CLOSE_ROUNDED,
                                                        size=16, color=COLOR_GRAY_DARK),
                                    ),
                                ],
                            ),
                            ft.Column(spacing=14, tight=True, controls=body_controls),
                            ft.Row(spacing=12, controls=actions),
                        ],
                    ),
                ),
            ),
        ],
    )


# ─── Main view ────────────────────────────────────────────────────────────────
def productos_view(page: ft.Page):
    products    = controller.get_products()
    grid_ref    = ft.Ref[ft.Row]()
    modal_layer = ft.Ref[ft.Stack]()

    def close_modal(e=None):
        if modal_layer.current and len(modal_layer.current.controls) > 1:
            modal_layer.current.controls = modal_layer.current.controls[:1]
            modal_layer.current.update()

    def refresh_grid(query: str = ""):
        q = query.strip().lower()
        filtered = [p for p in products if not q or q in p["name"].lower()]
        grid_ref.current.controls = (
            [_product_card(p, open_edit_modal, open_delete_modal, toggle_avail)
             for p in filtered]
            if filtered else [_empty_state()]
        )
        grid_ref.current.update()

    def on_search(e):
        refresh_grid(e.control.value)

    # ── Toggle disponibilidad con toast ───────────────────────────────
    def toggle_avail(product: dict):
        new_val = not product["available"]
        ok = controller.toggle_disponible(product["id"], new_val)
        if ok:
            product["available"] = new_val
            refresh_grid()
            if new_val:
                show_toast(
                    page,
                    f'"{product["name"]}" ahora está disponible',
                    title="Disponibilidad",
                    type="success",
                )
            else:
                show_toast(
                    page,
                    f'"{product["name"]}" marcado como no disponible',
                    title="Disponibilidad",
                    type="error",
                )
        else:
            show_toast(page, "Error al cambiar disponibilidad", type="error")

    # ── CREATE modal ──────────────────────────────────────────────────
    def open_create_modal(e=None):
        f_name  = ft.Ref[ft.TextField]()
        f_desc  = ft.Ref[ft.TextField]()
        f_price = ft.Ref[ft.TextField]()
        f_stock = ft.Ref[ft.TextField]()
        f_img   = ft.Ref[ft.TextField]()

        def on_image_picked(path: str):
            f_img.current.value = path
            f_img.current.update()

        def do_create(e=None):
            name  = f_name.current.value.strip()
            price = f_price.current.value.strip()
            stock = f_stock.current.value.strip() or "0"
            desc  = f_desc.current.value.strip() or "Sin descripción"
            img   = f_img.current.value.strip() or None
            if not name or not price:
                show_toast(page, "Nombre y precio son obligatorios", type="error")
                return
            ok = controller.create_product(name, desc, price, stock, img)
            if ok:
                products.clear()
                products.extend(controller.get_products())
                close_modal()
                refresh_grid()
                show_toast(page, "Producto creado exitosamente", type="success")
            else:
                show_toast(page, "Error al crear el producto", type="error")

        modal = _modal_shell(
            title="Nuevo Producto",
            subtitle="Completa los datos para crear un nuevo producto",
            on_close=close_modal,
            height=580,
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
                        _field("12000", ref=f_price,
                               input_filter=ft.NumbersOnlyInputFilter()),
                    ], spacing=6, tight=True, expand=True),
                    ft.Column([
                        ft.Text("Stock *", size=12, weight="bold",
                                color=COLOR_GRAY_DARK),
                        _field("0", ref=f_stock,
                               input_filter=ft.NumbersOnlyInputFilter()),
                    ], spacing=6, tight=True, expand=True),
                ], spacing=12),
                ft.Column([
                    ft.Text("Imagen del producto", size=12, weight="bold",
                            color=COLOR_GRAY_DARK),
                    _field("Selecciona una imagen...", ref=f_img, value=""),
                    ft.Container(
                        on_click=lambda ev: open_file_dialog(on_image_picked),
                        content=ft.Row(spacing=6, controls=[
                            ft.Icon(ft.Icons.IMAGE_OUTLINED, size=16,
                                    color=COLOR_ORANGE_PRIMARY),
                            ft.Text("Subir imagen desde tu dispositivo",
                                    size=12, color=COLOR_ORANGE_PRIMARY,
                                    weight="bold"),
                        ]),
                    ),
                ], spacing=6, tight=True),
            ],
            actions=[
                ft.Container(expand=True, content=ft.Button(
                    "Cancelar", on_click=close_modal,
                    style=ft.ButtonStyle(
                        color=COLOR_GRAY_DARK, bgcolor={"": "#F3F4F6"},
                        padding=ft.Padding(0, 14, 0, 14),
                        shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                )),
                ft.Container(expand=True, content=ft.Button(
                    "Crear Producto", on_click=do_create,
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor={"": COLOR_ORANGE_PRIMARY, "hovered": COLOR_ORANGE_DARK},
                        padding=ft.Padding(0, 14, 0, 14),
                        shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                )),
            ],
        )
        modal_layer.current.controls = modal_layer.current.controls[:1] + [modal]
        modal_layer.current.update()

    # ── EDIT modal ────────────────────────────────────────────────────
    def open_edit_modal(product: dict):
        f_name  = ft.Ref[ft.TextField]()
        f_desc  = ft.Ref[ft.TextField]()
        f_price = ft.Ref[ft.TextField]()
        f_stock = ft.Ref[ft.TextField]()
        f_img   = ft.Ref[ft.TextField]()
        preview       = ft.Ref[ft.Image]()
        prev_container = ft.Ref[ft.Container]()

        raw_price = str(int(product["price_raw"]))
        raw_stock = str(product.get("stock", 0))

        def on_url_change(e):
            url = e.control.value.strip()
            if url and prev_container.current:
                prev_container.current.visible = True
                preview.current.src = url
                prev_container.current.update()

        def on_image_picked_edit(path: str):
            f_img.current.value = path
            f_img.current.update()
            if prev_container.current:
                prev_container.current.visible = True
                preview.current.src = path
                prev_container.current.update()

        def do_update(e=None):
            name  = f_name.current.value.strip() or product["name"]
            desc  = f_desc.current.value.strip() or product["description"]
            price = f_price.current.value.strip() or raw_price
            stock = f_stock.current.value.strip() or raw_stock
            img   = f_img.current.value.strip() or None
            ok = controller.update_product(product["id"], name, desc, price, stock, img)
            if ok:
                product["name"]        = name
                product["description"] = desc
                product["price"]       = f"$ {int(float(price)):,}".replace(",", ".")
                product["price_raw"]   = float(price)
                product["stock"]       = int(stock)
                if img:
                    product["image"] = img
                close_modal()
                refresh_grid()
                show_toast(page, "Producto actualizado", type="success")
            else:
                show_toast(page, "Error al actualizar el producto", type="error")

        modal = _modal_shell(
            title="Editar Producto",
            subtitle="Actualiza la información del producto",
            on_close=close_modal,
            height=580,
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
                        _field("Precio", value=raw_price, ref=f_price,
                               input_filter=ft.NumbersOnlyInputFilter()),
                    ], spacing=6, tight=True, expand=True),
                    ft.Column([
                        ft.Text("Stock *", size=12, weight="bold",
                                color=COLOR_GRAY_DARK),
                        _field("0", value=raw_stock, ref=f_stock,
                               input_filter=ft.NumbersOnlyInputFilter()),
                    ], spacing=6, tight=True, expand=True),
                ], spacing=12),
                ft.Column([
                    ft.Text("Imagen del producto", size=12, weight="bold",
                            color=COLOR_GRAY_DARK),
                    ft.TextField(
                        value=product["image"],
                        hint_text="Ruta de la imagen",
                        border=ft.InputBorder.OUTLINE,
                        border_color=COLOR_GRAY_BORDER,
                        focused_border_color=COLOR_ORANGE_PRIMARY,
                        border_radius=10, text_size=13,
                        content_padding=ft.Padding(14, 12, 14, 12),
                        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
                        on_change=on_url_change, ref=f_img,
                    ),
                    ft.Container(
                        on_click=lambda ev: open_file_dialog(on_image_picked_edit),
                        content=ft.Row(spacing=6, controls=[
                            ft.Icon(ft.Icons.IMAGE_OUTLINED, size=16,
                                    color=COLOR_ORANGE_PRIMARY),
                            ft.Text("Subir imagen desde tu dispositivo",
                                    size=12, color=COLOR_ORANGE_PRIMARY,
                                    weight="bold"),
                        ]),
                    ),
                ], spacing=6, tight=True),
            ],
            actions=[
                ft.Container(expand=True, content=ft.Button(
                    "Cancelar", on_click=close_modal,
                    style=ft.ButtonStyle(
                        color=COLOR_GRAY_DARK, bgcolor={"": "#F3F4F6"},
                        padding=ft.Padding(0, 14, 0, 14),
                        shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                )),
                ft.Container(expand=True, content=ft.Button(
                    "Actualizar", on_click=do_update,
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor={"": COLOR_ORANGE_PRIMARY, "hovered": COLOR_ORANGE_DARK},
                        padding=ft.Padding(0, 14, 0, 14),
                        shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                )),
            ],
        )
        modal_layer.current.controls = modal_layer.current.controls[:1] + [modal]
        modal_layer.current.update()

    # ── DELETE modal ──────────────────────────────────────────────────
    def open_delete_modal(product: dict):
        def do_delete(e=None):
            ok = controller.delete_product(product["id"])
            if ok:
                products.remove(product)
                close_modal()
                refresh_grid()
                show_toast(page, "Producto eliminado", type="success")
            else:
                show_toast(page, "Error al eliminar el producto", type="error")

        modal = _modal_shell(
            title="Eliminar Producto",
            subtitle="¿Estás seguro? Esta acción no se puede deshacer.",
            icon=ft.Icons.WARNING_AMBER_ROUNDED, icon_color=COLOR_RED_ERROR,
            on_close=close_modal,
            body_controls=[
                ft.Container(
                    bgcolor=COLOR_BG_LIGHT, border_radius=14,
                    padding=ft.Padding(16, 14, 16, 14),
                    content=ft.Row(
                        spacing=14,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=70, height=60, border_radius=10,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                content=ft.Image(src=product["image"], width=70,
                                                 height=60, fit=ft.BoxFit.COVER),
                            ),
                            ft.Column(spacing=4, tight=True, expand=True, controls=[
                                ft.Container(
                                    bgcolor=COLOR_ORANGE_LIGHT, border_radius=6,
                                    padding=ft.Padding(8, 2, 8, 2),
                                    content=ft.Text(f"Stock: {product.get('stock', 0)}",
                                                    size=10, weight="bold",
                                                    color=COLOR_ORANGE_PRIMARY),
                                ),
                                ft.Text(product["name"], size=14, weight="bold",
                                        color=COLOR_GRAY_DARK),
                                ft.Text(product["description"], size=11,
                                        color=COLOR_GRAY_TEXT, max_lines=2,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(product["price"], size=14, weight="bold",
                                        color=COLOR_GRAY_DARK),
                            ]),
                        ],
                    ),
                ),
            ],
            actions=[
                ft.Container(expand=True, content=ft.Button(
                    "Cancelar", on_click=close_modal,
                    style=ft.ButtonStyle(
                        color=COLOR_GRAY_DARK, bgcolor={"": "#F3F4F6"},
                        padding=ft.Padding(0, 14, 0, 14),
                        shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                )),
                ft.Container(expand=True, content=ft.Button(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER, spacing=6,
                        controls=[
                            ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    color="white", size=16),
                            ft.Text("Eliminar", color="white", size=14,
                                    weight="bold"),
                        ],
                    ),
                    on_click=do_delete,
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor={"": COLOR_RED_ERROR, "hovered": "#B91C1C"},
                        padding=ft.Padding(0, 14, 0, 14),
                        shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                )),
            ],
        )
        modal_layer.current.controls = modal_layer.current.controls[:1] + [modal]
        modal_layer.current.update()

    # ── Empty state ───────────────────────────────────────────────────
    def _empty_state():
        return ft.Container(
            padding=ft.Padding(0, 60, 0, 0),
            alignment=ft.Alignment(0, -1),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Container(
                        width=80, height=80,
                        bgcolor=COLOR_ORANGE_LIGHT,
                        border_radius=40,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(ft.Icons.RESTAURANT_MENU_ROUNDED,
                                        size=38, color=COLOR_ORANGE_PRIMARY),
                    ),
                    ft.Text("Sin productos todavía", size=18,
                            weight="bold", color=COLOR_GRAY_DARK),
                    ft.Text("Agrega tu primer producto con el botón\n\"Nuevo Producto\"",
                            size=13, color=COLOR_GRAY_TEXT,
                            text_align=ft.TextAlign.CENTER),
                ],
            ),
        )

    # ── Grid de productos ─────────────────────────────────────────────
    products_grid = ft.Row(
        ref=grid_ref,
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=(
            [_product_card(p, open_edit_modal, open_delete_modal, toggle_avail)
             for p in products]
            if products else [_empty_state()]
        ),
    )

    # ── Layout principal — contenido siempre en el tope ─────────────
    inner_col = ft.Column(
        spacing=20,
        controls=[
            # Cabecera
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(spacing=3, tight=True, controls=[
                        ft.Text("Gestión de Productos", size=24,
                                weight="bold", color=COLOR_GRAY_DARK),
                        ft.Text("Administra el menú y disponibilidad de productos",
                                size=13, color=COLOR_GRAY_TEXT),
                    ]),
                    ft.Container(
                        on_click=open_create_modal,
                        bgcolor=COLOR_ORANGE_PRIMARY,
                        border_radius=12,
                        padding=ft.Padding(18, 11, 18, 11),
                        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                        content=ft.Row(spacing=7, tight=True, controls=[
                            ft.Icon(ft.Icons.ADD_ROUNDED, color="white", size=17),
                            ft.Text("Nuevo Producto", size=13,
                                    weight="bold", color="white"),
                        ]),
                    ),
                ],
            ),
            # Buscador
            ft.Container(
                bgcolor=COLOR_WHITE,
                border_radius=12,
                border=ft.Border.all(1, COLOR_GRAY_BORDER),
                padding=ft.Padding(14, 0, 14, 0),
                content=ft.Row(spacing=10, controls=[
                    ft.Icon(ft.Icons.SEARCH_ROUNDED, color=COLOR_GRAY_TEXT, size=18),
                    ft.TextField(
                        hint_text="Buscar productos por nombre...",
                        border=ft.InputBorder.NONE,
                        expand=True, height=44,
                        text_size=13,
                        hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT),
                        on_change=on_search,
                    ),
                ]),
            ),
            # Grid
            products_grid,
        ],
    )

    # Stack expand + Container top=0 garantiza que el contenido
    # SIEMPRE empiece desde arriba sin importar cuánto contenido haya
    page_content = ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=COLOR_BG_PAGE,
            ),
            ft.Container(
                top=0,
                left=0,
                right=0,
                bottom=0,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=0,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(28, 24, 28, 24),
                            content=inner_col,
                        ),
                    ],
                ),
            ),
        ],
    )

    return ft.Stack(ref=modal_layer, expand=True, controls=[page_content])