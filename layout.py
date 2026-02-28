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
                                border=ft.Border.all(1, "#E5E7EB"),
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
                                border=ft.Border.all(1, "#E5E7EB"),
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
                                border=ft.Border.all(1, "#E5E7EB"),
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
        # helpers
        def info_row(icon, text):
            return ft.Container(
                bgcolor="#F3F2F1",
                border_radius=8,
                padding=ft.Padding.symmetric(vertical=8, horizontal=12),
                margin=ft.Margin.only(top=8),
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(icon, size=16, color="#6B7280"),
                        ft.Text(text, size=14, color="#374151"),
                    ],
                ),
            )

        def activity_item(title, subtitle, time):
            return ft.Container(
                bgcolor="#F3F2F1",
                border_radius=8,
                padding=ft.padding.symmetric(vertical=10, horizontal=12),
                margin=ft.Margin.only(top=8),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(title, size=14, weight="bold", color="#1F2937"),
                                ft.Text(subtitle, size=12, color="#6B7280"),
                            ],
                        ),
                        ft.Text(time, size=12, color="#9CA3AF"),
                    ],
                ),
            )

        def stat_card(label, value, value_color="#F97316"):
            return ft.Container(
                bgcolor="#F3F2F1",
                border_radius=8,
                padding=ft.Padding.all(12),
                margin=ft.Margin.only(top=8),
                content=ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(label, size=12, color="#6B7280"),
                        ft.Text(value, size=20, weight="bold", color=value_color),
                    ],
                ),
            )

        def sec_option(icon, label, color="#374151", on_click=None, badge_text: str | None = None, badge_bg="#F97316", badge_color="white"):
            # row always holds icon, label, and optional badge
            controls = [
                ft.Icon(icon, size=16, color=color),
                ft.Text(label, size=14, color=color),
            ]
            if badge_text is not None:
                badge = ft.Container(
                    bgcolor=badge_bg,
                    border_radius=8,
                    padding=ft.Padding.symmetric(vertical=4, horizontal=12),
                    content=ft.Text(badge_text, size=14, color=badge_color, weight="bold"),
                )
                controls.append(badge)
            return ft.Container(
                bgcolor="#F3F2F1",
                border_radius=8,
                padding=ft.padding.symmetric(vertical=10, horizontal=12),
                margin=ft.Margin.only(top=8),
                on_click=on_click,
                content=ft.Row(
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                    controls=controls,
                ),
            )

        # initialize edit mode state and stored profile data (prepared for DB later)
        if not hasattr(page, 'is_edit_mode'):
            page.is_edit_mode = False
        if not hasattr(page, 'profile_data'):
            page.profile_data = {
                'name': "Administrador SENA FOOD",
                'role': "Administrador Principal",
                'member_since': "Miembro desde 15 de Enero, 2024",
                'email': "admin@seafood.edu.co",
                'phone': "+57 300 123 4567",
                'location': "SENA Regional Bogotá",
            }

        # header
        edit_btn = ft.Container(
            bgcolor="#F97316",
            border_radius=20,
            padding=ft.Padding.symmetric(vertical=8, horizontal=16),
            on_click=lambda e: setattr(page, 'is_edit_mode', True) or change_view(5),
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Icon(ft.icons.Icons.EDIT, size=16, color="white"),
                    ft.Text("Editar Perfil", size=14, color="white"),
                ],
            ),
        ) if not page.is_edit_mode else ft.Container()

        header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Mi Perfil", size=28, weight="bold", color="#1F2937"),
                        ft.Text("Gestiona tu información de administrador", size=16, color="#6B7280"),
                    ],
                ),
                edit_btn,
            ],
        )

        # avatar container that can resize
        page.avatar_ctrl = ft.Container(
            width=60,
            height=60,
            border_radius=30,
            bgcolor="#F97316",
            content=ft.Icon(ft.icons.Icons.PERSON, color="white", size=32),
        )
        # builder: returns either view-mode card or edit-mode form card
        def build_personal_card(edit_mode: bool):
            if not edit_mode:
                return ft.Container(
                    bgcolor="#FFFFFF",
                    border_radius=16,
                    padding=24,
                    content=ft.Column(
                        spacing=24,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            ft.Row(
                                spacing=12,
                                controls=[
                                    page.avatar_ctrl,
                                    ft.Column(
                                        spacing=4,
                                        controls=[
                                            ft.Text(page.profile_data['name'], size=20, weight="bold", color="#1F2937"),
                                            ft.Text(page.profile_data['role'], size=14, color="#6B7280"),
                                            ft.Text(page.profile_data['member_since'], size=12, color="#9CA3AF"),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Container(ft.Divider(height=1, color="#E5E7EB"), margin=ft.Margin.only(top=0, bottom=0)),
                            info_row(ft.icons.Icons.EMAIL, page.profile_data['email']),
                            info_row(ft.icons.Icons.PHONE, page.profile_data['phone']),
                            info_row(ft.icons.Icons.PLACE, page.profile_data['location']),
                            info_row(ft.icons.Icons.CALENDAR_MONTH, "15 de Enero, 2024"),
                        ],
                    ),
                )

            # Edit mode: form fields with exact visual spec
            def labeled_input(label_text, value, icon):
                label = ft.Text(label_text, size=13, weight="medium", color="#374151")
                # make inputs minimal: no grey background, underline style
                field = ft.TextField(
                    value=value,
                    prefix_icon=ft.Icon(icon, size=16, color="#9CA3AF"),
                    height=44,
                    border=ft.InputBorder.UNDERLINE,
                    border_color="#F3F3F3",
                    filled=False,
                    content_padding=ft.Padding.symmetric(vertical=12, horizontal=14),
                    text_style=ft.TextStyle(size=14, color="#1F2937"),
                )
                return ft.Column(spacing=6, controls=[label, field])

            name_block = labeled_input("Nombre completo", page.profile_data.get('name', ''), ft.icons.Icons.PERSON)
            email_block = labeled_input("Correo electrónico", page.profile_data.get('email', ''), ft.icons.Icons.EMAIL)
            phone_block = labeled_input("Teléfono", page.profile_data.get('phone', ''), ft.icons.Icons.PHONE)
            location_block = labeled_input("Ubicación", page.profile_data.get('location', ''), ft.icons.Icons.PLACE)

            def on_save(e):
                # capture values for future DB integration (temporary storage)
                page.profile_data['name'] = name_block.controls[1].value
                page.profile_data['email'] = email_block.controls[1].value
                page.profile_data['phone'] = phone_block.controls[1].value
                page.profile_data['location'] = location_block.controls[1].value
                page.is_edit_mode = False
                print('Saved profile:', page.profile_data)
                change_view(5)

            def on_cancel(e):
                # discard changes and restore original state
                page.is_edit_mode = False
                change_view(5)

            def on_save_hover(e):
                e.control.bgcolor = "#14532D" if e.data == "true" else "#16A34A"
                e.control.update()

            def on_cancel_hover(e):
                e.control.bgcolor = "#9CA3AF" if e.data == "true" else "#E5E7EB"
                e.control.update()

            save_btn = ft.Container(
                on_click=on_save,
                on_hover=on_save_hover,
                expand=True,
                width=520,
                height=44,
                padding=ft.Padding.symmetric(horizontal=24),
                bgcolor="#16A34A",
                border_radius=22,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8, controls=[
                    ft.Icon(ft.icons.Icons.SAVE, size=16, color="white"),
                    ft.Text("Guardar Cambios", size=14, color="white")
                ]),
            )

            cancel_btn = ft.Container(
                on_click=on_cancel,
                on_hover=on_cancel_hover,
                expand=True,
                width=520,
                height=44,
                padding=ft.Padding.symmetric(horizontal=24),
                border=ft.Border.all(1, "#D1D5DB"),
                border_radius=22,
                bgcolor="#E5E7EB",
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8, controls=[
                    ft.Icon(ft.icons.Icons.CLOSE, size=16, color="#374151"),
                    ft.Text("Cancelar", size=14, color="#374151")
                ]),
            )

            return ft.Container(
                expand=True,
                bgcolor="#FFFFFF",
                border_radius=16,
                padding=24,
                content=ft.Column(
                    spacing=18,
                    expand=True,
                    controls=[
                        ft.Row(
                            spacing=12,
                            controls=[
                                page.avatar_ctrl,
                                ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(page.profile_data.get('name', ''), size=20, weight="bold", color="#1F2937"),
                                        ft.Text(page.profile_data.get('role', ''), size=14, color="#6B7280"),
                                        ft.Text(page.profile_data.get('member_since', ''), size=12, color="#9CA3AF"),
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(ft.Divider(height=1, color="#E5E7EB"), margin=ft.Margin.only(top=0, bottom=0)),
                        name_block,
                        email_block,
                        phone_block,
                        location_block,
                        ft.Row(spacing=16, alignment=ft.MainAxisAlignment.CENTER, controls=[save_btn, cancel_btn], margin=ft.Margin.only(top=28)),
                    ],
                ),
            )

        personal_card = build_personal_card(page.is_edit_mode)

        activity_card = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=16,
            padding=24,
            margin=ft.Margin.only(top=20),
            content=ft.Column(
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Text("Actividad Reciente", size=18, weight="bold", color="#1F2937"),
                    activity_item("Pedido confirmado", "ORD-1247", "Hace 5 min"),
                    activity_item("Producto actualizado", "Bandeja Paisa", "Hace 1 hora"),
                    activity_item("Token verificado", "ABC123XYZ", "Hace 2 horas"),
                    activity_item("Reporte exportado", "Ventas semanal", "Hace 3 horas"),
                ],
            ),
        )

        # left column: allow proportional expansion (flex factor 2)
        # tight=True makes it shrink to its content vertically (no unused height)
        left_col = ft.Column(
            expand=2,
            tight=True,
            controls=[personal_card, activity_card],
        )

        # right column cards (no fixed width)
        stats_card = ft.Container(
            expand=True,
            bgcolor="#FFFFFF",
            border_radius=16,
            padding=24,
            content=ft.Column(
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Text("Estadísticas", size=18, weight="bold", color="#1F2937"),
                    stat_card("Pedidos Gestionados", "156", "#F97316"),
                    stat_card("Productos Activos", "24", "#10B981"),
                    stat_card("Ingresos Totales", "$2,850,000", "#F97316"),
                    stat_card("Clientes Atendidos", "89", "#F97316"),
                ],
            ),
        )

        security_card = ft.Container(
            expand=True,
            bgcolor="#FFFFFF",
            border_radius=16,
            padding=24,
            margin=ft.Margin.only(top=20),
            content=ft.Column(
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Text("Seguridad", size=18, weight="bold", color="#1F2937"),
                    sec_option(ft.icons.Icons.LOCK, "Cambiar contraseña", on_click=lambda e: open_password_modal(e)),
                    sec_option(ft.icons.Icons.QR_CODE, "Configurar Token de Verificación", badge_text="123456", badge_bg="#FFEDD5", badge_color="#F97316"),
                    sec_option(ft.icons.Icons.SHIELD, "Activar 2FA"),
                    sec_option(ft.icons.Icons.EXIT_TO_APP, "Cerrar sesión", color="#EF4444", on_click=lambda e: logout()),
                ],
            ),
        )

        # right column: flex factor 1, no fixed width, shrink-wrap vertically
        right_col = ft.Column(
            expand=1,
            tight=True,
            controls=[stats_card, security_card],
        )

        return ft.Container(
            expand=True,
            bgcolor="#F5F3EE",
            padding=20,
            content=ft.Column(
                spacing=24,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    header,
                    # main row fills available width and splits space 2:1
                    # vertical_alignment=start prevents children from stretching vertically
                    ft.Row(expand=True, spacing=20, vertical_alignment=ft.CrossAxisAlignment.START, controls=[left_col, right_col]),
                ],
            ),
        )

    # sidebar and logo references for resizing
    logo_img = ft.Image(src="img/logo.png", width=70, height=70)
    sidebar_container = ft.Container(
        width=240,  # will adjust via on_resize
        bgcolor="#F9FAFB",
        padding=15,
        border=ft.Border.only(right=ft.BorderSide(1, "#E5E7EB")),
        content=None,  # set later
    )

    # placeholder content; will be replaced once make_item defined
    content = ft.Container(
        expand=True,
        content=dashboard_view(),
    )

    # application state and view registry
    selected_index = 0
    views = {
        0: dashboard_view,
        1: productos_view,
        2: pedidos_view,
        3: token_view,
        4: reportes_view,
        5: perfil_view,
    }

    # list of sidebar definitions (label, icon)
    sidebar_items = [
        ("Dashboard", ft.icons.Icons.DASHBOARD),
        ("Productos", ft.icons.Icons.RESTAURANT),
        ("Pedidos", ft.icons.Icons.SHOPPING_BAG),
        ("Token", ft.icons.Icons.QR_CODE),
        ("Reportes", ft.icons.Icons.BAR_CHART),
        ("Perfil", ft.icons.Icons.PERSON),
    ]

    # controls for each item; we keep them so we can update styling when selection changes
    sidebar_controls: list[ft.Control] = []
    # spacer pushes logout button to bottom (always present)
    sidebar_spacer = ft.Container(expand=True)
    # logout control (visible except on perfil view)
    logout_ctrl = ft.Container(
        padding=ft.Padding.symmetric(vertical=8, horizontal=12),
        margin=ft.Margin.only(top=20),
        on_click=lambda e: logout(),
        content=ft.Row(
            spacing=10,
            controls=[
                ft.Icon(ft.icons.Icons.EXIT_TO_APP, color="#1F2937", size=18),
                ft.Text("Cerrar sesión", color="#1F2937", size=14),
            ],
        ),
    )
    # keep in layout always, but hide visually on perfil view (avoids shifting)
    logout_ctrl.opacity = 0 if selected_index == 5 else 1
    logout_ctrl.disabled = selected_index == 5

    def change_view(i):
        nonlocal selected_index
        selected_index = i
        # update content pane
        content.content = views[i]()
        # restyle each sidebar item
        for idx, ctrl in enumerate(sidebar_controls):
            sel = idx == selected_index
            fg = "white" if sel else "#1F2937"
            ctrl.bgcolor = "#F97316" if sel else "transparent"
            ctrl.shadow = [ft.BoxShadow(color="#F9731660", blur_radius=6, offset=ft.Offset(0,2))] if sel else None
            ctrl.border_radius = 12
            # update icon and text colours
            row = ctrl.content
            row.controls[0].color = fg
            row.controls[1].color = fg
        # toggle logout button appearance without affecting layout
        logout_ctrl.opacity = 0 if selected_index == 5 else 1
        logout_ctrl.disabled = selected_index == 5
        page.update()

    def make_item(idx, label, icon):
        sel = idx == selected_index
        fg = "white" if sel else "#1F2937"
        bg = "#F97316" if sel else "transparent"
        shadow = [ft.BoxShadow(color="#F9731660", blur_radius=6, offset=ft.Offset(0,2))] if sel else None
        # container shrinks to content; no expand
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


    # populate sidebar container now that make_item exists
    sidebar_container.content = ft.Column(
        spacing=10,
        controls=(
            [
                ft.Column(
                    spacing=5,
                    controls=[logo_img, ft.Text("Panel de Administración", size=11, color="#6B7280")]
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

    # responsive resizing: adjust sidebar and avatar when window size changes
    def on_resize(e):
        # width may be provided in the resize event data, otherwise fall back to page.width
        if e is not None and hasattr(e, 'data') and isinstance(e.data, dict) and 'width' in e.data:
            w = e.data['width']
        else:
            w = getattr(page, 'width', 0) or 0
        new_sw = max(220, min(300, int(w * 0.22)))
        sidebar_container.width = new_sw
        logo_img.width = logo_img.height = int(new_sw * 0.35)
        if hasattr(page, 'avatar_ctrl') and page.avatar_ctrl:
            size = int(new_sw * 0.3)
            page.avatar_ctrl.width = page.avatar_ctrl.height = size
        page.update()

    def password_input(label_text, hint_text):
        return ft.Column(
            spacing=4,
            controls=[
                ft.Text(label_text, size=13, weight="bold", color="#374151"),
                ft.TextField(
                    hint_text=hint_text,
                    hint_style=ft.TextStyle(color="#9CA3AF", size=13),
                    password=True,
                    can_reveal_password=True,
                    text_size=14,
                    border_color="#E5E7EB",
                    border=ft.InputBorder.OUTLINE,
                    border_radius=8,
                    bgcolor="#FFFFFF",
                    height=45,
                    content_padding=ft.Padding(left=15, top=2, right=15, bottom=2)
                )
            ]
        )

    import threading
    import time

    def close_password_modal(e):
        modal_overlay.opacity = 0
        modal_content.offset = ft.Offset(0, 1.5)
        modal_overlay.update()
        
        def finalize_close():
            time.sleep(0.3)
            # Only hide if the modal hasn't been reopened
            if modal_overlay.opacity == 0:
                modal_overlay.disabled = True
                modal_overlay.visible = False
                try:
                    modal_overlay.update()
                except Exception:
                    pass
        threading.Thread(target=finalize_close, daemon=True).start()

    def open_password_modal(e):
        if modal_overlay not in page.overlay:
            page.overlay.append(modal_overlay)
            page.update()
            
        modal_overlay.visible = True
        modal_overlay.disabled = False
        modal_overlay.update()
        
        # very short sleep to allow flutter to render the invisible overlay then animate
        def animate_in():
            time.sleep(0.05)
            modal_overlay.opacity = 1
            modal_content.offset = ft.Offset(0, 0)
            try:
                modal_overlay.update()
            except Exception:
                pass
        threading.Thread(target=animate_in, daemon=True).start()

    def confirm_password_change(e):
        print("Contraseña cambiada")
        close_password_modal(e)

    def on_btn_hover(e, color_in, color_out):
        e.control.bgcolor = color_in if e.data == "true" else color_out
        e.control.update()

    modal_content = ft.Container(
        bgcolor="white",
        border_radius=ft.BorderRadius(16, 16, 16, 16),
        padding=ft.Padding(32, 24, 32, 32),
        width=500,
        offset=ft.Offset(0, 1.5),
        animate_offset=ft.Animation(400, ft.AnimationCurve.DECELERATE),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color="#20000000", offset=ft.Offset(0, 10)),
        content=ft.Column(
            tight=True,
            spacing=16,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(spacing=10, controls=[ft.Icon(ft.icons.Icons.LOCK_OUTLINE, color="#374151", size=22), ft.Text("Cambiar Contraseña", size=20, weight="bold", color="#1F2937")]),
                        ft.IconButton(ft.icons.Icons.CLOSE, on_click=close_password_modal, icon_color="#6B7280", width=32, height=32)
                    ]
                ),
                ft.Text("Ingresa tu contraseña actual y la nueva contraseña", size=14, color="#9CA3AF", margin=ft.Margin(0, -5, 0, 5)),
                password_input("Contraseña Actual", "Ingresa tu contraseña actual"),
                password_input("Nueva Contraseña", "Mínimo 8 caracteres"),
                password_input("Confirmar Nueva Contraseña", "Repite la nueva contraseña"),
                ft.Container(height=4),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    spacing=12,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            border_radius=20,
                            border=ft.Border(top=ft.BorderSide(1, "#E5E7EB"), bottom=ft.BorderSide(1, "#E5E7EB"), left=ft.BorderSide(1, "#E5E7EB"), right=ft.BorderSide(1, "#E5E7EB")),
                            bgcolor="white",
                            on_click=close_password_modal,
                            on_hover=lambda e: on_btn_hover(e, "#F3F4F6", "white"),
                            animate=ft.Animation(200),
                            content=ft.Text("Cancelar", size=14, weight="bold", color="#374151"),
                        ),
                        ft.Container(
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            border_radius=20,
                            bgcolor="#F97316",
                            on_click=confirm_password_change,
                            on_hover=lambda e: on_btn_hover(e, "#EA580C", "#F97316"),
                            animate=ft.Animation(200),
                            content=ft.Text("Cambiar Contraseña", size=14, weight="bold", color="white"),
                        ),
                    ]
                )
            ]
        )
    )

    modal_overlay = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        bgcolor="#40000000",
        blur=ft.Blur(10, 10),
        opacity=0,
        disabled=True,
        visible=False,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE),
        content=modal_content,
    )

    page.overlay.append(modal_overlay)

    page.on_resize = on_resize
    on_resize(None)

    return main_row
