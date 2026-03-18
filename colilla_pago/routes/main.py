from flask import Blueprint, render_template, request, send_file
from services.calculos import calcular_valores
from services.pdf import generar_pdf

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    form = {}

    if request.method == "POST":
        form = request.form.to_dict()

        # CALCULAR VALORES (SEGURIDAD YA INCLUIDA)
        resultado = calcular_valores(form)

        # GENERAR PDF
        if "generar_pdf" in request.form:
            pdf = generar_pdf(
                form.get("nombre"),
                form.get("id"),
                resultado
            )
            return send_file(
                pdf,
                download_name=f"Colilla_{form.get('nombre','sin_nombre')}.pdf",
                as_attachment=True
            )

    return render_template("index.html", resultado=resultado, form=form)
