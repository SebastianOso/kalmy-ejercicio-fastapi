# API de Items - FastAPI

Una API REST profesional y completamente funcional construida con **FastAPI**, **SQLAlchemy** y **SQLite**. Incluye CRUD completo, paginación, tests automatizados. 

**Documentación interactiva**: [http://localhost:8000/docs](http://localhost:8000/docs) (una vez que esté corriendo)

**Despliegue usando Railway**: [https://kalmy-ejercicio-fastapi-production.up.railway.app/docs](https://kalmy-ejercicio-fastapi-production.up.railway.app/docs)

---

## Index

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Cómo Correr la API](#cómo-correr-la-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Decisiones Tecnológicas](#decisiones-tecnológicas)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Paginación](#paginación)

---

## Características

-  **CRUD Completo**: Create, Read, Update y Delete items
-  **Paginación**: Sistema de paginación con parámetros
-  **Tests Automatizados**: Suite completa de tests con pytest
-  **Base de Datos**: SQLite + SQLAlchemy ORM con 
-  **Documentación Interactiva**: OpenAPI/Swagger UI integrado
-  **Production-Ready**: Configuración para Railway deployment
-  **Validación**: Validación de datos con Pydantic

---

## Requisitos Previos

Asegúrate de tener instalados:

- **Python 3.10+**
- **pip**
- **git**

---

## Instalación

### 1. Clonar el repo

```bash
git clone https://github.com/SebastianOso/kalmy-ejercicio-fastapi.git
cd kalmy-ejercicio-fastapi
```

### 2. Crear un entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- **fastapi** >= 0.115.0 
- **uvicorn** >= 0.32.0 
- **sqlalchemy** >= 2.0.36
- **pydantic** >= 2.10.0 
- **pytest** >= 8.3.0
- **pytest-cov** >= 6.0.0 

---

## Cómo Correr la API

### Opción 1: Desarrollo

```bash
uvicorn app:app --reload
```

- **--reload**: Reinicia el servidor automáticamente cuando cambias el código
- Accede a: [http://localhost:8000](http://localhost:8000)
- Docs interactivos: [http://localhost:8000/docs](http://localhost:8000/docs)

### Opción 2: Producción

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## Estructura del Proyecto

```
kalmy-ejercicio-fastapi/
├── app.py                    # Aplicación principal FastAPI
├── requirements.txt          # Dependencias del proyecto
├── railway.json              # Configuración para Railway
├── README.md                 
├── LICENSE                   # Licencia del proyecto
│
├── config/
│   ├── __init__.py
│   └── db.py                 # Configuración de la base de datos
│
├── models/
│   ├── __init__.py
│   └── item.py               # Modelo SQLAlchemy para Items
│
├── schemas/
│   ├── __init__.py
│   └── item.py               # Schema Pydantic para validación
│
├── routes/
│   ├── __init__.py
│   └── item.py               # Rutas/Endpoints de Items
│
├── tests/
│   ├── __init__.py
│   └── test_items.py         # Tests con pytest
│

```

### Descripción de Módulos

- `app.py` | Inicializa la aplicación FastAPI e incluye los routers
- `config/db.py` | Gestión de la conexión a base de datos y sesiones
- `models/item.py` | Definición del modelo Item con SQLAlchemy
- `schemas/item.py` | Schema de validación con Pydantic
- `routes/item.py` | Endpoints REST (GET, POST, PUT, DELETE)
- `tests/test_items.py` | Suite de tests automatizados 

## Decisiones Tecnológicas

### 1. **SQLAlchemy 2.0+**
   - Se uso un ORM, que es SQLAlchemy, ya que de esta forma puedo seguir trabajando con código de python, en este caso objetos, para crear las tablas con las que se va a estar trabajando, de igual manera en vez de tener que escribir queries de SQL sigo utilizando python y con su correcto uso podemos evitar inyección de SQL
   - También sirve si queremos migrar la base de datos a otra SQL como PostgreSQL simplemente se tienen que cambiar la configuración de la conexión en la base de datos 

### 2. **SQLite**
   - Se opto por usar SQLite en vez de cualquier otra base de datos, por lo simple que es, no se tiene que levantar un servidor para usarla, es un simple archivo
   - Funciona bien para este tipo de ejercicios pero no es recomendada para aplicaciones con tráfico más concurrente

### 3. **Pydantic v2**
   - Se uso un Schema de Pydantic para la serialización de modelos y nos hace la vida más fácil para la validación de request o response

### 4. **Pytest**
   - Se uso el Framework de testing de pytest, ya que es fácil de usar y es utilizado en la industria

### 5. **Railway** (Deployment)
   - Para el despliegue de la API se uso Railway, ya que puedes desplegar tus proyectos sin tener que hacer configuraciones complejas, simplemente escoges tu repo de GitHUb y lo subes
   - A diferencia de AWS en la cual tendrías que configurar varias cosas, como la instalación tanto instalar python, entre otras cosas

---

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

### 1. **Crear un Item** (POST)

```http
POST /items/
Content-Type: application/json

{
  "name": "Laptop",
  "description": "Laptop gamer",
  "price": 1500.50,
  "available": true
}
```

**Respuesta (201 Created)**:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gamer",
  "price": 1500.50,
  "available": true,
  "created_at": "2026-02-15T10:30:00"
}
```

**Validaciones**:
- `name`: Requerido, 1-100 caracteres, no vacío
- `description`: Requerido, 1-300 caracteres, no vacío
- `price`: Requerido, debe ser > 0
- `available`: Opcional, default: true

---

### 2. **Listar Items con Paginación** (GET)

```http
GET /items/?page=1&size=10
```

**Parámetros**:
- `page` (int, opcional): Número de página (default: 1, mín: 1)
- `size` (int, opcional): Items por página (default: 10, rango: 1-100)

**Respuesta (200 OK)**:
```json
{
  "items": [
    {
      "id": 1,
      "name": "Laptop",
      "description": "Laptop gamer",
      "price": 1500.50,
      "available": true,
      "created_at": "2026-02-15T10:30:00"
    }
  ],
  "total": 25,
  "page": 1,
  "size": 10,
  "pages": 3
}
```

---

### 3. **Obtener Item por ID** (GET)

```http
GET /items/1
```

**Respuesta (200 OK)**:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gamer",
  "price": 1500.50,
  "available": true,
  "created_at": "2026-02-15T10:30:00"
}
```

**Errores**:
- `404 Not Found`: Item no existe

---

### 4. **Actualizar Item** (PUT)

```http
PUT /items/1
Content-Type: application/json

{
  "price": 1299.99,
  "available": false
}
```

**Nota**: Solo actualiza los campos proporcionados

**Respuesta (200 OK)**:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gamer",
  "price": 1299.99,
  "available": false,
  "created_at": "2026-02-15T10:30:00"
}
```

---

### 5. **Eliminar Item** (DELETE)

```http
DELETE /items/1
```

**Respuesta**: `204 No Content` (sin body)

**Errores**:
- `404 Not Found`: Item no existe

---

## Testing

### Ejecutar los tests

```bash
pytest tests/ -v
```
### Suite de Tests Incluida

- `test_crear_item` | Crear un item correctamente 
- `test_crear_item_sin_campos_requeridos` | Validar campos requeridos
- `test_crear_item_precio_invalido` | Validar precio > 0
- `test_crear_item_nombre_vacio` | Validar nombre no vacío
- `test_listar_items_vacio` | Listar sin items
- `test_listar_items_con_datos` | Listar con items
- `test_paginacion` | Paginación funciona correctamente
- `test_obtener_item_por_id` | Obtener item por ID
- `test_obtener_item_no_existente` | Error 404
- `test_actualizar_item` | Actualizar item parcialmente
- `test_actualizar_item_completo` | Actualizar todos los campos
- `test_actualizar_item_no_existente` | Error al actualizar item inexistente
- `test_eliminar_item` | Eliminar item |
- `test_eliminar_item_no_existente` | Error al eliminar item inexistente

---

## Paginación

La API implementa un sistema de paginación flexible:

### Cómo funciona

- Cada solicitud GET a `/items/` soporta paginación
- **Parámetro `page`**: Número de página (1-indexed)
- **Parámetro `size`**: Cantidad de items por página (1-100)

### Ejemplos

Obtener página 1 con 10 items:
```bash
GET /items/?page=1&size=10
```

Obtener página 2 con 20 items:
```bash
GET /items/?page=2&size=20
```

### Respuesta incluye

```json
{
  "items": [...],      // Array de items
  "total": 85,         // Total de items en BD
  "page": 1,           // Página actual
  "size": 10,          // Items por página
  "pages": 9           // Total de páginas (calculado)
}
```

### Cálculos automáticos

- **total pages**: `ceil(total_items / size)`
- **offset**: `(page - 1) * size`

---

### Railway Deployment

El proyecto incluye configuración para Railway en `railway.json`:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

---
## Documentación Interactiva

Una vez que la API esté corriendo:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Todos los endpoints están documentados con descripciones y ejemplos.
