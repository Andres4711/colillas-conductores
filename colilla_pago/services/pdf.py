from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_pdf(nombre, cedula, datos):
    # Nombre del archivo basado en el conductor
    file_path = f"Colilla_{nombre.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    def money(valor):
        # Usamos abs() para que en el desglose no salgan signos negativos feos
        return f"${abs(valor):,.0f}"

    # 1. ENCABEZADO Y LOGO
    if os.path.exists("static/logo.png"):
        c.drawImage("static/logo.png", 225, 710, width=150, height=70)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(300, 690, "WHEELGRIN S.A.S.")
    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 675, "NIT: 901216088-9")

    # 2. TÍTULO Y FECHA
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 645, "COLILLA DE PAGO")
    
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica-Oblique", 9)
    c.drawRightString(550, 750, f"Fecha: {fecha}")

    y = 600
    # 3. DATOS DEL CONDUCTOR (Más limpio)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"CONDUCTOR: {nombre.upper()}")
    c.drawRightString(550, y, f"ID: {cedula}")
    
    y -= 10
    c.setLineWidth(1)
    c.line(50, y, 550, y) # Línea superior de la tabla
    
    y -= 20
    # Encabezados de tabla
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y, "DESCRIPCIÓN DE CONCEPTOS")
    c.drawRightString(540, y, "VALOR")
    
    y -= 10
    c.setLineWidth(0.5)
    c.line(50, y, 550, y) # Línea divisoria sutil
    
    y -= 25

    # 4. LISTADO DE VALORES
    # Nota: Aquí invertimos los signos visualmente para que el usuario entienda el descuento
    conceptos = [
        ("Efectivo reportado (+)", datos['efectivo']),
        ("Gastos de Gasolina (-)", datos['gasolina']),
        ("Gastos Operativos (-)", datos['operativos']),
        ("Comisión devengada (-)", datos['comision']),
        ("Extras y Recargos (-)", datos['extras']),
        ("Bonificaciones (-)", datos['bono']),
    ]

    c.setFont("Helvetica", 11)
    for texto, valor in conceptos:
        c.drawString(60, y, texto)
        c.drawRightString(540, y, money(valor))
        y -= 20

    # 5. RESULTADO DE LIQUIDACIÓN
    y -= 10
    c.setLineWidth(1)
    c.line(50, y, 550, y) # Línea de cierre de tabla
    
    y -= 30
    res = datos['resultado']
    c.setFont("Helvetica-Bold", 13)
    
    if res > 0:
        c.drawString(50, y, "TOTAL A ENTREGAR A EMPRESA:")
        c.drawRightString(550, y, money(res))
    else:
        c.drawString(50, y, "TOTAL A RECIBIR DE EMPRESA:")
        c.drawRightString(550, y, money(res))
    
    # 6. BALANCE DE ENTREGA FÍSICA
    y -= 40
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Efectivo entregado físicamente:")
    c.drawRightString(550, y, money(datos['entrega']))
    
    y -= 25
    saldo = datos['saldo_final']
    c.setFont("Helvetica-Bold", 12)
    
    if saldo > 0:
        c.setFillColorRGB(0, 0.5, 0) # Verde para sobrante
        c.drawString(50, y, "SOBRANTE (A favor del conductor):")
        c.drawRightString(550, y, money(saldo))
    elif saldo < 0:
        c.setFillColorRGB(0.8, 0, 0) # Rojo para faltante
        c.drawString(50, y, "FALTANTE (Debe al administrador):")
        c.drawRightString(550, y, money(saldo))
    else:
        c.setFillColorRGB(0, 0, 0.8) # Azul para cuentas exactas
        c.drawCentredString(300, y, "ESTADO: CUENTAS AL DÍA")

    # Pie de página sutil
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(300, 30, "Este documento es un soporte interno de cuentas de WheelGrin S.A.S.")

    c.save()
    return file_path
    
