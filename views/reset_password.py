import flet as ft
import re
from views.styles import show_toast

def reset_password_view(page: ft.Page, go_login):
    """Tercera y última vista del flujo de recuperación: establecer nueva contraseña."""

    # Estados de los requisitos
    req_status = {
        "length": False,
        "letters": False,
        "numbers": False,
        "match": False
    }

    def get_req_row(text):
        return ft.Row(
            spacing=10,
            controls=[
                ft.Container(
                    width=20,
                    height=20,
                    border_radius=10,
                    bgcolor="#E5E7EB", # Gris por defecto
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                ),
                ft.Text(text, size=14, color="#64748B")
            ]
        )

    req_rows = {
        "length": get_req_row("Al menos 6 caracteres"),
        "letters": get_req_row("Contiene letras (a-z, A-Z)"),
        "numbers": get_req_row("Contiene números (0-9)"),
        "match": get_req_row("Las contraseñas coinciden")
    }

    def update_requirements(e):
        pwd = password_field.value
        confirm = confirm_password_field.value

        # Validaciones
        req_status["length"] = len(pwd) >= 6
        req_status["letters"] = bool(re.search(r'[a-zA-Z]', pwd))
        req_status["numbers"] = bool(re.search(r'\d', pwd))
        req_status["match"] = pwd == confirm and pwd != ""

        # Actualizar UI de los círculos
        for key, status in req_status.items():
            req_rows[key].controls[0].bgcolor = "#22C55E" if status else "#E5E7EB"

        # Actualizar botón
        all_met = all(req_status.values())
        change_button.style.bgcolor = "#22C55E" if all_met else "#91D1A6"
        
        page.update()

    password_field = ft.TextField(
        label="Nueva Contraseña",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.OUTLINE,
        border_radius=12,
        border_color="#D1D5DB",
        focused_border_color="#F97316",
        prefix_icon=ft.Icons.LOCK_OUTLINED,
        on_change=update_requirements,
        width=360,
    )

    confirm_password_field = ft.TextField(
        label="Confirmar Contraseña",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.OUTLINE,
        border_radius=12,
        border_color="#D1D5DB",
        focused_border_color="#F97316",
        prefix_icon=ft.Icons.LOCK_RESET_ROUNDED,
        on_change=update_requirements,
        width=360,
    )

    change_button = ft.FilledButton(
        "Cambiar contraseña",
        width=360,
        height=50,
        disabled=False, # Lo manejamos por color
        style=ft.ButtonStyle(
            bgcolor="#91D1A6",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=lambda _: handle_reset()
    )

    def handle_reset():
        if all(req_status.values()):
            show_toast(page, "Contraseña actualizada", "Tu contraseña ha sido cambiada correctamente")
            go_login()
        else:
            show_toast(page, "Error", "Por favor cumple con todos los requisitos", True)

    # ----------------------------
    # Lado izquierdo (Logo)
    # ----------------------------
    left_side = ft.Container(
        expand=True,
        bgcolor="#FFF9E6",
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Container(
                    width=380,
                    height=380,
                    bgcolor="white",
                    border_radius=30,
                    shadow=ft.BoxShadow(
                        blur_radius=25, spread_radius=1, color="#E5E7EB", offset=ft.Offset(0, 10),
                    ),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Image(src="img/logo.png", width=320, height=320, fit="contain"),
                ),
                ft.Text("SENA FOOD", size=30, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Text("RESTABLECER CONTRASEÑA", size=16, color="#9CA3AF"),
            ],
        ),
    )

    # ----------------------------
    # Lado derecho (Caja de Formulario)
    # ----------------------------
    right_side_content = ft.Container(
        width=460,
        padding=ft.Padding(32, 28, 32, 28),
        bgcolor="white",
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=20, spread_radius=1, color="#E5E7EB", offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Container(
                    padding=16,
                    bgcolor="#E6F4EA", 
                    border_radius=16,
                    content=ft.Icon(ft.Icons.PASSWORD_ROUNDED, color="#34A853", size=32)
                ),
                ft.Container(height=24),
                ft.Text("Nueva Contraseña", size=26, weight=ft.FontWeight.BOLD, color="#1E293B"),
                ft.Container(height=8),
                ft.Text("Crea una contraseña segura para proteger tu cuenta", size=15, color="#64748B", text_align=ft.TextAlign.CENTER),
                ft.Container(height=32),
                
                password_field,
                ft.Container(height=16),
                confirm_password_field,
                ft.Container(height=24),
                
                # Caja de requisitos
                ft.Container(
                    bgcolor="#F8FAFC",
                    padding=20,
                    border_radius=12,
                    width=360,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Row([ft.Icon(ft.Icons.SECURITY_ROUNDED, size=18, color="#64748B"), ft.Text("Requisitos de Contraseña Segura:", size=14, weight=ft.FontWeight.BOLD, color="#475569")]),
                            req_rows["length"],
                            req_rows["letters"],
                            req_rows["numbers"],
                            req_rows["match"],
                        ]
                    )
                ),
                ft.Container(height=32),
                
                change_button,
                ft.Container(height=20),
                ft.TextButton("Volver al inicio de sesión", on_click=lambda _: go_login(), style=ft.ButtonStyle(color="#64748B")),
            ]
        )
    )

    right_side = ft.Container(
        expand=True,
        bgcolor="#F3F4F6",
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[right_side_content]
        )
    )

    return ft.Container(
        expand=True,
        bgcolor="#FDFBF5",
        content=ft.Row(expand=True, controls=[left_side, right_side]),
    )
