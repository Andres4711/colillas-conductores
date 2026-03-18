from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_pdf(nombre, id, datos):
    file_path = "colilla.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    # ===== LOGO CENTRADO =====
    if os.path.exists("static/logo.png"):
        c.drawImage("static/logo.png", 225, 710, width=150, height=70)

    # ===== EMPRESA =====
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(300, 690, "WHEELGRIN S.A.S.")

    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 675, "NIT: 901216088-9")

    # ===== TÍTULO =====
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 650, "COLILLA DE PAGO")

    # ===== FECHA =====
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica", 9)
    c.drawRightString(550, 740, fecha)

    y = 610

    # ===== DATOS DEL CONDUCTOR =====
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

    # ===== INGRESOS =====
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Ingresos")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Efectivo: ${datos['efectivo']}")
    y -= 15
    c.drawString(50, y, f"Extras: ${datos['extras']}")
    y -= 15
    c.drawString(50, y, f"Bono: ${datos['bono']}")
    y -= 25

    c.line(50, y, 550, y)
    y -= 20

    # ===== DESCUENTOS =====
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Descuentos")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Gasolina: ${datos['gasolina']}")
    y -= 15
    c.drawString(50, y, f"Operativos: ${datos['operativos']}")
    y -= 15
    c.drawString(50, y, f"Comisión: ${datos['comision']}")
    y -= 25

    c.line(50, y, 550, y)
    y -= 25

    # ===== RESULTADO FINAL =====
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"Debe entregar: ${datos['resultado']}")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Entregó: ${datos['entrega']}")
    y -= 20

    saldo = datos["saldo_final"]

    if saldo > 0:
        c.setFillColorRGB(0, 0.6, 0)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, f"Sobrante: ${saldo}")
    elif saldo < 0:
        c.setFillColorRGB(1, 0, 0)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, f"Debe: ${abs(saldo)}")
    else:
        c.setFillColorRGB(0, 0, 1)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, "Al día")

    # Reset color
    c.setFillColorRGB(0, 0, 0)

    # ===== FOOTER =====
    c.setFont("Helvetica", 9)
    c.drawRightString(550, 30, "Generado automáticamente")

    c.save()

    return file_path
