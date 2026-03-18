from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_pdf(nombre, id, datos):
    file_path = "colilla.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    def money(valor):
        return f"${valor:,.0f}"

    if os.path.exists("static/logo.png"):
        c.drawImage("static/logo.png", 225, 710, width=150, height=70)

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(300, 690, "WHEELGRIN S.A.S.")

    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 675, "NIT: 901216088-9")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 650, "COLILLA DE PAGO")

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica", 9)
    c.drawRightString(550, 740, fecha)

    y = 610

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Datos del conductor")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Nombre: {nombre}")
    y -= 15
    c.drawString(50, y, f"ID: {id}")
    y -= 25

    c.line(50, y, 550, y)
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Ingresos")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Efectivo: {money(datos['efectivo'])}")
    y -= 15
    c.drawString(50, y, f"Extras: {money(datos['extras'])}")
    y -= 15
    c.drawString(50, y, f"Bono: {money(datos['bono'])}")
    y -= 25

    c.line(50, y, 550, y)
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Descuentos")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Gasolina: {money(datos['gasolina'])}")
    y -= 15
    c.drawString(50, y, f"Operativos: {money(datos['operativos'])}")
    y -= 15
    c.drawString(50, y, f"Comisión: {money(datos['comision'])}")
    y -= 25

    c.line(50, y, 550, y)
    y -= 25

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"Debe entregar: {money(datos['resultado'])}")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Entregó: {money(datos['entrega'])}")
    y -= 20

    saldo = datos["saldo_final"]

    if saldo > 0:
        c.setFillColorRGB(0, 0.6, 0)
        c.drawString(50, y, f"Sobrante: {money(saldo)}")
    elif saldo < 0:
        c.setFillColorRGB(1, 0, 0)
        c.drawString(50, y, f"Debe: {money(abs(saldo))}")
    else:
        c.setFillColorRGB(0, 0, 1)
        c.drawString(50, y, "Al día")

    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica", 9)
    c.drawRightString(550, 30, "Generado automáticamente")

    c.save()

    return file_path
