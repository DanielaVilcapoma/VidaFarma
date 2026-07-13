from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db_connection

app = Flask(__name__)

with app.app_context():
    init_db()


@app.route('/')
def index():
    return render_template('index.html')


# --- MÓDULO DE PACIENTES ---

@app.route('/pacientes')
def pacientes():
    conn = get_db_connection()
    lista_pacientes = conn.execute("SELECT * FROM pacientes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('pacientes.html', lista_pacientes=lista_pacientes)


@app.route('/pacientes/guardar', methods=['POST'])
def guardar_paciente():
    nombre = request.form['nombre']
    dni = request.form['dni']
    telefono = request.form['telefono']
    fecha_nacimiento = request.form['fecha_nacimiento']
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO pacientes (nombre, dni, telefono, fecha_nacimiento) VALUES (?, ?, ?, ?)",
            (nombre, dni, telefono, fecha_nacimiento)
        )
        conn.commit()
    except Exception as e:
        print(f"Error al registrar paciente: {e}")
    finally:
        conn.close()
    return redirect(url_for('pacientes'))


# --- MÓDULO DE MEDICAMENTOS ---

@app.route('/medicamentos')
def medicamentos():
    conn = get_db_connection()
    lista_medicamentos = conn.execute("SELECT * FROM medicamentos ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('medicamentos.html', lista_medicamentos=lista_medicamentos)


@app.route('/medicamentos/guardar', methods=['POST'])
def guardar_medicamento():
    nombre = request.form['nombre']
    laboratorio = request.form['laboratorio']
    stock = request.form['stock']
    precio = request.form['precio']
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO medicamentos (nombre, laboratorio, stock, precio) VALUES (?, ?, ?, ?)",
            (nombre, laboratorio, stock, precio)
        )
        conn.commit()
    except Exception as e:
        print(f"Error al registrar medicamento: {e}")
    finally:
        conn.close()
    return redirect(url_for('medicamentos'))


# --- MÓDULO DE CONSULTAS MÉDICAS ---

@app.route('/consultas')
def consultas():
    """Carga la página de consultas enviando tanto la lista de pacientes como el historial de consultas."""
    conn = get_db_connection()
    # Necesitamos la lista de pacientes para llenar el menú desplegable del formulario
    lista_pacientes = conn.execute("SELECT id, nombre, dni FROM pacientes ORDER BY nombre ASC").fetchall()

    # Traemos las consultas uniendo las tablas para jalar el nombre del paciente real
    query_consultas = """
        SELECT consultas.id, consultas.fecha, consultas.diagnostico, consultas.tratamiento, pacientes.nombre AS nombre_paciente
        FROM consultas
        INNER JOIN pacientes ON consultas.paciente_id = pacientes.id
        ORDER BY consultas.id DESC
    """
    lista_consultas = conn.execute(query_consultas).fetchall()
    conn.close()
    return render_template('consultas.html', lista_pacientes=lista_pacientes, lista_consultas=lista_consultas)


@app.route('/consultas/guardar', methods=['POST'])
def guardar_consulta():
    """Inserta una consulta médica vinculada a un paciente específico."""
    paciente_id = request.form['paciente_id']
    fecha = request.form['fecha']
    diagnostico = request.form['diagnostico']
    treatment = request.form['tratamiento']
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO consultas (paciente_id, fecha, diagnostico, tratamiento) VALUES (?, ?, ?, ?)",
            (paciente_id, fecha, diagnostico, treatment)
        )
        conn.commit()
    except Exception as e:
        print(f"Error al registrar consulta: {e}")
    finally:
        conn.close()
    return redirect(url_for('consultas'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)