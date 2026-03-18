VALOR_GASOLINA = 65000
VALOR_GASOLINA_LEJOS = 70000
VALOR_HORA_EXTRA = 8233

def calcular_valores(form):

    
    efectivo_str = form.get("efectivo", "0")

    efectivo = sum(
        int(v.strip() or 0)
        for v in efectivo_str.split("+")
        if v.strip() != ""
    )

    
    operativos = int(form.get("operativos", 0) or 0)
    comision = int(form.get("comision", 0) or 0)
    horas_extra = int(form.get("horas_extra", 0) or 0)
    horas_festivo = int(form.get("horas_festivo", 0) or 0)
    bono_semanas = int(form.get("bono", 0) or 0)
    tanqueos = int(form.get("tanqueos", 0) or 0)
    entrega = int(form.get("entrega", 0) or 0)

    tipo_carro = form.get("tipo_carro")
    vive_lejos = form.get("vive_lejos")

    
    if tipo_carro == "electrico":
        gasolina = 0
    else:
        gasolina = tanqueos * (
            VALOR_GASOLINA_LEJOS if vive_lejos == "si" else VALOR_GASOLINA
        )

    
    extras_normal = horas_extra * VALOR_HORA_EXTRA
    extras_festivo = horas_festivo * (VALOR_HORA_EXTRA * 1.75)
    extras_total = int(extras_normal + extras_festivo)

    
    bono = bono_semanas * 65000

    
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
