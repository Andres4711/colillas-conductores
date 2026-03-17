from flask import Flask, render_template, request, send_file, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime
import os

app = Flask(__name__)

VALOR_GASOLINA = 65000
VALOR_GASOLINA_LEJOS = 70000
VALOR_HORA_EXTRA = 8233

EMPRESA = "WHEELGRIN S.A.S."
NIT = "901216088-9"


def calcular_valores(efectivo, operativos, comision, horas_extra, horas_festivo, bono_semanas, tipo_carro, vive_lejos, tanqueos):

    if tipo_carro == "electrico":
        gasolina = 0
    else:
        gasolina = tanqueos * (VALOR_GASOLINA_LEJOS if vive_lejos == "si" else VALOR_GASOLINA)

    extras_normal = horas_extra * VALOR_HORA_EXTRA
    extras_festivo = horas_festivo * (VALOR_HORA_EXTRA * 1.75)

    extras_total = extras_normal + extras_festivo
    bono = bono_semanas * 65000

    sobrante = efectivo - gasolina - operativos
    ganancias = comision + extras_total + bono

    resultado = sobrante - ganancias

    return gasolina, extras_total, bono, resultado


def generar_pdf(nombre, id, efectivo, gasolina, operativos, comision, extras, bono, resultado, entrega, saldo_final):

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    if os.path.exists("logo.png"):
        c.drawImage("logo.png", 30, 660, width=200, height=95)

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

    c.drawString(50, y, f"Efectivo producido: ${efectivo:,.0f}")
    y -= 20

    c.drawString(50, y, f"Gasolina: ${gasolina:,.0f}")
    y -= 20

    c.drawString(50, y, f"Gastos operativos: ${operativos:,.0f}")
    y -= 20

    c.drawString(50, y, f"Comisión: ${comision:,.0f}")
    y -= 20

    c.drawString(50, y, f"Horas extras: ${extras:,.0f}")
    y -= 20

    c.drawString(50, y, f"Bono: ${bono:,.0f}")
    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"RESULTADO FINAL: ${resultado:,.0f}")
    y -= 40

    if resultado >= 0:
        c.drawString(50, y, f"EL CONDUCTOR DEBE ENTREGAR: ${resultado:,.0f}")
    else:
        c.drawString(50, y, f"LA EMPRESA DEBE PAGAR: ${abs(resultado):,.0f}")

    y -= 40

    c.drawString(50, y, f"Entrega conductor: ${entrega:,.0f}")
    y -= 30

    if saldo_final > 0:
        c.drawString(50, y, f"SOBRANTE A FAVOR DEL CONDUCTOR: ${saldo_final:,.0f}")
    elif saldo_final < 0:
        c.drawString(50, y, f"CONDUCTOR QUEDA DEBIENDO: ${abs(saldo_final):,.0f}")
    else:
        c.drawString(50, y, "CONDUCTOR AL DÍA")

    y -= 40

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.save()
    buffer.seek(0)

    return buffer


@app.route("/", methods=["GET", "POST"])
def index():

    resultado_data = None
    form_data = {}

    if request.method == "POST":

        form_data = request.form.to_dict()

        nombre = request.form.get("nombre")
        id = request.form.get("id")

        efectivo_texto = request.form.get("efectivo", "0")
        valores = efectivo_texto.split("+")
        efectivo = sum(float(v.strip() or 0) for v in valores)

        operativos = float(request.form.get("operativos") or 0)
        comision = float(request.form.get("comision") or 0)

        horas_extra = int(request.form.get("horas_extra") or 0)
        horas_festivo = int(request.form.get("horas_festivo") or 0)

        bono_semanas = int(request.form.get("bono") or 0)

        tipo_carro = request.form.get("tipo_carro")
        vive_lejos = request.form.get("vive_lejos")

        tanqueos = int(request.form.get("tanqueos") or 0)
        entrega = float(request.form.get("entrega") or 0)

        gasolina, extras, bono, resultado = calcular_valores(
            efectivo,
            operativos,
            comision,
            horas_extra,
            horas_festivo,
            bono_semanas,
            tipo_carro,
            vive_lejos,
            tanqueos
        )

        saldo_final = entrega - resultado

        resultado_data = {
            "resultado": resultado,
            "entrega": entrega,
            "saldo_final": saldo_final
        }

        # GENERAR PDF DIRECTO
        if "generar_pdf" in request.form:

            pdf = generar_pdf(
                nombre,
                id,
                efectivo,
                gasolina,
                operativos,
                comision,
                extras,
                bono,
                resultado,
                entrega,
                saldo_final
            )

            response = make_response(send_file(
                pdf,
                download_name=f"Colilla_{nombre}.pdf",
                as_attachment=True
            ))

            # LIMPIAR FORM AUTOMÁTICAMENTE
            response.headers["X-Limpiar-Formulario"] = "true"

            return response

    return render_template("index.html", resultado=resultado_data, form=form_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
