VALOR_GASOLINA = 65000
VALOR_GASOLINA_LEJOS = 70000
VALOR_HORA_EXTRA = 8233

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
