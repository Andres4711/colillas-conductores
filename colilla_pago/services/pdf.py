from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_pdf(nombre, cedula, datos):
    file_path = f"Colilla_{nombre}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    def money(valor):
        return f"${abs(valor):,.0f}"

    # Logo y Encabezado
    if os.path.exists("static/logo.png"):
        c.drawImage("static/logo.png", 225, 710, width=150, height=70)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(300, 690, "WHEELGRIN S.A.S.")
    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 675, "NIT: 901216088-9")

    # Título y Fecha
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 640, "COLILLA DE PAGO")
    c.setFont("Helvetica", 9)
    c.drawRightString(550, 750, datetime.now().strftime("%d/%m/%Y %H:%M"))

    y = 600
    # Datos Conductor
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"CONDUCTOR: {nombre.upper()}")
    c.drawString(400, y, f"ID: {cedula}")
    y -= 30

    # Tabla de conceptos
    c.line(50, y+5, 550, y+5)
    c.drawString(50, y, "CONCEPTO")
    c.drawRightString(550, y, "VALOR")
    c.line(50, y-5, 550, y-5)
    y -= 25

    conceptos = [
        ("Efectivo reportado", datos['efectivo']),
        ("Gasolina", -datos['gasolina']),
        ("Gastos operativos", -datos['operativos']),
        ("Comisión ganada", -datos['comision']),
        ("Extras y Recargos", -datos['extras']),
        ("Bonificaciones", -datos['bono']),
    ]

    c.setFont("Helvetica", 11)
    for texto, valor in conceptos:
        c.drawString(50, y, texto)
        c.drawRightString(550, y, money(valor))
        y -= 20

    y -= 10
    c.line(50, y, 550, y)
    y -= 25

    # Lógica de pie de página
    res = datos['resultado']
    c.setFont("Helvetica-Bold", 12)
    if res > 0:
        c.drawString(50, y, "TOTAL A ENTREGAR A EMPRESA:")
        c.drawRightString(550, y, money(res))
    else:
        c.drawString(50, y, "TOTAL A RECIBIR DE EMPRESA:")
        c.drawRightString(550, y, money(res))
    
    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Efectivo entregado físicamente: {money(datos['entrega'])}")
    
    # Saldo final
    y -= 25
    saldo = datos['saldo_final']
    if saldo > 0:
        c.setFillColorRGB(0, 0.5, 0)
        c.drawString(50, y, f"SOBRANTE (A favor conductor): {money(saldo)}")
    elif saldo < 0:
        c.setFillColorRGB(0.8, 0, 0)
        c.drawString(50, y, f"FALTANTE (Debe al administrador): {money(saldo)}")
    
    c.save()
    return file_path
    
