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
                ("Ticket Promedio", "$ 18.269", "Por pedido"),
                ("Crecimiento", "$ 310.000", "Anterior"),
            ],
            "daily": [
                ("Lunes", "$ 450.000", 28, 75),
                ("Martes", "$ 520.000", 32, 85),
                ("Miércoles", "$ 480.000", 26, 80),
                ("Jueves", "$ 550.000", 34, 90),
                ("Viernes", "$ 620.000", 36, 100),
                ("Sábado", "$ 230.000", 12, 40),
                ("Domingo", "$ 0", 0, 0),
            ],
            "payments": [
                ("Nequi", "(64 pedidos)", "$ 1.170.000", 41, COLOR_GREEN_SUCCESS),
            ]
        },
        "Este Mes": {
            "stats": [
                ("Ingresos Totales", "$ 11.400.000", "+11.8%"),
                ("Total de Pedidos", "624", "Mensual"),
                ("Ticket Promedio", "$ 18.269", "Por pedido"),
                ("Crecimiento", "$ 1.200.000", "Anterior"),
            ],
            "daily": [
                ("Semana 1", "$ 2.850.000", 156, 85),
                ("Semana 2", "$ 3.100.000", 168, 92),
                ("Semana 3", "$ 2.950.000", 160, 88),
                ("Semana 4", "$ 2.500.000", 140, 75),
            ],
            "payments": [
                ("Efectivo", "(92 pedidos)", "$ 1.680.000", 59, COLOR_GREEN_SUCCESS),
            ]
        },
        "Este Año": {
            "stats": [
                ("Ingresos Totales", "$ 136.800.000", "+11.8%"),
                ("Total de Pedidos", "7488", "Anual"),
                ("Ticket Promedio", "$ 18.269", "Por pedido"),
                ("Crecimiento", "$ 14.400.000", "Anterior"),
            ],
            "daily": [
                ("Ene-Mar", "$ 34.200.000", 1872, 80),
                ("Abr-Jun", "$ 36.500.000", 1920, 85),
                ("Jul-Sep", "$ 32.800.000", 1840, 78),
                ("Oct-Dic", "$ 33.300.000", 1856, 79),
            ],
            "payments": [
                ("Nequi", "(64 pedidos)", "$ 1.170.000", 41, COLOR_GREEN_SUCCESS),
            ]
        }
    }

    # --- UI COMPONENTS ---
    stats_row = ft.Row(spacing=20)
    daily_chart_col = ft.Column(spacing=16, animate_opacity=300)
    payments_chart_col = ft.Column(spacing=16, animate_opacity=300)
    daily_card_title = ft.Text(
        "Desglose Diario", size=18, weight="bold", color=COLOR_GRAY_DARK
    )

    # Filter control references
    filter_pills = {}
    selected_date_text = ft.Text("Hoy", size=13, color=COLOR_GRAY_MEDIUM)

    def on_date_change(e):
        """Actualiza el texto cuando el usuario elige una fecha en el calendario."""
        if not e.control.value:
            return
        dt = e.control.value
        try:
            selected_date_text.value = dt.strftime("%d/%m/%Y")
        except Exception:
            selected_date_text.value = str(dt)
        selected_date_text.update()

    # Calendario real (DatePicker) para seleccionar día, mes y año
    date_picker = ft.DatePicker(
        on_change=on_date_change,
        first_date=datetime(2024, 1, 1),
        last_date=datetime(2030, 12, 31),
    )

    def update_ui(selected_filter):
        # Update filter pill visual states
        for label, pill in filter_pills.items():
            is_sel = (label == selected_filter)
            pill.bgcolor = COLOR_ORANGE_PRIMARY if is_sel else "transparent"
            pill.border = None if is_sel else ft.Border.all(1, "#E5E7EB")
            pill.shadow = ft.BoxShadow(color="#40F97316", blur_radius=6, offset=ft.Offset(0, 2)) if is_sel else None
            pill.data = is_sel
            pill.content.weight = "bold" if is_sel else "medium"
            pill.content.color = "white" if is_sel else COLOR_GRAY_MEDIUM
            pill.update()
        
        # Fade out content
        daily_chart_col.opacity = 0
        payments_chart_col.opacity = 0
        daily_chart_col.update()
        payments_chart_col.update()
        
        data = report_data[selected_filter]
        
        # Update Stats
        stats_row.controls = [
            report_stat_card(label, value, trend=trend if trend.startswith("+") else None, subtext=f"Período: {trend}" if not trend.startswith("+") else None)
            for label, value, trend in data["stats"]
        ]
        stats_row.update()
        
        # Update Daily Chart
        daily_card_title.value = "Desglose por Período" if selected_filter != "Esta Semana" else "Desglose Diario"
        daily_card_title.update()
        
        daily_chart_col.controls = [
            chart_bar(label, f"{amount} ({pedidos} pedidos)", pct)
            for label, amount, pedidos, pct in data["daily"]
        ]
        
        # Update Payments
        payments_chart_col.controls = [
            chart_bar(f"{name}{sub}", f"{amount} {pct}%", pct, color=color)
            for name, sub, amount, pct, color in data["payments"]
        ]
        
        # Fade in content
        daily_chart_col.opacity = 1
        payments_chart_col.opacity = 1
        daily_chart_col.update()
        payments_chart_col.update()

    async def handle_export(e):
        # 1. Loading state
        export_btn.disabled = True
        export_btn.content.controls[0].icon = ft.Icons.REFRESH
        export_btn.content.controls[1].value = "Exportando..."
        export_btn.update()
        
        show_toast(page, "Capturando reporte...", "Iniciando")
        
        try:
            # 2. Capture screenshot
            # page.get_screenshot() returns base64
            shot_base64 = await page.get_screenshot()
            
            if shot_base64:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"Reporte_Financiero_{timestamp}.png"
                
                # Decode and save to Downloads
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
        
        # 3. Restore button
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
            on_click=lambda e, l=label: update_ui(l)
        )

    # --- INITIAL LAYOUT ---
    # Populate initial data
    initial_data = report_data["Esta Semana"]
    stats_row.controls = [
        report_stat_card(label, value, trend=trend if trend.startswith("+") else None, subtext=f"Período: {trend}" if not trend.startswith("+") else None)
        for label, value, trend in initial_data["stats"]
    ]
    daily_chart_col.controls = [
        chart_bar(label, f"{amount} ({pedidos} pedidos)", pct)
        for label, amount, pedidos, pct in initial_data["daily"]
    ]
    payments_chart_col.controls = [
        chart_bar(f"{name}{sub}", f"{amount} {pct}%", pct, color=color)
        for name, sub, amount, pct, color in initial_data["payments"]
    ]

    filter_icon_container = ft.Container(
        padding=ft.Padding(8, 6, 10, 6),
        border_radius=12,
        border=ft.Border.all(1, "#E5E7EB"),
        bgcolor=COLOR_BG_PAGE,
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Icon(
                    ft.Icons.CALENDAR_MONTH_OUTLINED,
                    color=COLOR_GRAY_TEXT,
                    size=20,
                ),
                selected_date_text,
            ],
        ),
    )

    def open_date_picker(e):
        # Abre el calendario nativo de Flet para elegir fecha completa
        try:
            date_picker.pick_date()
        except Exception:
            show_toast(
                page,
                "No se pudo abrir el calendario.\nVerifica tu versión de Flet.",
                "Error de calendario",
                type="error",
            )

    filter_icon_container.on_click = open_date_picker

    filter_container = ft.Container(
        bgcolor=COLOR_WHITE,
        padding=20,
        border_radius=16,
        border=ft.Border.all(1, "#F3EFEA"),
        content=ft.Row(
            spacing=15,
            controls=[
                filter_icon_container,
                filter_pills["Esta Semana"],
                filter_pills["Este Mes"],
                filter_pills["Este Año"],
            ],
        )
    )

    main_container = ft.Container(
        expand=True,
        padding=ft.Padding(40, 40, 60, 40),
        bgcolor=COLOR_BG_PAGE,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
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
                            ]
                        ),
                        export_btn := ft.Container(
                            content=ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.FILE_DOWNLOAD_OUTLINED, color="white", size=20),
                                    ft.Text("Exportar Reporte", color="white", weight="bold", size=14),
                                ]
                            ),
                            bgcolor=COLOR_GREEN_SUCCESS,
                            padding=ft.Padding(20, 12, 20, 12),
                            border_radius=30,
                            on_click=handle_export,
                            on_hover=lambda e: setattr(e.control, "scale", 1.05 if e.data == "true" else 1.0) or e.control.update(),
                            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
                        )
                    ]
                ),
                filter_container,
                stats_row,
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    padding=32,
                    border_radius=20,
                    border=ft.Border.all(1, "#F3EFEA"),
                    content=ft.Column(
                        spacing=20,
                        controls=[
                            daily_card_title,
                            daily_chart_col
                        ]
                    )
                ),
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    padding=32,
                    border_radius=20,
                    border=ft.Border.all(1, "#F3EFEA"),
                    content=ft.Column(
                        spacing=20,
                        controls=[
                            ft.Text("Métodos de Pago", size=18, weight="bold", color=COLOR_GRAY_DARK),
                            payments_chart_col
                        ]
                    )
                ),
                ft.Container(height=20)
            ]
        )
    )

    # Registramos el DatePicker en el overlay de la página para que funcione el botón
    try:
        if date_picker not in page.overlay:
            page.overlay.append(date_picker)
    except Exception:
        # Si el overlay no está disponible, simplemente ignoramos el error
        pass

    return main_container
