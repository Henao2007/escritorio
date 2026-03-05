import base64
import os
from datetime import datetime

import flet as ft
from .styles import (
    COLOR_ORANGE_PRIMARY,
    COLOR_ORANGE_LIGHT,
    COLOR_GRAY_DARK,
    COLOR_GRAY_MEDIUM,
    COLOR_GRAY_TEXT,
    COLOR_BG_PAGE,
    COLOR_WHITE,
    COLOR_GREEN_SUCCESS,
    report_stat_card,
    chart_bar,
    filter_pill,
    show_toast,
)

def reportes_view(page: ft.Page):
    # --- DATA DEFINITIONS ---
    report_data = {
        "Esta Semana": {
            "stats": [
                ("Ingresos Totales", "$ 2.850.000", "+12.2%"),
                ("Total de Pedidos", "156", "Semanal"),
            ],
            "payments": [
                ("Nequi", "(64 pedidos)", "$ 1.170.000", 41, COLOR_GREEN_SUCCESS),
            ],
        },
        "Este Mes": {
            "stats": [
                ("Ingresos Totales", "$ 11.400.000", "+11.8%"),
                ("Total de Pedidos", "624", "Mensual"),
            ],
            "payments": [
                ("Efectivo", "(92 pedidos)", "$ 1.680.000", 59, COLOR_GREEN_SUCCESS),
            ],
        },
        "Este Año": {
            "stats": [
                ("Ingresos Totales", "$ 136.800.000", "+11.8%"),
                ("Total de Pedidos", "7488", "Anual"),
            ],
            "payments": [
                ("Nequi", "(64 pedidos)", "$ 1.170.000", 41, COLOR_GREEN_SUCCESS),
            ],
        },
    }

    # --- UI COMPONENTS ---
    stats_row = ft.Row(spacing=20)
    payments_chart_col = ft.Column(spacing=16, animate_opacity=300)
    filter_pills = {}

    def update_ui(selected_filter):
        for label, pill in filter_pills.items():
            is_sel = (label == selected_filter)
            pill.bgcolor = COLOR_ORANGE_PRIMARY if is_sel else "transparent"
            pill.border = None if is_sel else ft.Border.all(1, "#E5E7EB")
            pill.shadow = ft.BoxShadow(color="#40F97316", blur_radius=6, offset=ft.Offset(0, 2)) if is_sel else None
            pill.data = is_sel
            pill.content.weight = "bold" if is_sel else "medium"
            pill.content.color = "white" if is_sel else COLOR_GRAY_MEDIUM
            pill.update()

        payments_chart_col.opacity = 0
        payments_chart_col.update()

        data = report_data[selected_filter]

        stats_row.controls = [
            report_stat_card(
                label,
                value,
                trend=trend if trend.startswith("+") else None,
                subtext=f"Período: {trend}" if not trend.startswith("+") else None,
            )
            for label, value, trend in data["stats"]
        ]
        stats_row.update()

        payments_chart_col.controls = [
            chart_bar(f"{name}{sub}", f"{amount} {pct}%", pct, color=color)
            for name, sub, amount, pct, color in data["payments"]
        ]
        payments_chart_col.opacity = 1
        payments_chart_col.update()

    async def handle_export(e):
        export_btn.disabled = True
        export_btn.content.controls[0].icon = ft.Icons.REFRESH
        export_btn.content.controls[1].value = "Exportando..."
        export_btn.update()
        show_toast(page, "Capturando reporte...", "Iniciando")
        try:
            shot_base64 = await page.get_screenshot()
            if shot_base64:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"Reporte_Financiero_{timestamp}.png"
                img_data = base64.b64decode(shot_base64)
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                if not os.path.exists(downloads_path):
                    downloads_path = os.getcwd()
                file_path = os.path.join(downloads_path, filename)
                with open(file_path, "wb") as f:
                    f.write(img_data)
                show_toast(page, f"Guardado en: {filename}", "¡Éxito!", type="success")
            else:
                show_toast(page, "Error al capturar pantalla.", "Error", type="error")
        except Exception as ex:
            show_toast(page, f"Error: {str(ex)}", "Error", type="error")
        export_btn.disabled = False
        export_btn.content.controls[0].icon = ft.Icons.FILE_DOWNLOAD_OUTLINED
        export_btn.content.controls[1].value = "Exportar Reporte"
        export_btn.update()

    # Create filter pills
    filter_labels = ["Esta Semana", "Este Mes", "Este Año"]
    for label in filter_labels:
        filter_pills[label] = filter_pill(
            label,
            selected=(label == "Esta Semana"),
            on_click=lambda e, l=label: update_ui(l),
        )

    # --- INITIAL DATA ---
    initial_data = report_data["Esta Semana"]
    stats_row.controls = [
        report_stat_card(
            label,
            value,
            trend=trend if trend.startswith("+") else None,
            subtext=f"Período: {trend}" if not trend.startswith("+") else None,
        )
        for label, value, trend in initial_data["stats"]
    ]
    payments_chart_col.controls = [
        chart_bar(f"{name}{sub}", f"{amount} {pct}%", pct, color=color)
        for name, sub, amount, pct, color in initial_data["payments"]
    ]

    # ListView llena toda la altura → fondo COLOR_BG_PAGE sin recortes blancos
    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_PAGE,
        padding=ft.Padding(40, 40, 60, 40),
        content=ft.ListView(
            expand=True,
            spacing=30,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text("Reportes Financieros", size=32, weight="bold", color=COLOR_GRAY_DARK),
                                ft.Text("Análisis detallado de ventas e ingresos", size=16, color=COLOR_GRAY_TEXT),
                            ],
                        ),
                        export_btn := ft.Container(
                            content=ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.FILE_DOWNLOAD_OUTLINED, color="white", size=20),
                                    ft.Text("Exportar Reporte", color="white", weight="bold", size=14),
                                ],
                            ),
                            bgcolor=COLOR_GREEN_SUCCESS,
                            padding=ft.Padding(20, 12, 20, 12),
                            border_radius=30,
                            on_click=handle_export,
                            on_hover=lambda e: setattr(e.control, "scale", 1.05 if e.data == "true" else 1.0) or e.control.update(),
                            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
                        ),
                    ],
                ),
                stats_row,
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    padding=32,
                    border_radius=20,
                    border=ft.Border.all(1, "#F3EFEA"),
                    content=ft.Column(
                        spacing=20,
                        controls=[
                            ft.Text("Métodos de Pago", size=18, weight="bold", color=COLOR_GRAY_DARK),
                            payments_chart_col,
                        ],
                    ),
                ),
                ft.Container(height=20),
            ],
        ),
    )
