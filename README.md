# Wheelgrin - Sistema de Liquidación de Conductores

Aplicación web desarrollada en **Python (Flask)** para la gestión y cálculo de colillas de pago de conductores. El sistema permite procesar de forma óptima el balance entre el efectivo producido en el turno y las ganancias del conductor, generando un reporte profesional en PDF.

## Características Principales

- **Cálculo Automático:** Optimizado para el ingreso de cantidades (Gasolina, Horas Extras, Bonos) multiplicando automáticamente por los valores vigentes.
- **Lógica de Carros Eléctricos:** Campos con valores predeterminados en cero para una carga limpia.
- **Validación de Bonos:** Restricción de seguridad para el bono semanal (mínimo 0, máximo 4).
- **Balance Financiero:** - **Positivo (+):** El conductor debe entregar dinero a la empresa.
  - **Negativo (-):** La empresa debe pagar al conductor.
- **Generación de PDF:** Exportación inmediata de la colilla de pago con un diseño organizado.
- **Auto-Reset:** El formulario se limpia automáticamente tras generar la colilla para agilizar el siguiente registro.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.12
- **Framework Web:** Flask
- **Generación de PDF:** FPDF
- **Despliegue:** Azure App Service via GitHub Actions

## Estructura del Proyecto

```text
├── app.py              # Lógica principal y rutas de Flask
├── requirements.txt    # Dependencias del proyecto
├── templates/          # Archivos HTML
│   └── index.html      # Interfaz de usuario y diseño
└── README.md           # Documentación del proyecto
