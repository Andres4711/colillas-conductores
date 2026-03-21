# services/calculos.py

VALOR_GASOLINA = 65000
VALOR_GASOLINA_LEJOS = 70000
VALOR_HORA_EXTRA = 8233

def to_int(valor):
    """
    Limpia el string de puntos o comas y lo convierte a entero.
    Si el valor es inválido, retorna 0.
    """
    try:
        if isinstance(valor, str):
            # Elimina puntos y comas que el usuario pueda ingresar por costumbre
            valor = valor.replace('.', '').replace(',', '')
        return int(valor)
    except (TypeError, ValueError):
        return 0

def calcular_valores(form):
    """
    Procesa los datos del formulario y realiza los cálculos de liquidación.
    Soporta sumas (ej: 20000+10000) en los campos Efectivo y Comisión.
    """
    
    # 1. PROCESAMIENTO DE SUMAS EN EFECTIVO
    efectivo_str = form.get("efectivo", "0")
    efectivo = sum(to_int(v.strip()) for v in efectivo_str.split("+") if v.strip())

    # 2. PROCESAMIENTO DE SUMAS EN COMISIÓN (Nueva condición solicitada)
    comision_str = form.get("comision", "0")
    comision = sum(to_int(v.strip()) for v in comision_str.split("+") if v.strip())

    # 3. CAPTURA DE CAMPOS RESTANTES
    operativos = to_int(form.get("operativos"))
    horas_extra = to_int(form.get("horas_extra"))
    horas_festivo = to_int(form.get("horas_festivo"))
    bono_semanas = to_int(form.get("bono"))
    tanqueos = to_int(form.get("tanqueos"))
    entrega = to_int(form.get("entrega"))
    tipo_carro = form.get("tipo_carro")
    vive_lejos = form.get("vive_lejos")

    # 4. LÓGICA DE GASTOS DE GASOLINA
    gasolina = 0
    if tipo_carro != "electrico":
        # Se asigna el precio según si vive lejos o cerca
        precio = VALOR_GASOLINA_LEJOS if vive_lejos == "si" else VALOR_GASOLINA
        gasolina = tanqueos * precio

    # 5. CÁLCULO DE EXTRAS Y BONIFICACIONES
    # Horas extra normales y festivas (con recargo del 75% adicional)
    extras_total = int((horas_extra * VALOR_HORA_EXTRA) + (horas_festivo * VALOR_HORA_EXTRA * 1.75))
    bono = bono_semanas * 65000

    # 6. CÁLCULO FINAL DE LIQUIDACIÓN
    # Paso A: Lo que quedó de la producción tras gastos operativos y gasolina
    sobrante_produccion = efectivo - gasolina - operativos
    
    # Paso B: Lo que se le debe pagar al conductor (su ganancia)
    total_ganado_conductor = comision + extras_total + bono

    # Paso C: Resultado (Positivo = Conductor entrega a empresa / Negativo = Empresa debe al conductor)
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
    
