# services/calculos.py

VALOR_GASOLINA = 65000
VALOR_GASOLINA_LEJOS = 70000
VALOR_HORA_EXTRA = 8233

def to_int(valor):
    """Limpia puntos/comas y convierte a entero (para dinero)."""
    try:
        if isinstance(valor, str):
            valor = valor.replace('.', '').replace(',', '')
        return int(valor)
    except (TypeError, ValueError):
        return 0

def to_float(valor):
    """Convierte a decimal (para tanqueos y horas). Soporta punto y coma."""
    try:
        if isinstance(valor, str):
            # Reemplaza coma por punto para que Python lo entienda como decimal
            valor = valor.replace(',', '.')
        return float(valor)
    except (TypeError, ValueError):
        return 0.0

def calcular_valores(form):
    # 1. Procesamiento de sumas (Efectivo y Comisión)
    efectivo_str = form.get("efectivo", "0")
    efectivo = sum(to_int(v.strip()) for v in efectivo_str.split("+") if v.strip())

    comision_str = form.get("comision", "0")
    comision = sum(to_int(v.strip()) for v in comision_str.split("+") if v.strip())

    # 2. Captura de decimales (Horas y Tanqueos)
    horas_extra = to_float(form.get("horas_extra"))
    horas_festivo = to_float(form.get("horas_festivo"))
    tanqueos = to_float(form.get("tanqueos"))

    # 3. Captura de otros valores
    operativos = to_int(form.get("operativos"))
    bono_semanas = to_int(form.get("bono"))
    entrega = to_int(form.get("entrega"))
    tipo_carro = form.get("tipo_carro")
    vive_lejos = form.get("vive_lejos")

    # 4. Lógica de Gasolina
    gasolina = 0
    if tipo_carro != "electrico":
        precio = VALOR_GASOLINA_LEJOS if vive_lejos == "si" else VALOR_GASOLINA
        gasolina = int(tanqueos * precio)

    # 5. Cálculo de Extras y Bonos
    extras_total = int((horas_extra * VALOR_HORA_EXTRA) + (horas_festivo * VALOR_HORA_EXTRA * 1.75))
    bono = bono_semanas * 65000

    # 6. Liquidación Final
    sobrante_produccion = efectivo - gasolina - operativos
    total_ganado_conductor = comision + extras_total + bono
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
    
