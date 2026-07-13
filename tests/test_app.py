import pytest
from app import app

@pytest.fixture
def client():
    """Configura un cliente de pruebas para simular peticiones HTTP a Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_ruta_inicio(client):
    """Verifica que la página de inicio cargue correctamente."""
    response = client.get('/')
    assert response.status_code == 200

def test_ruta_pacientes(client):
    """Verifica que el módulo de pacientes responda con éxito."""
    response = client.get('/pacientes')
    assert response.status_code == 200

def test_ruta_medicamentos(client):
    """Verifica que el módulo de medicamentos responda con éxito."""
    response = client.get('/medicamentos')
    assert response.status_code == 200

def test_ruta_consultas(client):
    """Verifica que el módulo de consultas médicas responda con éxito."""
    response = client.get('/consultas')
    assert response.status_code == 200

# --- NUEVAS PRUEBAS DE FUNCIONALIDAD ---

def test_guardar_paciente_post(client):
    """Prueba el envío del formulario para registrar un paciente (Simula POST)."""
    datos_prueba = {
        'nombre': 'Paciente de Prueba Pytest',
        'dni': '99999999',
        'telefono': '900000000',
        'fecha_nacimiento': '2000-01-01'
    }
    # Enviamos los datos simulando el clic en "Guardar"
    response = client.post('/pacientes/guardar', data=datos_prueba)
    # Debe redireccionar (Código 302) de vuelta a la lista de pacientes
    assert response.status_code == 302

def test_guardar_medicamento_post(client):
    """Prueba el envío del formulario para registrar un medicamento (Simula POST)."""
    datos_prueba = {
        'nombre': 'Medicina de Prueba 500mg',
        'laboratorio': 'Lab Pytest',
        'stock': '50',
        'precio': '4.50'
    }
    response = client.post('/medicamentos/guardar', data=datos_prueba)
    assert response.status_code == 302