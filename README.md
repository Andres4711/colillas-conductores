# Wheelgrin - Sistema de Liquidación de Conductores

Aplicación web desarrollada en **Python (Flask)** para la gestión y cálculo de colillas de pago de conductores. El sistema permite procesar de forma óptima el balance entre el efectivo producido en el turno y las ganancias del conductor, generando un reporte profesional en PDF.

## Características Principales

- **Cálculo Dinámico:** Soporta el ingreso de múltiples valores mediante sumas (ej: `20000+10000`) tanto en el campo de **Efectivo** como en el de **Comisión**.
- **Gestión de Gastos:** Deducción automática de Gasolina (basada en si el conductor vive lejos o cerca) y gastos operativos.
- **Liquidación de Extras:** Cálculo automático de horas extra normales y recargos festivos con el factor correspondiente.
- **Balance Financiero Inteligente:** - **Saldo a favor Empresa:** Indica el monto que el conductor debe entregar.
  - **Saldo a favor Conductor:** Indica el monto que la empresa debe pagar al trabajador.
- **Generación de PDF Profesional:** Exportación de colillas con diseño de tabla, efecto cebra y espacios para firmas de soporte.
- **Auto-Reset:** El formulario y el estado del servidor se limpian automáticamente tras generar la colilla para agilizar el siguiente registro.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.12
- **Framework Web:** Flask
- **Generación de PDF:** ReportLab (Para diseño de alta fidelidad y tablas).
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
