from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_pdf(nombre, cedula, datos):
    # Nombre del archivo basado en el conductor
    file_path = f"Colilla_{nombre.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    def money(valor):
        return f"${abs(valor):,.0f}"

    # --- ENCABEZADO ---
    if os.path.exists("static/logo.png"):
        c.drawImage("static/logo.png", 50, 710, width=100, height=50)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(160, 740, "WHEELGRIN S.A.S.")
    c.setFont("Helvetica", 10)
    c.drawString(160, 725, "NIT: 901216088-9")
    c.drawRightString(550, 740, "SOPORTE DE PAGO")
    c.drawRightString(550, 725, datetime.now().strftime("%d/%m/%Y %H:%M"))

    y = 680
    # --- INFO CONDUCTOR (Recuadro sutil) ---
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(50, y-35, 500, 45, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y-5, f"CONDUCTOR: {nombre.upper()}")
    c.drawString(60, y-25, f"IDENTIFICACIÓN: {cedula}")

    y -= 70
    # --- TABLA DE CONCEPTOS ---
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.rect(50, y, 500, 20, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y+6, "DESCRIPCIÓN")
    c.drawRightString(540, y+6, "VALOR")

    y -= 20
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)
    
    # Desglose para el PDF
    conceptos = [
        ("Efectivo total reportado (+)", datos['efectivo']),
        ("Gasto de Gasolina (-)", datos['gasolina']),
        ("Gastos Operativos / Otros (-)", datos['operativos']),
        ("Comisión por servicios (-)", datos['comision']),
        ("Horas Extras y Recargos (-)", datos['extras']),
        ("Bonificaciones semanales (-)", datos['bono']),
    ]

    for i, (texto, valor) in enumerate(conceptos):
        if i % 2 == 0:
            c.setFillColorRGB(0.98, 0.98, 0.98)
            c.rect(50, y, 500, 18, fill=1, stroke=0)
        
        c.setFillColorRGB(0, 0, 0)
        c.drawString(60, y+5, texto)
        c.drawRightString(540, y+5, money(valor))
        y -= 18

    # --- NUEVO: RESUMEN DE HORAS (Detalle técnico) ---
    y -= 15
    c.setFont("Helvetica-BoldOblique", 9)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    # Extraemos las horas del diccionario si las pasas, 
    # por ahora usamos el total de extras como referencia
    c.drawString(60, y, f"* Incluye el pago de horas extra y recargos festivos calculados.")
    
    # --- TOTALES FINALES ---
    y -= 25
    c.setLineWidth(1.5)
    c.line(50, y, 550, y)
    
    y -= 25
    res = datos['resultado']
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)
    if res > 0:
        [span_3](start_span)c.drawString(50, y, "SALDO A FAVOR DE EMPRESA (ENTREGAR):")[span_3](end_span)
    else:
        [span_4](start_span)c.drawString(50, y, "SALDO A FAVOR DEL CONDUCTOR (PAGAR):")[span_4](end_span)
    c.drawRightString(540, y, money(res))

    y -= 35
    # --- CUADRO DE BALANCE FINAL ---
    c.setLineWidth(1)
    c.roundRect(50, y-40, 500, 60, 5, stroke=1, fill=0)
    
    c.setFont("Helvetica", 10)
    [span_5](start_span)[span_6](start_span)c.drawString(65, y+5, "Dinero entregado físicamente:")[span_5](end_span)[span_6](end_span)
    c.drawRightString(535, y+5, money(datos['entrega']))
    
    saldo = datos['saldo_final']
    y -= 20
    if saldo > 0:
        c.setFillColorRGB(0, 0.4, 0) # Verde
        c.setFont("Helvetica-Bold", 11)
        [span_7](start_span)c.drawString(65, y, f"RESULTADO: SOBRANTE DE {money(saldo)}")[span_7](end_span)
    elif saldo < 0:
        c.setFillColorRGB(0.7, 0, 0) # Rojo
        c.setFont("Helvetica-Bold", 11)
        [span_8](start_span)c.drawString(65, y, f"RESULTADO: FALTANTE DE {money(saldo)}")[span_8](end_span)
    else:
        c.setFillColorRGB(0, 0, 0.7)
        c.drawString(65, y, "RESULTADO: CUENTAS AL DÍA")

    c.save()
    return file_path
    
