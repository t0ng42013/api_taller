# ⚙️ API - Mecánica Integral Alonso

Una API RESTful robusta diseñada para la gestión integral de un taller mecánico. Este sistema centraliza el control de clientes, vehículos, presupuestos dinámicos, control de deudas y stock de repuestos, sirviendo como motor backend para una futura aplicación móvil nativa.

## 🚀 Características Principales

* **Gestión de Vehículos y Clientes:** Registro detallado del historial de cada unidad (kilómetros, trabajos realizados, fechas).
* **Presupuestos Inteligentes:** Cálculo automático de mano de obra sugerida basado en horas de trabajo y un sistema de multiplicadores de dificultad.
* **Control de Cuentas Corrientes:** Sistema de pagos parciales con cálculo automático de deuda pendiente y días de mora.
* **Catálogo Estandarizado:** Semilla de datos (Seed) con más de 25 trabajos de mecánica general pre-cargados con horas y precios base.
* **Control de Stock Interno:** Trazabilidad de repuestos sobrantes compatibles con modelos específicos.
* **Autenticación Segura:** Sistema protegido mediante JSON Web Tokens (JWT) para el acceso exclusivo de los mecánicos.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework:** Django 5.x
* **API:** Django REST Framework (DRF)
* **Autenticación:** Simple JWT
* **Base de Datos:** SQLite (Versión 1)

## 📦 Instalación y Configuración Local

Sigue estos pasos para levantar el entorno de desarrollo en tu computadora:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/t0ng42013/api_taller.git](https://github.com/t0ng42013/api_taller.git)
   cd api_taller
   ```
2. **Crear y activar el entorno virtual::**
   ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate
   ```
3. **Instalar las dependencias::**
   ```bash
    pip install -r requirements.txt
   ```
4. **Aplicar las migraciones de la base de datos:**
   ```bash
    python manage.py migrate
   ```
5. **Cargar el catálogo de trabajos (Seed):**
   ```bash
    python manage.py seed_trabajos
   ```
6. **Crear el usuario administrador (Mecánico):**
   ```bash
    python manage.py createsuperuser
   ``` 
7. **Levantar el servidor local:**
   ```bash
    python manage.py runserver
   ``` 

## 📡 Endpoints Principales
La API cuenta con rutas generadas automáticamente por el Router de DRF, más rutas personalizadas para la lógica de negocio:

POST /api/login/ - Obtención del Token JWT.

GET /api/vehiculos/ - Listado e historial de vehículos.

GET /api/trabajos/ - Órdenes de trabajo ingresadas.

GET /api/trabajos/deudores/ - Endpoint personalizado que retorna exclusivamente clientes con saldo pendiente.

## 📱 Próximos Pasos (Roadmap)
[x] Despliegue de la API v1 en entorno Cloud (PythonAnywhere).

[ ] Desarrollo de aplicación móvil cliente en Kotlin (Android Nativo).

[ ] Integración de Google ML Kit en la app para escaneo y OCR de patentes vehiculares en tiempo real usando CameraX.

Desarrollado para Mecánica Integral Alonso.