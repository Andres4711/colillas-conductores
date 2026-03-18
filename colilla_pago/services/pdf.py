from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime
import os

EMPRESA = "WHEELGRIN S.A.S."
NIT = "901216088-9"

def generar_pdf(nombre, id, efectivo, gasolina, operativos, comision, extras, bono, resultado, entrega, saldo_final):

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    if os.path.exists("static/logo.png"):
        c.drawImage("static/logo.png", 30, 660, width=200, height=95)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, EMPRESA)
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(200, y, f"NIT: {NIT}")
    y -= 40

    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, y, "COLILLA DE PAGO")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Conductor: {nombre}")
    y -= 20
    c.drawString(50, y, f"ID: {id}")
    y -= 40

    c.drawString(50, y, f"Efectivo: ${efectivo:,.0f}")
    y -= 20
    c.drawString(50, y, f"Gasolina: ${gasolina:,.0f}")
    y -= 20
    c.drawString(50, y, f"Operativos: ${operativos:,.0f}")
    y -= 20
    c.drawString(50, y, f"Comisión: ${comision:,.0f}")
    y -= 20
    c.drawString(50, y, f"Extras: ${extras:,.0f}")
    y -= 20
    c.drawString(50, y, f"Bono: ${bono:,.0f}")
    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Resultado: ${resultado:,.0f}")
    y -= 40

    c.drawString(50, y, f"Entrega: ${entrega:,.0f}")
    y -= 20

    if saldo_final > 0:
        c.drawString(50, y, f"Sobrante: ${saldo_final:,.0f}")
    elif saldo_final < 0:
        c.drawString(50, y, f"Debe: ${abs(saldo_final):,.0f}")
    else:
        c.drawString(50, y, "Al día")

    y -= 40
    c.drawString(50, y, datetime.now().strftime('%d/%m/%Y %H:%M'))

    c.save()
    buffer.seek(0)

    return buffer
