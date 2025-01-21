# Khipu Tools

## Proyecto en Desarrollo

Este proyecto está en desarrollo activo. Las funcionalidades y API pueden cambiar sin previo aviso.

![PyPI - Status](https://img.shields.io/pypi/status/khipu-tools)
[![Tests&Coverage](https://github.com/mariofix/khipu-tools/actions/workflows/tests_coverage.yml/badge.svg?branch=main)](https://github.com/mariofix/khipu-tools/actions/workflows/tests_coverage.yml)
[![Downloads](https://pepy.tech/badge/khipu-tools)](https://pepy.tech/project/khipu-tools)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7f6ca2bad320445f954862dc119091aa)](https://app.codacy.com/gh/mariofix/khipu-tools/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/7f6ca2bad320445f954862dc119091aa)](https://app.codacy.com/gh/mariofix/khipu-tools/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mariofix/khipu-tools/main.svg)](https://results.pre-commit.ci/latest/github/mariofix/khipu-tools/main)
![PyPI](https://img.shields.io/pypi/v/khipu-tools)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/khipu-tools)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/khipu-tools)
![PyPI - License](https://img.shields.io/pypi/l/khipu-tools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Descripción

Khipu Tools es una librería en Python pensada para que integrar los servicios de Khipu en tus proyectos sea sencillo y directo. Ideal para gestionar transacciones y pagos desde tu código.

## Características

- **Conexión directa con la API de Khipu**: Compatible con la versión 3 en adelante de la API.
- **Pagos instantáneos**: Basado en [fixmycode/pykhipu](https://github.com/fixmycode/pykhipu).
- **Pagos automáticos**: Simplifica transacciones recurrentes.
- **Diseño amigable**: Fácil de usar y ligero.
- **Manejo de errores**: Robusto y preparado para entornos reales.

## Instalación

Puedes instalar Khipu Tools desde PyPI:

```bash
pip install khipu-tools
```

## Requisitos Previos

- **Python 3.9 o superior**.
- **Credenciales de Khipu**: Necesitarás tu `API Key` proporcionada por Khipu.

## Uso Básico

Ejemplo de cómo crear un pago utilizando Khipu Tools:

```python
import khipu_tools

# Configura tu API Key de Khipu
khipu_tools.api_key = "tu-api-key"

# Crear un pago
pago = khipu_tools.Payments.create(
    amount=5000,
    currency="CLP",
    subject="Pago de Prueba"
)

print(pago)
```

Salida esperada:

```json
{
  "payment_id": "gqzdy6chjne9",
  "payment_url": "https://khipu.com/payment/info/gqzdy6chjne9",
  "simplified_transfer_url": "https://app.khipu.com/payment/simplified/gqzdy6chjne9",
  "transfer_url": "https://khipu.com/payment/manual/gqzdy6chjne9",
  "app_url": "khipu:///pos/gqzdy6chjne9",
  "ready_for_terminal": false
}
```

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama con un nombre descriptivo para tu cambio.
3. Envía un Pull Request describiendo los cambios.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).
Este proyecto no está patrocinado ni asociado con Khipu.
