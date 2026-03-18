VALOR_GASOLINA = 65000
VALOR_GASOLINA_LEJOS = 70000
VALOR_HORA_EXTRA = 8233

def to_int(valor):
    try:
        # Eliminamos puntos o comas que el usuario pueda escribir por error
        if isinstance(valor, str):
            valor = valor.replace('.', '').replace(',', '')
        return int(valor)
    except (TypeError, ValueError):
        return 0

def calcular_valores(form):
    # Procesar sumas en el campo efectivo (ej: 20000+10000)
    efectivo_str = form.get("efectivo", "0")
    efectivo = sum(to_int(v.strip()) for v in efectivo_str.split("+") if v.strip())

    # Captura de datos
    operativos = to_int(form.get("operativos"))
    comision = to_int(form.get("comision"))
    horas_extra = to_int(form.get("horas_extra"))
    horas_festivo = to_int(form.get("horas_festivo"))
    bono_semanas = to_int(form.get("bono"))
    tanqueos = to_int(form.get("tanqueos"))
    entrega = to_int(form.get("entrega"))
    tipo_carro = form.get("tipo_carro")
    vive_lejos = form.get("vive_lejos")

    # LÓGICA DE GASOLINA
    gasolina = 0
    if tipo_carro != "electrico":
        precio = VALOR_GASOLINA_LEJOS if vive_lejos == "si" else VALOR_GASOLINA
        gasolina = tanqueos * precio

    # LÓGICA DE EXTRAS Y BONOS
    extras_total = int((horas_extra * VALOR_HORA_EXTRA) + (horas_festivo * VALOR_HORA_EXTRA * 1.75))
    bono = bono_semanas * 65000

    # --- EL CÁLCULO CLAVE ---
    # 1. ¿Cuánto quedó de lo que el carro produjo después de gastos?
    sobrante_produccion = efectivo - gasolina - operativos
    
    # 2. ¿Cuánto se ganó el conductor (su sueldo)?
    total_ganado_conductor = comision + extras_total + bono

    # 3. Diferencia: 
    # Positivo: El conductor tiene dinero de la empresa.
    # Negativo: La empresa le debe al conductor.
    resultado_liquidacion = sobrante_produccion - total_ganado_conductor

    return {
        "efectivo": efectivo,
        "extras": extras_total,
        "bono": bono,
        "gasolina": gasolina,
        "operativos": operativos,
        "comision": comision,
        "resultado": resultado_liquidacion,
        "entrega": entrega,
        "saldo_final": entrega - resultado_liquidacion
    }
    
