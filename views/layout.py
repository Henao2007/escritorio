import flet as ft

def app_layout(page: ft.Page, logout):
    
    def dashboard_view():
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                spacing=25,
                controls=[
                    ft.Text("Dashboard", size=28, weight="bold", color="#1F2937"),
                    ft.Text(f"Bienvenido, {page.session.user}", size=16, color="#6B7280"),
                    
                    # Estadísticas
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Container(
                                width=200,
                                height=120,
                                bgcolor="white",
                                border_radius=10,
                                padding=15,
                                border=ft.border.all(1, "#E5E7EB"),
                                content=ft.Column([
                                    ft.Text("150", size=24, weight="bold", color="#F97316"),
                                    ft.Text("Pedidos Hoy", size=14, color="#6B7280"),
                                ])
                            ),
                            ft.Container(
                                width=200,
                                height=120,
                                bgcolor="white",
                                border_radius=10,
                                padding=15,
                                border=ft.border.all(1, "#E5E7EB"),
                                content=ft.Column([
                                    ft.Text("₡250,000", size=24, weight="bold", color="#10B981"),
                                    ft.Text("Ingresos Hoy", size=14, color="#6B7280"),
                                ])
                            ),
                            ft.Container(
                                width=200,
                                height=120,
                                bgcolor="white",
                                border_radius=10,
                                padding=15,
                                border=ft.border.all(1, "#E5E7EB"),
                                content=ft.Column([
                                    ft.Text("45", size=24, weight="bold", color="#3B82F6"),
                                    ft.Text("Productos", size=14, color="#6B7280"),
                                ])
                            ),
                        ]
                    ),
                ]
            )
        )
    
    def productos_view():
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                ft.Text("Productos", size=28, weight="bold", color="#1F2937"),
                ft.Text("Gestión de productos del menú", size=16, color="#6B7280"),
            ])
        )
    
    def pedidos_view():
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                ft.Text("Pedidos", size=28, weight="bold", color="#1F2937"),
                ft.Text("Gestión de pedidos", size=16, color="#6B7280"),
            ])
        )
    
    def token_view():
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                ft.Text("Token", size=28, weight="bold", color="#1F2937"),
                ft.Text("Gestión de tokens", size=16, color="#6B7280"),
            ])
        )
    
    def reportes_view():
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                ft.Text("Reportes", size=28, weight="bold", color="#1F2937"),
                ft.Text("Reportes y estadísticas", size=16, color="#6B7280"),
            ])
        )
    
    def perfil_view():
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                ft.Text("Perfil", size=28, weight="bold", color="#1F2937"),
                ft.Text(f"Usuario: {page.session.user}", size=16, color="#6B7280"),
                ft.ElevatedButton(
                    "Cerrar sesión", 
                    on_click=lambda e: logout(),
                    width=180,
                    height=40
                ),
            ])
        )

    content = ft.Container(
        expand=True,
        content=dashboard_view(),
    )

    views = {
        0: dashboard_view,
        1: productos_view,
        2: pedidos_view,
        3: token_view,
        4: reportes_view,
        5: perfil_view,
    }

    def on_nav_change(e):
        content.content = views[e.control.selected_index]()
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        on_change=on_nav_change,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=80,
        min_extended_width=180,
        destinations=[
            ft.NavigationRailDestination(
                icon="dashboard",
                selected_icon="dashboard",
                label="Dashboard"
            ),
            ft.NavigationRailDestination(
                icon="restaurant",
                selected_icon="restaurant",
                label="Productos"
            ),
            ft.NavigationRailDestination(
                icon="shopping_bag",
                selected_icon="shopping_bag",
                label="Pedidos"
            ),
            ft.NavigationRailDestination(
                icon="qr_code",
                selected_icon="qr_code",
                label="Token"
            ),
            ft.NavigationRailDestination(
                icon="bar_chart",
                selected_icon="bar_chart",
                label="Reportes"
            ),
            ft.NavigationRailDestination(
                icon="person",
                selected_icon="person",
                label="Perfil"
            ),
        ],
    )

    logout_btn = ft.IconButton(
        icon="logout",
        icon_size=24,
        tooltip="Cerrar sesión",
        on_click=lambda e: logout(),
    )

    return ft.Row(
        expand=True,
        controls=[
            ft.Container(
                width=180,
                bgcolor="#F9FAFB",
                padding=15,
                border=ft.border.only(right=ft.border.BorderSide(1, "#E5E7EB")),
                content=ft.Column(
                    spacing=25,
                    controls=[
                        ft.Image(src="img/logo.png", width=80, height=80),
                        rail,
                        ft.Divider(height=1, color="#E5E7EB"),
                        ft.Container(
                            padding=ft.padding.symmetric(vertical=10),
                            content=ft.Column(
                                spacing=5,
                                controls=[
                                    ft.Text("Usuario", size=12, color="#6B7280"),
                                    ft.Text(f"{page.session.user.split('@')[0]}", size=14, weight="bold"),
                                ]
                            )
                        ),
                        logout_btn,
                    ]
                ),
            ),
            content,
        ],
    )