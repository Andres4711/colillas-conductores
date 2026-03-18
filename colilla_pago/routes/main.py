from flask import Blueprint, render_template, request, send_file
from services.calculos import calcular_valores
from services.pdf import generar_pdf

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html", resultado=None, form={})

    form_data = request.form.to_dict()

    nombre = request.form.get("nombre")
    id = request.form.get("id")

    efectivo = sum(float(v.strip() or 0) for v in request.form.get("efectivo", "0").split("+") if v.strip() != "")

    operativos = float(request.form.get("operativos") or 0)
    comision = float(request.form.get("comision") or 0)

    horas_extra = int(request.form.get("horas_extra") or 0)
    horas_festivo = int(request.form.get("horas_festivo") or 0)

    bono = int(request.form.get("bono") or 0)

    tipo_carro = request.form.get("tipo_carro")
    vive_lejos = request.form.get("vive_lejos")
    tanqueos = int(request.form.get("tanqueos") or 0)

    entrega = float(request.form.get("entrega") or 0)

    gasolina, extras, bono, resultado = calcular_valores(
        efectivo, operativos, comision,
        horas_extra, horas_festivo,
        bono, tipo_carro, vive_lejos, tanqueos
    )

    saldo_final = entrega - resultado

    if "generar_pdf" in request.form:
        pdf = generar_pdf(
            nombre, id, efectivo, gasolina, operativos,
            comision, extras, bono, resultado, entrega, saldo_final
        )

        return send_file(pdf, download_name=f"Colilla_{nombre}.pdf", as_attachment=True)

    return render_template("index.html", resultado={
        "resultado": resultado,
        "entrega": entrega,
        "saldo_final": saldo_final
    }, form=form_data)
