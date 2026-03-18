VALOR_GASOLINA = 65000
VALOR_GASOLINA_LEJOS = 70000
VALOR_HORA_EXTRA = 8233

def to_int(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return 0

def calcular_valores(form):

    efectivo_str = form.get("efectivo", "0")

    efectivo = sum(
        to_int(v.strip())
        for v in efectivo_str.split("+")
        if v.strip() != ""
    )

    operativos = to_int(form.get("operativos"))
    comision = to_int(form.get("comision"))
    horas_extra = to_int(form.get("horas_extra"))
    horas_festivo = to_int(form.get("horas_festivo"))
    bono_semanas = to_int(form.get("bono"))
    tanqueos = to_int(form.get("tanqueos"))
    entrega = to_int(form.get("entrega"))

    tipo_carro = form.get("tipo_carro")
    vive_lejos = form.get("vive_lejos")

    # GASOLINA
    if tipo_carro == "electrico":
        gasolina = 0
    else:
        gasolina = tanqueos * (
            VALOR_GASOLINA_LEJOS if vive_lejos == "si" else VALOR_GASOLINA
        )

    # EXTRAS
    extras_normal = horas_extra * VALOR_HORA_EXTRA
    extras_festivo = horas_festivo * (VALOR_HORA_EXTRA * 1.75)
    extras_total = int(extras_normal + extras_festivo)

    # BONO
    bono = bono_semanas * 65000

    # CÁLCULOS
    sobrante = efectivo - gasolina - operativos
    ganancias = comision + extras_total + bono

    resultado = sobrante - ganancias
    saldo_final = entrega - resultado

    return {
        "efectivo": efectivo,
        "extras": extras_total,
        "bono": bono,
        "gasolina": gasolina,
        "operativos": operativos,
        "comision": comision,
        "resultado": resultado,
        "entrega": entrega,
        "saldo_final": saldo_final
    }
