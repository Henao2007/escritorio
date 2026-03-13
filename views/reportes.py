import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

import flet as ft
from .styles import (
    COLOR_ORANGE_PRIMARY,
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
from controllers.reportes import get_reporte_completo


def _fmt_dinero(valor: float) -> str:
    """2850000.0  →  '$ 2.850.000'"""
    return f"$ {int(valor):,}".replace(",", ".")


def _color_por_pedidos(cant: int) -> str:
    """
    1 pedido  → amarillo  (poco volumen)
    2 pedidos → naranja   (volumen medio)
    3+pedidos → verde     (barra llena)
    """
    if cant >= 3:
        return "#22C55E"   # verde
    elif cant == 2:
        return "#F97316"   # naranja
    else:
        return "#EAB308"   # amarillo




def reportes_view(page: ft.Page):

    # ── 1. Cargar datos reales desde la BD ───────────────────────────────
    raw = get_reporte_completo()

    # Paleta de colores para los métodos de pago
    COLORES = [
        COLOR_GREEN_SUCCESS,
        COLOR_ORANGE_PRIMARY,
        "#3B82F6",
        "#8B5CF6",
        "#EC4899",
    ]

    def _construir_report_data(raw: dict) -> dict:
        """Convierte el dict del controlador al formato interno de la UI."""
        result = {}
        periodo_label = {
            "Hoy":         "Diario",
            "Esta Semana": "Semanal",
            "Este Mes":    "Mensual",
            "Este Año":    "Anual",
        }
        for filtro, datos in raw.items():
            tendencia = datos["tendencia"]
            result[filtro] = {
                "stats": [
                    ("Ingresos Totales", _fmt_dinero(datos["ingresos"]), tendencia),
                    ("Total de Pedidos", str(datos["pedidos"]),          periodo_label[filtro]),
                ],
                "payments": [
                    (nombre, f"({cant} pedidos)", _fmt_dinero(monto), pct, COLORES[i % len(COLORES)])
                    for i, (nombre, cant, monto, pct) in enumerate(datos["metodos"])
                ] if datos["metodos"] else [],
            }
        return result

    report_data = _construir_report_data(raw)

    # ── 2. Componentes de UI ─────────────────────────────────────────────
    stats_row          = ft.Row(spacing=20)
    payments_chart_col = ft.Column(spacing=16, animate_opacity=300)
    filter_pills       = {}

    def update_ui(selected_filter):
        # Actualizar estilos de pills
        for label, pill in filter_pills.items():
            is_sel = (label == selected_filter)
            pill.bgcolor = COLOR_ORANGE_PRIMARY if is_sel else "transparent"
            pill.border  = None if is_sel else ft.Border.all(1, "#E5E7EB")
            pill.shadow  = ft.BoxShadow(
                color="#40F97316", blur_radius=6, offset=ft.Offset(0, 2)
            ) if is_sel else None
            pill.content.weight = "bold"   if is_sel else "medium"
            pill.content.color  = "white"  if is_sel else COLOR_GRAY_MEDIUM
            pill.update()

        # Fade out → actualizar datos → fade in
        payments_chart_col.opacity = 0
        payments_chart_col.update()

        data = report_data[selected_filter]

        # Tarjetas de stats
        stats_row.controls = [
            report_stat_card(
                label,
                value,
                trend=trend   if trend.startswith("+") or trend.startswith("-") else None,
                subtext=f"Período: {trend}" if not (trend.startswith("+") or trend.startswith("-")) else None,
            )
            for label, value, trend in data["stats"]
        ]
        stats_row.update()

        # Barras de métodos de pago
        if data["payments"]:
            payments_chart_col.controls = [
                chart_bar(
                    f"{name} {sub}",
                    f"{amount} {pct}%",
                    pct,
                    color=_color_por_pedidos(cant_raw),
                )
                for (name, sub, amount, pct, _color), cant_raw in zip(
                    data["payments"],
                    [d[1] for d in raw[selected_filter]["metodos"]],
                )
            ]
        else:
            payments_chart_col.controls = [
                ft.Text(
                    "Sin datos de pagos aprobados para este período.",
                    color=COLOR_GRAY_TEXT,
                    size=14,
                    italic=True,
                )
            ]

        payments_chart_col.opacity = 1
        payments_chart_col.update()

    # ── 3. Exportar reporte como PDF ─────────────────────────────────────
    def handle_export(e):
        export_btn.disabled = True
        export_btn.content.controls[0].icon  = ft.Icons.REFRESH
        export_btn.content.controls[1].value = "Exportando..."
        export_btn.update()
        try:
            timestamp      = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename       = f"Reporte_Financiero_{timestamp}.pdf"
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads_path):
                downloads_path = os.getcwd()
            file_path = os.path.join(downloads_path, filename)

            doc    = SimpleDocTemplate(file_path, pagesize=A4,
                                       leftMargin=2*cm, rightMargin=2*cm,
                                       topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            story  = []

            # ── Título ──────────────────────────────────────────────────
            title_style = ParagraphStyle(
                "title", parent=styles["Title"],
                fontSize=22, textColor=colors.HexColor("#1F2937"),
                spaceAfter=4,
            )
            sub_style = ParagraphStyle(
                "sub", parent=styles["Normal"],
                fontSize=11, textColor=colors.HexColor("#6B7280"),
                spaceAfter=16,
            )
            story.append(Paragraph("Reportes Financieros – SENA FOOD", title_style))
            story.append(Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                sub_style,
            ))
            story.append(Spacer(1, 0.4*cm))

            # ── Tabla por cada período ───────────────────────────────────
            header_style = ParagraphStyle(
                "hdr", parent=styles["Heading2"],
                fontSize=13, textColor=colors.HexColor("#F97316"),
                spaceBefore=12, spaceAfter=6,
            )

            for periodo, datos in raw.items():
                story.append(Paragraph(periodo, header_style))

                # Tarjetas de stats
                stats_data = [
                    ["Métrica", "Valor"],
                    ["Ingresos Totales", _fmt_dinero(datos["ingresos"])],
                    ["Total de Pedidos", str(datos["pedidos"])],
                ]
                stats_table = Table(stats_data, colWidths=[8*cm, 8*cm])
                stats_table.setStyle(TableStyle([
                    ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#F97316")),
                    ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
                    ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE",     (0, 0), (-1, 0), 11),
                    ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [colors.HexColor("#F9FAFB"), colors.white]),
                    ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                    ("FONTSIZE",     (0, 1), (-1, -1), 10),
                    ("TOPPADDING",   (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
                ]))
                story.append(stats_table)
                story.append(Spacer(1, 0.3*cm))

                # Métodos de pago
                if datos["metodos"]:
                    metodos_data = [["Método de Pago", "Pedidos", "Monto", "%"]]
                    for nombre, cant, monto, pct in datos["metodos"]:
                        metodos_data.append([nombre, str(cant), _fmt_dinero(monto), f"{pct}%"])
                    metodos_table = Table(metodos_data, colWidths=[5*cm, 3*cm, 5*cm, 3*cm])
                    metodos_table.setStyle(TableStyle([
                        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#22C55E")),
                        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
                        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                         [colors.HexColor("#F0FDF4"), colors.white]),
                        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                        ("FONTSIZE",     (0, 0), (-1, -1), 10),
                        ("TOPPADDING",   (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
                    ]))
                    story.append(metodos_table)

                story.append(Spacer(1, 0.5*cm))

            doc.build(story)
            show_toast(page, f"PDF guardado en Downloads: {filename}", "¡Éxito!", type="success")

        except Exception as ex:
            show_toast(page, f"Error al exportar: {str(ex)}", "Error", type="error")
        finally:
            export_btn.disabled = False
            export_btn.content.controls[0].icon  = ft.Icons.FILE_DOWNLOAD_OUTLINED
            export_btn.content.controls[1].value = "Exportar Reporte"
            export_btn.update()

    # ── 4. Crear filter pills (Hoy / Esta Semana / Este Mes / Este Año) ──
    filter_labels    = ["Hoy", "Esta Semana", "Este Mes", "Este Año"]
    selected_default = "Hoy"

    for label in filter_labels:
        filter_pills[label] = filter_pill(
            label,
            selected=(label == selected_default),
            on_click=lambda e, l=label: update_ui(l),
        )

    # ── 5. Datos iniciales ───────────────────────────────────────────────
    initial_data = report_data[selected_default]

    stats_row.controls = [
        report_stat_card(
            label,
            value,
            trend=trend   if trend.startswith("+") or trend.startswith("-") else None,
            subtext=f"Período: {trend}" if not (trend.startswith("+") or trend.startswith("-")) else None,
        )
        for label, value, trend in initial_data["stats"]
    ]

    if initial_data["payments"]:
        payments_chart_col.controls = [
            chart_bar(
                f"{name} {sub}",
                f"{amount} {pct}%",
                pct,
                color=_color_por_pedidos(cant_raw),
            )
            for (name, sub, amount, pct, _c), cant_raw in zip(
                initial_data["payments"],
                [d[1] for d in raw[selected_default]["metodos"]],
            )
        ]
    else:
        payments_chart_col.controls = [
            ft.Text(
                "Sin datos de pagos aprobados para este período.",
                color=COLOR_GRAY_TEXT,
                size=14,
                italic=True,
            )
        ]

    # ── 6. Layout final ──────────────────────────────────────────────────
    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG_PAGE,
        padding=ft.Padding(40, 40, 60, 40),
        content=ft.ListView(
            expand=True,
            spacing=30,
            controls=[
                # Header: título + botón exportar
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    "Reportes Financieros",
                                    size=32, weight="bold", color=COLOR_GRAY_DARK,
                                ),
                                ft.Text(
                                    "Análisis detallado de ventas e ingresos",
                                    size=16, color=COLOR_GRAY_TEXT,
                                ),
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
                            on_click=lambda e: handle_export(e),
                            on_hover=lambda e: (
                                setattr(e.control, "scale", 1.05 if e.data == "true" else 1.0),
                                e.control.update(),
                            ),
                            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
                        ),
                    ],
                ),

                # Filtros de período
                ft.Row(
                    spacing=12,
                    controls=list(filter_pills.values()),
                ),

                # Tarjetas de estadísticas
                stats_row,

                # Métodos de pago
                ft.Container(
                    bgcolor=COLOR_WHITE,
                    padding=32,
                    border_radius=20,
                    border=ft.Border.all(1, "#F3EFEA"),
                    content=ft.Column(
                        spacing=20,
                        controls=[
                            ft.Text(
                                "Métodos de Pago",
                                size=18, weight="bold", color=COLOR_GRAY_DARK,
                            ),
                            payments_chart_col,
                        ],
                    ),
                ),

                ft.Container(height=20),
            ],
        ),
    )