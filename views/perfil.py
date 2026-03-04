import flet as ft
from .styles import (
    COLOR_ORANGE_PRIMARY,
    COLOR_ORANGE_DARK,
    COLOR_GRAY_DARK,
    COLOR_GRAY_MEDIUM,
    COLOR_GRAY_LIGHT,
    COLOR_GRAY_TEXT,
    COLOR_BG_LIGHT,
    COLOR_BG_PAGE,
    COLOR_WHITE,
    COLOR_RED_ERROR,
    COLOR_RED_LIGHT,
    COLOR_GREEN_SUCCESS,
    COLOR_GREEN_DARK,
    COLOR_BLUE_INFO,
    COLOR_BLUE_LIGHT,
    COLOR_ORANGE_LIGHT,
    show_toast,
    info_row,
    activity_item,
    stat_card,
    sec_option,
)

def perfil_view(page: ft.Page, change_view, handle_logout):
    # initialize profile data if not exists
    if not hasattr(page, 'is_edit_mode'):
        page.is_edit_mode = False
    if not hasattr(page, 'profile_data'):
        page.profile_data = {
            "name": "Administrador SENA FOOD",
            "role": "Administrador Principal",
            "member_since": "Miembro desde 15 de Enero, 2024",
            "email": "admin@seafood.edu.co",
            "phone": "+57 300 123 4567",
            "location": "SENA Regional Bogotá",
            "verification_token": "123456",
            "avatar_src": None,
        }

    # --- (SIN FilePicker) AVATAR ---
    # Nota: para evitar el error "Unknown control: FilePicker" en tu versión de Flet,
    # la selección de imagen se limita por ahora a un mensaje informativo.

    # --- PASSWORD MODAL HELPERS ---
    def password_input(label_text, hint_text):
        return ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text(label_text, size=13, weight="bold", color=COLOR_GRAY_MEDIUM),
                ft.TextField(
                    hint_text=hint_text,
                    hint_style=ft.TextStyle(color=COLOR_GRAY_TEXT, size=13),
                    password=True,
                    can_reveal_password=True,
                    text_size=14,
                    border_color="transparent",
                    border=ft.InputBorder.OUTLINE,
                    border_radius=16,
                    bgcolor=COLOR_WHITE,
                    height=45,
                    content_padding=ft.Padding(left=15, top=2, right=15, bottom=2)
                )
            ]
        )

    def close_password_modal(e):
        modal_overlay.opacity = 0
        modal_content.offset = ft.Offset(0, 1)
        modal_overlay.disabled = True
        modal_overlay.visible = False
        page.update()
        if e and e.control and getattr(e.control, 'content', None) and getattr(e.control.content, 'value', '') == "Cancelar":
             show_toast(page, "Cambio de contraseña cancelado", title="Seguridad", type="error")

    def open_password_modal(e):
        if modal_overlay not in page.overlay:
            page.overlay.append(modal_overlay)
        modal_overlay.visible = True
        modal_overlay.disabled = False
        modal_overlay.opacity = 1
        modal_content.offset = ft.Offset(0, 0)
        page.update()

    def confirm_password_change(e):
        show_toast(page, "Contraseña actualizada correctamente", title="Seguridad")
        close_password_modal(e)

    def on_btn_hover(e, color_in, color_out):
        e.control.bgcolor = color_in if e.data == "true" else color_out
        e.control.update()

    modal_content = ft.Container(
        bgcolor="#FCFAF8",
        border_radius=24,
        padding=ft.Padding(32, 24, 32, 32),
        width=500,
        offset=ft.Offset(0, 1),
        animate_offset=ft.Animation(700, ft.AnimationCurve.EASE_OUT_BACK),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color="#20000000", offset=ft.Offset(0, 10)),
        content=ft.Column(
            tight=True,
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(spacing=10, controls=[ft.Icon(ft.Icons.LOCK_OUTLINE, color=COLOR_GRAY_MEDIUM, size=22), ft.Text("Cambiar Contraseña", size=20, weight="bold", color=COLOR_GRAY_DARK)]),
                        ft.IconButton(ft.Icons.CLOSE, on_click=close_password_modal, icon_color=COLOR_GRAY_LIGHT, width=32, height=32)
                    ]
                ),
                ft.Text("Ingresa tu contraseña actual y la nueva contraseña", size=14, color=COLOR_GRAY_TEXT, margin=ft.Margin(0, -5, 0, 5)),
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
                            border=ft.Border.all(1, "#E5E7EB"),
                            bgcolor="transparent",
                            on_click=close_password_modal,
                            on_hover=lambda e: on_btn_hover(e, "#F3F4F6", "transparent"),
                            animate=ft.Animation(200),
                            content=ft.Text("Cancelar", size=14, weight="bold", color=COLOR_GRAY_MEDIUM),
                        ),
                        ft.Container(
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            border_radius=20,
                            bgcolor=COLOR_ORANGE_PRIMARY,
                            on_click=confirm_password_change,
                            on_hover=lambda e: on_btn_hover(e, COLOR_ORANGE_DARK, COLOR_ORANGE_PRIMARY),
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

    # --- TOKEN MODAL HELPERS ---
    token_input_field = ft.TextField(
        hint_text="Ingresa el nuevo token",
        bgcolor=COLOR_WHITE,
        border_radius=12,
        border_color="#E5E7EB",
        height=48,
        content_padding=ft.Padding(16, 0, 16, 0),
        text_style=ft.TextStyle(size=14),
    )

    current_token_display = ft.Text(page.profile_data.get('verification_token', '123456'), size=28, weight="bold", color=COLOR_ORANGE_PRIMARY)

    def close_token_modal(e):
        token_modal_overlay.opacity = 0
        token_modal_content.offset = ft.Offset(0, 1)
        token_modal_overlay.disabled = True
        token_modal_overlay.visible = False
        page.update()
        if e and e.control and getattr(e.control, 'content', None) and getattr(e.control.content, 'value', '') == "Cancelar":
            show_toast(page, "Configuración de token cancelada", title="Token", type="error")

    def open_token_modal(e):
        if token_modal_overlay not in page.overlay:
            page.overlay.append(token_modal_overlay)
        current_token_display.value = page.profile_data.get('verification_token', '123456')
        token_input_field.value = ""
        token_modal_overlay.visible = True
        token_modal_overlay.disabled = False
        token_modal_overlay.opacity = 1
        token_modal_content.offset = ft.Offset(0, 0)
        page.update()

    def confirm_token_change(e):
        new_token = token_input_field.value
        if new_token and len(new_token) >= 6:
            page.profile_data['verification_token'] = new_token
            close_token_modal(e)
            show_toast(page, "Token de verificación actualizado", title="Token")
            change_view(5)
            page.update()
        else:
            show_toast(page, "Token inválido (mínimo 6 caracteres)", title="Token", type="error")

    token_modal_content = ft.Container(
        bgcolor="#FCFAF8",
        border_radius=24,
        padding=ft.Padding(32, 24, 32, 32),
        width=500,
        offset=ft.Offset(0, 1),
        animate_offset=ft.Animation(700, ft.AnimationCurve.EASE_OUT_BACK),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color="#20000000", offset=ft.Offset(0, 10)),
        content=ft.Column(
            tight=True,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(spacing=10, controls=[
                            ft.Icon(ft.Icons.AUTO_FIX_HIGH, color=COLOR_GRAY_MEDIUM, size=22), 
                            ft.Text("Configurar Token de Verificación", size=20, weight="bold", color=COLOR_GRAY_DARK)
                        ]),
                        ft.IconButton(ft.Icons.CLOSE, on_click=close_token_modal, icon_color=COLOR_GRAY_LIGHT, width=32, height=32)
                    ]
                ),
                ft.Text("Este token se usará para verificar el acceso al panel de administración", size=14, color=COLOR_GRAY_TEXT, margin=ft.Margin(0, -10, 0, 0)),
                ft.Container(
                    bgcolor="#FFF7ED",
                    padding=20,
                    border_radius=12,
                    border=ft.Border.all(1, "#FFEDD5"),
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text("Token actual:", size=13, weight="medium", color="#C2410C"),
                            current_token_display,
                        ]
                    )
                ),
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("Nuevo Token", size=14, weight="medium", color=COLOR_GRAY_MEDIUM),
                        token_input_field,
                        ft.Text("Puede contener letras, números y caracteres especiales. Mínimo 6 caracteres.", size=12, color=COLOR_GRAY_TEXT),
                    ]
                ),
                ft.Container(
                    bgcolor=COLOR_BLUE_LIGHT,
                    padding=16,
                    border_radius=12,
                    border=ft.Border.all(1, "#DBEAFE"),
                    content=ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=12,
                        controls=[
                            ft.Icon(ft.Icons.INFO_OUTLINE, color=COLOR_BLUE_INFO, size=20),
                            ft.Text(
                                "Importante: Una vez cambiado, deberás usar el nuevo token para iniciar sesión. Guárdalo en un lugar seguro.",
                                size=13,
                                color="#1E40AF",
                                expand=True,
                            )
                        ]
                    )
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    spacing=12,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            border_radius=20,
                            border=ft.Border.all(1, "#E5E7EB"),
                            bgcolor="transparent",
                            on_click=close_token_modal,
                            on_hover=lambda e: on_btn_hover(e, "#F3F4F6", "transparent"),
                            animate=ft.Animation(200),
                            content=ft.Text("Cancelar", size=14, weight="bold", color=COLOR_GRAY_MEDIUM),
                        ),
                        ft.Container(
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            border_radius=20,
                            bgcolor=COLOR_ORANGE_PRIMARY,
                            on_click=confirm_token_change,
                            on_hover=lambda e: on_btn_hover(e, COLOR_ORANGE_DARK, COLOR_ORANGE_PRIMARY),
                            animate=ft.Animation(200),
                            content=ft.Text("Actualizar Token", size=14, weight="bold", color="white"),
                        ),
                    ]
                )
            ]
        )
    )

    token_modal_overlay = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        bgcolor="#40000000",
        blur=ft.Blur(10, 10),
        opacity=0,
        disabled=True,
        visible=False,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE),
        content=token_modal_content,
    )

    # --- TFA MODAL HELPERS ---
    tfa_input_field = ft.TextField(
        hint_text="000 000",
        bgcolor=COLOR_WHITE,
        border_radius=12,
        border_color="#E5E7EB",
        height=48,
        text_align=ft.TextAlign.CENTER,
        text_style=ft.TextStyle(size=16, weight="bold", letter_spacing=2),
        content_padding=ft.Padding(16, 0, 16, 0),
    )

    def close_tfa_modal(e):
        tfa_modal_overlay.opacity = 0
        tfa_modal_content.offset = ft.Offset(0, 1)
        tfa_modal_overlay.disabled = True
        tfa_modal_overlay.visible = False
        page.update()
        if e and e.control and getattr(e.control, 'content', None) and getattr(e.control.content, 'value', '') == "Cancelar":
            show_toast(page, "Activación MFA cancelada", title="MFA", type="error")

    def open_tfa_modal(e):
        if tfa_modal_overlay not in page.overlay:
            page.overlay.append(tfa_modal_overlay)
        tfa_modal_overlay.visible = True
        tfa_modal_overlay.disabled = False
        tfa_modal_overlay.opacity = 1
        tfa_modal_content.offset = ft.Offset(0, 0)
        page.update()

    def confirm_tfa(e):
        code = tfa_input_field.value
        if code and len(code) == 6:
            show_toast(page, "Autenticación 2FA activada", title="MFA")
            close_tfa_modal(e)
        else:
            show_toast(page, "Código 2FA inválido (6 dígitos)", type="error")

    tfa_modal_content = ft.Container(
        bgcolor="#FCFAF8",
        border_radius=24,
        padding=ft.Padding(32, 24, 32, 32),
        width=500,
        offset=ft.Offset(0, 1),
        animate_offset=ft.Animation(700, ft.AnimationCurve.EASE_OUT_BACK),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color="#20000000", offset=ft.Offset(0, 10)),
        content=ft.Column(
            tight=True,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(spacing=10, controls=[
                            ft.Icon(ft.Icons.PHONELINK_LOCK, color=COLOR_GRAY_MEDIUM, size=22), 
                            ft.Text("Autenticación de Dos Factores", size=20, weight="bold", color=COLOR_GRAY_DARK)
                        ]),
                        ft.IconButton(ft.Icons.CLOSE, on_click=close_tfa_modal, icon_color=COLOR_GRAY_LIGHT, width=32, height=32)
                    ]
                ),
                ft.Text("Añade una capa extra de seguridad a tu cuenta", size=14, color=COLOR_GRAY_TEXT, margin=ft.Margin(0, -10, 0, 0)),
                ft.Text("Paso 1: Escanea el código QR", size=14, weight="bold", color=COLOR_GRAY_MEDIUM),
                ft.Container(
                    bgcolor="#F3F4F6",
                    width=200,
                    height=200,
                    border_radius=12,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Icon(ft.Icons.QR_CODE_2, size=100, color=COLOR_GRAY_TEXT),
                            ft.Text("Código QR para\nGoogle Authenticator", size=12, color=COLOR_GRAY_TEXT, text_align=ft.TextAlign.CENTER)
                        ]
                    )
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("O ingresa manualmente: ", size=12, color=COLOR_GRAY_MEDIUM),
                        ft.Container(
                            bgcolor="#F3F4F6",
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=4,
                            content=ft.Text("ABCD - EFGH - IJKL - MNOP", size=12, weight="bold", color=COLOR_GRAY_MEDIUM)
                        )
                    ]
                ),
                ft.Text("Paso 2: Ingresa el código de verificación", size=14, weight="bold", color=COLOR_GRAY_MEDIUM),
                ft.Column(
                    spacing=5,
                    controls=[
                        tfa_input_field,
                        ft.Text("0/6 dígitos", size=11, color=COLOR_GRAY_TEXT, text_align=ft.TextAlign.CENTER)
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    spacing=12,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            border_radius=20,
                            border=ft.Border.all(1, "#E5E7EB"),
                            bgcolor="transparent",
                            on_click=close_tfa_modal,
                            on_hover=lambda e: on_btn_hover(e, "#F3F4F6", "transparent"),
                            animate=ft.Animation(200),
                            content=ft.Text("Cancelar", size=14, weight="bold", color=COLOR_GRAY_MEDIUM),
                        ),
                        ft.Container(
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            border_radius=20,
                            bgcolor="#86EFAC",
                            on_click=confirm_tfa,
                            on_hover=lambda e: on_btn_hover(e, "#4ADE80", "#86EFAC"),
                            animate=ft.Animation(200),
                            content=ft.Text("Activar 2FA", size=14, weight="bold", color="#065F46"),
                        ),
                    ]
                )
            ]
        )
    )

    tfa_modal_overlay = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        bgcolor="#40000000",
        blur=ft.Blur(10, 10),
        opacity=0,
        disabled=True,
        visible=False,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE),
        content=tfa_modal_content,
    )

    # --- MAIN VIEW COMPONENTS ---
    
    # header
    edit_btn = ft.Container(
        bgcolor=COLOR_ORANGE_PRIMARY,
        border_radius=20,
        padding=ft.Padding.symmetric(vertical=8, horizontal=16),
        on_click=lambda e: setattr(page, 'is_edit_mode', True) or change_view(5),
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.EDIT, size=16, color="white"),
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
                    ft.Text("Mi Perfil", size=32, weight="bold", color=COLOR_GRAY_DARK),
                    ft.Text("Gestiona tu información de administrador", size=15, color=COLOR_GRAY_LIGHT),
                ],
            ),
            edit_btn,
        ],
    )

    def _build_avatar(editable: bool):
        avatar_src = page.profile_data.get("avatar_src")
        base = (
            ft.Container(
                width=80,
                height=80,
                border_radius=40,
                bgcolor=COLOR_ORANGE_PRIMARY if not avatar_src else COLOR_WHITE,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS if avatar_src else None,
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Image(
                                src=avatar_src,
                                fit=ft.BoxFit.COVER,
                            )
                            if avatar_src
                            else ft.Icon(
                                ft.Icons.PERSON,
                                color="white",
                                size=48,
                            ),
                            alignment=ft.Alignment(0, 0),
                        )
                    ]
                ),
            )
            if avatar_src
            else ft.Container(
                width=80,
                height=80,
                border_radius=40,
                bgcolor=COLOR_ORANGE_PRIMARY,
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Icon(ft.Icons.PERSON, color="white", size=48),
                            alignment=ft.Alignment(0, 0),
                        )
                    ]
                ),
            )
        )

        if not editable:
            return base

        def on_pick_avatar(e):
            show_toast(
                page,
                "Actualiza tu versión de Flet para habilitar la subida de imagen de perfil.",
                title="Función no disponible",
                type="info",
            )

        return ft.Container(
            width=80,
            height=80,
            on_click=on_pick_avatar,
            content=ft.Stack(
                controls=[
                    base,
                    ft.Container(
                        right=-2,
                        bottom=-2,
                        width=26,
                        height=26,
                        border_radius=13,
                        bgcolor=COLOR_WHITE,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.CAMERA_ALT_OUTLINED,
                            size=14,
                            color=COLOR_ORANGE_PRIMARY,
                        ),
                    ),
                ],
                width=80,
                height=80,
                alignment=ft.Alignment(0, 0),
            ),
        )

    def build_personal_card(edit_mode: bool):
        if not edit_mode:
            return ft.Container(
                bgcolor=COLOR_WHITE,
                border_radius=16,
                padding=24,
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Text("Información Personal", size=18, weight="bold", color=COLOR_GRAY_MEDIUM, margin=ft.Margin(bottom=8, left=0, right=0, top=0)),
                        ft.Row(
                            spacing=20,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                _build_avatar(False),
                                ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text(page.profile_data['name'], size=24, weight="bold", color=COLOR_GRAY_DARK),
                                        ft.Row(spacing=8, controls=[
                                            ft.Icon(ft.Icons.VERIFIED_USER_OUTLINED, size=16, color="#10B981"),
                                            ft.Text(page.profile_data['role'], size=15, color=COLOR_GRAY_LIGHT)
                                        ]),
                                        ft.Text(page.profile_data['member_since'], size=13, color=COLOR_GRAY_TEXT),
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(ft.Divider(height=1, color="#E5E7EB"), margin=ft.Margin.only(top=0, bottom=4)),
                        info_row(ft.Icons.EMAIL, "Correo electrónico", page.profile_data['email']),
                        info_row(ft.Icons.PHONE, "Teléfono", page.profile_data['phone']),
                        info_row(ft.Icons.PLACE, "Ubicación", page.profile_data['location']),
                        info_row(ft.Icons.CALENDAR_MONTH, "Miembro desde", "15 de Enero, 2024"),
                    ],
                ),
            )

        # Edit mode
        def labeled_input(label_text, value, icon):
            field = ft.TextField(
                value=value,
                border=ft.InputBorder.NONE,
                filled=False,
                height=30,
                content_padding=ft.Padding(0, 0, 0, 4),
                text_style=ft.TextStyle(size=15, weight="bold", color=COLOR_GRAY_MEDIUM),
                expand=True,
                cursor_color=COLOR_ORANGE_PRIMARY,
                selection_color=COLOR_ORANGE_LIGHT,
            )
            col = ft.Column(
                spacing=6,
                tight=True,
                controls=[
                    ft.Text(label_text, size=12, color=COLOR_GRAY_LIGHT),
                    ft.Container(
                        width=500,
                        border=ft.Border(bottom=ft.BorderSide(0.8, "#F1F1F1")),
                        padding=ft.Padding(0, 0, 0, 4),
                        content=ft.Row(
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    content=ft.Icon(icon, size=18, color=COLOR_GRAY_TEXT),
                                    margin=ft.Margin(0, 3, 0, 0)
                                ),
                                field
                            ]
                        )
                    )
                ]
            )
            col.data = field
            return col

        name_block = labeled_input("Nombre completo", page.profile_data.get('name', ''), ft.Icons.PERSON)
        email_block = labeled_input("Correo electrónico", page.profile_data.get('email', ''), ft.Icons.EMAIL)
        phone_block = labeled_input("Teléfono", page.profile_data.get('phone', ''), ft.Icons.PHONE)
        location_block = labeled_input("Ubicación", page.profile_data.get('location', ''), ft.Icons.PLACE)

        def on_save(e):
            page.profile_data['name'] = name_block.data.value
            page.profile_data['email'] = email_block.data.value
            page.profile_data['phone'] = phone_block.data.value
            page.profile_data['location'] = location_block.data.value
            page.is_edit_mode = False
            show_toast(page, "Cambios guardados con éxito", title="Perfil")
            change_view(5)

        def on_cancel(e):
            page.is_edit_mode = False
            show_toast(page, "Edición cancelada", title="Perfil", type="error")
            change_view(5)

        def on_save_hover(e):
            e.control.bgcolor = COLOR_GREEN_DARK if e.data == "true" else COLOR_GREEN_SUCCESS
            e.control.update()

        def on_cancel_hover(e):
            e.control.bgcolor = COLOR_GRAY_TEXT if e.data == "true" else "#E5E7EB"
            e.control.update()

        save_btn = ft.Container(
            on_click=on_save,
            on_hover=on_save_hover,
            expand=True,
            width=520,
            height=48,
            padding=ft.Padding.symmetric(horizontal=24),
            bgcolor=COLOR_GREEN_SUCCESS,
            border_radius=24,
            shadow=ft.BoxShadow(
                blur_radius=18,
                spread_radius=-4,
                color="#4016A34A",
                offset=ft.Offset(0, 6),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8, controls=[
                ft.Icon(ft.Icons.SAVE, size=18, color="white"),
                ft.Text("Guardar Cambios", size=15, color="white")
            ]),
        )

        cancel_btn = ft.Container(
            on_click=on_cancel,
            on_hover=on_cancel_hover,
            expand=True,
            width=520,
            height=48,
            padding=ft.Padding.symmetric(horizontal=24),
            border=ft.Border.all(1, "#D1D5DB"),
            border_radius=24,
            bgcolor="#E5E7EB",
             shadow=ft.BoxShadow(
                blur_radius=18,
                spread_radius=-4,
                color="#401F2937",
                offset=ft.Offset(0, 6),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8, controls=[
                ft.Icon(ft.Icons.CLOSE, size=18, color=COLOR_GRAY_MEDIUM),
                ft.Text("Cancelar", size=15, color=COLOR_GRAY_MEDIUM)
            ]),
        )

        return ft.Container(
            expand=True,
            bgcolor=COLOR_WHITE,
            border_radius=16,
            padding=24,
            content=ft.Column(
                spacing=22,
                expand=True,
                controls=[
                            ft.Row(
                                spacing=16,
                                controls=[
                                    _build_avatar(True),
                            ft.Column(
                                spacing=6,
                                controls=[
                                    ft.Text(page.profile_data.get('name', ''), size=24, weight="bold", color=COLOR_GRAY_DARK),
                                    ft.Row(spacing=8, controls=[
                                        ft.Icon(ft.Icons.VERIFIED_USER_OUTLINED, size=16, color="#10B981"),
                                        ft.Text(page.profile_data.get('role', ''), size=16, color=COLOR_GRAY_LIGHT)
                                    ]),
                                    ft.Text(page.profile_data.get('member_since', ''), size=13, color=COLOR_GRAY_TEXT),
                                ],
                            ),
                        ],
                    ),
                    ft.Container(ft.Divider(height=1, color="#E5E7EB"), margin=ft.Margin.only(top=0, bottom=0)),
                    name_block,
                    email_block,
                    phone_block,
                    location_block,
                    ft.Row(spacing=16, alignment=ft.MainAxisAlignment.CENTER, controls=[save_btn, cancel_btn], margin=ft.Margin.only(top=32)),
                ],
            ),
        )

    personal_card = build_personal_card(page.is_edit_mode)

    activity_card = ft.Container(
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=24,
        margin=ft.Margin.only(top=24),
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Actividad Reciente", size=18, weight="bold", color=COLOR_GRAY_MEDIUM, margin=ft.Margin(bottom=8, left=0, right=0, top=0)),
                activity_item("Pedido confirmado", "ORD-1247", "Hace 5 min"),
                activity_item("Producto actualizado", "Bandeja Paisa", "Hace 1 hora"),
                activity_item("Token verificado", "ABC123XYZ", "Hace 2 horas"),
                activity_item("Reporte exportado", "Ventas semanal", "Hace 3 horas"),
            ],
        ),
    )

    left_col = ft.Column(
        col={"sm": 12, "md": 12, "lg": 8, "xl": 8},
        controls=[personal_card, activity_card],
    )

    stats_card = ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=24,
        content=ft.Column(
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Estadísticas", size=18, weight="bold", color=COLOR_GRAY_MEDIUM, margin=ft.Margin(bottom=8, left=0, right=0, top=0)),
                stat_card("Pedidos Gestionados", "156", COLOR_ORANGE_PRIMARY),
                stat_card("Productos Activos", "24", "#10B981"),
                stat_card("Ingresos Totales", "$2,850,000", COLOR_ORANGE_PRIMARY),
                stat_card("Clientes Atendidos", "89", COLOR_ORANGE_PRIMARY),
            ],
        ),
    )

    security_card = ft.Container(
        expand=True,
        bgcolor=COLOR_WHITE,
        border_radius=16,
        padding=24,
        margin=ft.Margin.only(top=24),
        content=ft.Column(
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text(
                    "Seguridad",
                    size=18,
                    weight="bold",
                    color=COLOR_GRAY_MEDIUM,
                    margin=ft.Margin(bottom=8, left=0, right=0, top=0),
                ),
                sec_option(
                    ft.Icons.LOCK_OUTLINE,
                    "Cambiar contraseña",
                    on_click=lambda e: open_password_modal(e),
                ),
                sec_option(
                    ft.Icons.VPN_KEY_OUTLINED,
                    "Configurar Token de Verificación",
                    badge_text=page.profile_data.get("verification_token", "123456"),
                    badge_bg=COLOR_ORANGE_LIGHT,
                    badge_color=COLOR_ORANGE_PRIMARY,
                    on_click=lambda e: open_token_modal(e),
                ),
                sec_option(
                    ft.Icons.EXIT_TO_APP,
                    "Cerrar sesión",
                    color=COLOR_RED_ERROR,
                    on_click=handle_logout,
                ),
            ],
        ),
    )

    right_col = ft.Column(
        col={"sm": 12, "md": 12, "lg": 4, "xl": 4},
        controls=[stats_card, security_card],
    )

    # Initial overlays
    page.overlay.extend([modal_overlay, token_modal_overlay, tfa_modal_overlay])

    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_PAGE,
        padding=24,
        content=ft.Column(
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                header,
                ft.ResponsiveRow(
                    columns=12,
                    spacing=24,
                    run_spacing=24,
                    controls=[left_col, right_col]
                ),
            ],
        ),
    )