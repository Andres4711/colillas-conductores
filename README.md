# Wheelgrin - Sistema de Liquidación de Conductores

Aplicación web desarrollada en **Python (Flask)** para la gestión y cálculo de colillas de pago de conductores. [span_0](start_span)[span_1](start_span)El sistema permite procesar de forma óptima el balance entre el efectivo producido en el turno y las ganancias del conductor, generando un reporte profesional en PDF[span_0](end_span)[span_1](end_span).

## Características Principales

- **Cálculo Dinámico:** Soporta el ingreso de múltiples valores mediante sumas (ej: `20000+10000`) tanto en el campo de **Efectivo** como en el de **Comisión**.
- **[span_2](start_span)[span_3](start_span)Gestión de Gastos:** Deducción automática de Gasolina (basada en si el conductor vive lejos o cerca) y gastos operativos[span_2](end_span)[span_3](end_span).
- **[span_4](start_span)Liquidación de Extras:** Cálculo automático de horas extra normales y recargos festivos con el factor correspondiente[span_4](end_span).
- **[span_5](start_span)Balance Financiero Inteligente:** - **Saldo a favor Empresa:** Indica el monto que el conductor debe entregar[span_5](end_span).
  - **[span_6](start_span)Saldo a favor Conductor:** Indica el monto que la empresa debe pagar al trabajador[span_6](end_span).
- **[span_7](start_span)Generación de PDF Profesional:** Exportación de colillas con diseño de tabla, efecto cebra y espacios para firmas de soporte[span_7](end_span).
- **Auto-Reset:** El formulario y el estado del servidor se limpian automáticamente tras generar la colilla para agilizar el siguiente registro.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.12
- **Framework Web:** Flask
- **[span_8](start_span)Generación de PDF:** ReportLab (Para diseño de alta fidelidad y tablas)[span_8](end_span).
- **Servidor de Producción:** Gunicorn
- **Despliegue:** Render Cloud Service via GitHub

## Estructura del Proyecto

```text
├── app.py              # Lógica principal y rutas de Flask
├── requirements.txt    # Dependencias del proyecto (Flask, ReportLab, Gunicorn)
├── services/           # Lógica modular del negocio
│   ├── calculos.py     # Motor de cálculos y procesamiento de sumas
│   └── pdf.py          # Generación y diseño estético del reporte PDF
├── static/             # Recursos estáticos (Logo Wheelgrin)
├── templates/          # Archivos HTML
│   └── index.html      # Interfaz de usuario y scripts de limpieza
└── README.md           # Documentación del proyecto
