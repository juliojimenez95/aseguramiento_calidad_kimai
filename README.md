# 🧪 Automatización de Pruebas - Kimai Time Tracking

Este repositorio contiene los scripts de automatización de pruebas funcionales y la documentación del proceso de Aseguramiento de la Calidad (SQA) para el sistema **Kimai**, desarrollado como parte del **Taller Final**.

## 📄 Documentación del Proyecto

Puedes consultar el informe completo con la estrategia de pruebas, métricas de calidad y análisis de seguridad aquí:

👉 **[Ver Informe Final (PDF)](Informe_Final.pdf)**

---

## 📋 Descripción del Escenario Automatizado

El script principal (`test_kimai_customer.py`) automatiza el flujo crítico de **Creación de un Cliente**. El flujo cubre los siguientes pasos de verificación:

1.  **Login:** Autenticación con credenciales de administrador.
2.  **Validación Post-Login:** Verificación de acceso correcto al Dashboard (validación de URL).
3.  **Navegación:** Interacción con el menú lateral dinámico para llegar al módulo de "Clientes".
4.  **Formulario:** Diligenciamiento automatizado del formulario de creación de nuevo cliente con nombres únicos (UUID).
5.  **Envío y Confirmación:** Guardado del registro y validación del flujo exitoso.

## ⚙️ Pre-requisitos Técnicos

Antes de ejecutar las pruebas, asegúrate de tener instalado y configurado lo siguiente en tu entorno:

1.  **Python 3.x**: [Descargar Python](https://www.python.org/downloads/).
2.  **Mozilla Firefox**: El navegador donde se ejecutarán las pruebas.
3.  **GeckoDriver**: El driver necesario para que Selenium controle Firefox.
    * [Descargar GeckoDriver](https://github.com/mozilla/geckodriver/releases).
    * **Nota:** Asegúrate de agregar la ruta del `geckodriver.exe` a las Variables de Entorno (PATH) de tu sistema operativo.
4.  **Instancia de Kimai Local**:
    * El script espera que Kimai esté corriendo en `http://localhost:8001`.

## 🚀 Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/juliojimenez95/aseguramiento_calidad_kimai.git](https://github.com/juliojimenez95/aseguramiento_calidad_kimai.git)
    cd aseguramiento_calidad_kimai
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install selenium
    ```

3.  **Ejecutar la prueba:**
    ```bash
    python test_kimai_customer.py
    ```

## 🛠️ Configuración

Las constantes principales están definidas al inicio del archivo para facilitar cambios futuros sin tocar la lógica:

```python
# Configuración del entorno
BASE_URL = "http://localhost:8001"

# Credenciales
TEST_USERNAME = "admin@example.com"
TEST_PASSWORD = "TallerCalidad2025"
