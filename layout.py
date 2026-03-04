import flet as ft
from views.perfil import perfil_view
from views.reportes import reportes_view
from views.token import token_view
from views.pedidos import pedidos_view
from views.dashboard import dashboard_view
from views.productos import productos_view
from views.styles import (
    show_toast, COLOR_BG_SIDEBAR, COLOR_ORANGE_PRIMARY,
    COLOR_GRAY_DARK, COLOR_GRAY_LIGHT, COLOR_BG_PAGE,
)

def app_layout(page: ft.Page, logout):
    

    # Los borradores locales han sido removidos para usar las vistas externas
    
    def handle_logout(e=None):
        page.overlay.clear()
        page.update()
        logout()

    def change_view(i):
        nonlocal selected_index
        selected_index = i
        content.content = views[i]()
        for idx, ctrl in enumerate(sidebar_controls):
            sel = idx == selected_index
            fg = "white" if sel else "#1F2937"
            ctrl.bgcolor = "#F97316" if sel else "transparent"
            ctrl.shadow = [ft.BoxShadow(color="#F9731660", blur_radius=6, offset=ft.Offset(0,2))] if sel else None
            ctrl.border_radius = 12
            row = ctrl.content
            row.controls[0].color = fg
            row.controls[1].color = fg
        logout_ctrl.opacity = 0 if selected_index == 5 else 1
        logout_ctrl.disabled = selected_index == 5
        page.update()

    # sidebar and logo references for resizing
    # Logo ligeramente más grande para mayor presencia visual
    logo_img = ft.Image(src="img/logo.png", width=140, height=140, fit="contain")
    sidebar_container = ft.Container(
        width=240,
        bgcolor=COLOR_BG_SIDEBAR,
        padding=15,
        content=None,
    )

    content = ft.Container(
        expand=True,
        content=dashboard_view(page),
    )

    # application state and view registry
    selected_index = 0
    views = {
        0: lambda: dashboard_view(page),
        1: lambda: productos_view(page),
        2: lambda: pedidos_view(page),
        3: lambda: token_view(page),
        4: lambda: reportes_view(page),
        5: lambda: perfil_view(page, change_view, handle_logout),
    }

    sidebar_items = [
        ("Dashboard", ft.Icons.DASHBOARD),
        ("Productos", ft.Icons.RESTAURANT),
        ("Pedidos", ft.Icons.SHOPPING_BAG),
        ("Token", ft.Icons.QR_CODE),
        ("Reportes", ft.Icons.BAR_CHART),
        ("Perfil", ft.Icons.PERSON),
    ]

    sidebar_controls: list[ft.Control] = []
    sidebar_spacer = ft.Container(expand=True)
    logout_ctrl = ft.Container(
        padding=ft.Padding.symmetric(vertical=8, horizontal=12),
        margin=ft.Margin.only(top=20),
        on_click=handle_logout,
        content=ft.Row(
            spacing=10,
            controls=[
                ft.Icon(ft.Icons.EXIT_TO_APP, color="#1F2937", size=18),
                ft.Text("Cerrar sesión", color="#1F2937", size=14),
            ],
        ),
    )
    logout_ctrl.opacity = 0 if selected_index == 5 else 1
    logout_ctrl.disabled = selected_index == 5

    def make_item(idx, label, icon):
        sel = idx == selected_index
        fg = "white" if sel else "#1F2937"
        bg = "#F97316" if sel else "transparent"
        shadow = [ft.BoxShadow(color="#F9731660", blur_radius=6, offset=ft.Offset(0,2))] if sel else None
        ctrl = ft.Container(
            padding=ft.Padding.symmetric(vertical=10, horizontal=16),
            bgcolor=bg,
            border_radius=12,
            shadow=shadow,
            on_click=lambda e, i=idx: change_view(i),
            content=ft.Row(
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Icon(icon, color=fg, size=18),
                    ft.Text(label, color=fg, size=14),
                ],
            ),
        )
        sidebar_controls.append(ctrl)
        return ctrl

    sidebar_container.content = ft.Column(
        spacing=10,
        controls=(
            [
                ft.Container(
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            logo_img, 
                            ft.Text("Panel de Administración", size=12, color="#6B7280", text_align=ft.TextAlign.CENTER)
                        ]
                    ),
                    padding=ft.Padding(0, 20, 0, 10),
                    alignment=ft.Alignment(0, 0)
                ),
                ft.Container(height=10) # spacer
            ]
            + [make_item(i,label,icon) for i,(label,icon) in enumerate(sidebar_items)]
            + [sidebar_spacer, logout_ctrl]
        ),
    )

    main_row = ft.Row(
        expand=True,
        controls=[
            sidebar_container,
            content,
        ],
    )

    def on_resize(e):
        if e is not None and hasattr(e, 'data') and isinstance(e.data, dict) and 'width' in e.data:
            w = e.data['width']
        else:
            w = getattr(page, 'width', 0) or 0
        new_sw = max(220, min(300, int(w * 0.22)))
        sidebar_container.width = new_sw
        # El logo ocupa un poco más del ancho de la barra
        logo_img.width = logo_img.height = int(new_sw * 0.6)
        try:
            sidebar_container.update()
            logo_img.update()
        except RuntimeError:
            pass

    page.on_resize = on_resize
    return main_row
