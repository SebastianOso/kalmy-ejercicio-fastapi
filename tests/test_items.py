from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db import Base, get_db  # ← Cambio aquí
from app import app  # ← Cambio aquí
import pytest
import os

# Base de datos para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override de la dependencia de BD
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixture: Limpiar BD antes de cada test
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    
# Limpiar archivo de BD después de todos los tests
def teardown_module(module):
    # CERRAR todas las conexiones antes de borrar
    engine.dispose()
    
    import time
    time.sleep(0.1)
    
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            # Si aún está bloqueado, lo ignoramos
            pass

# ================== TESTS ==================

def test_crear_item():
    """Test: Crear un item correctamente"""
    response = client.post(
        "/items/",
        json={
            "name": "Laptop",
            "description": "Laptop gamer",
            "price": 1500.50,
            "available": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1500.50
    assert data["available"] == True
    assert "id" in data
    assert "created_at" in data

def test_crear_item_sin_campos_requeridos():
    """Test: Error al crear item sin campos requeridos"""
    response = client.post(
        "/items/",
        json={
            "name": "nombre"
        }
    )
    assert response.status_code == 400

def test_crear_item_precio_invalido():
    """Test: Error al crear item con precio negativo"""
    response = client.post(
        "/items/",
        json={
            "name": "Item malo",
            "description": "Descripción",
            "price": -10,
            "available": True
        }
    )
    assert response.status_code == 422  # Validation error de Pydantic

def test_crear_item_nombre_vacio():
    """Test: Error al crear item con nombre vacío"""
    response = client.post(
        "/items/",
        json={
            "name": "",
            "description": "Description",
            "price": 100,
        }
    )
    assert response.status_code == 422

def test_listar_items_vacio():
    """Test: Listar items cuando no hay ninguno"""
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
    assert data["page"] == 1
    assert data["pages"] == 0

def test_listar_items_con_datos():
    """Test: Listar items cuando existen"""
    # Crear 3 items
    for i in range(3):
        client.post(
            "/items/",
            json={
                "name": f"Item {i}",
                "description": f"Description {i}",
                "price": 10.0 + i
            }
        )
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3

def test_paginacion():
    """Test: Paginación funciona correctamente"""
    # Crear 25 items
    for i in range(25):
        client.post(
            "/items/",
            json={
                "name": f"Item {i}",
                "description": f"Description {i}",
                "price": 10.0 + i
            }
        )
    
    # Página 1 (10 items por default)
    response = client.get("/items/?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 25
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["pages"] == 3
    
    # Página 2
    response = client.get("/items/?page=2&size=10")
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 2
    
    # Página 3 (solo 5 items)
    response = client.get("/items/?page=3&size=10")
    data = response.json()
    assert len(data["items"]) == 5

def test_obtener_item_por_id():
    """Test: Obtener un item específico por ID"""
    # Crear item
    create_response = client.post(
        "/items/",
        json={
            "name": "Mouse",
            "description": "Mouse wireless",
            "price": 25.99,
            "available": True
        }
    )
    item_id = create_response.json()["id"]
    
    # Obtener item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Mouse"
    assert data["price"] == 25.99

def test_obtener_item_no_existente():
    """Test: Error 404 al buscar item que no existe"""
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()

def test_actualizar_item():
    """Test: Actualizar un item existente"""
    # Crear item
    create_response = client.post(
        "/items/",
        json={
            "name": "Teclado",
            "description": "Teclado mecánico",
            "price": 100.0,
            "available": True
        }
    )
    item_id = create_response.json()["id"]
    
    # Actualizar precio y disponibilidad
    response = client.put(
        f"/items/{item_id}",
        json={
            "price": 89.99,
            "available": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 89.99
    assert data["available"] == False
    assert data["name"] == "Teclado"  # No cambia
    assert data["description"] == "Teclado mecánico"  # No cambia

def test_actualizar_item_completo():
    """Test: Actualizar todos los campos de un item"""
    # Crear item
    create_response = client.post(
        "/items/",
        json={
            "name": "Original",
            "description": "Description original",
            "price": 50.0,
            "available": True
        }
    )
    item_id = create_response.json()["id"]
    
    # Actualizar todo
    response = client.put(
        f"/items/{item_id}",
        json={
            "name": "Actualizado",
            "description": "Nueva description",
            "price": 75.0,
            "available": False
        }
    )
    data = response.json()
    assert data["name"] == "Actualizado"
    assert data["description"] == "Nueva description"
    assert data["price"] == 75.0
    assert data["available"] == False

def test_actualizar_item_no_existente():
    """Test: Error al actualizar item que no existe"""
    response = client.put(
        "/items/9999",
        json={"price": 100.0}
    )
    assert response.status_code == 404

def test_eliminar_item():
    """Test: Eliminar un item correctamente"""
    # Crear item
    create_response = client.post(
        "/items/",
        json={
            "name": "Monitor",
            "description": "Monitor 144hz",
            "price": 300.0,
            "available": True
        }
    )
    item_id = create_response.json()["id"]
    
    # Eliminar
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    
    # Verificar que ya no existe
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404

def test_eliminar_item_no_existente():
    """Test: Error al eliminar item que no existe"""
    response = client.delete("/items/999999999")
    assert response.status_code == 404