import sqlite3

DATABASE_NAME = "farmacia.db"

def get_db_connection():
    """Establece la conexión con la base de datos y activa llaves foráneas."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Permite buscar los datos por su nombre de columna
    conn.row_factory = sqlite3.Row
    # Activa el control estricto de las relaciones entre tablas
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Crea las tablas necesarias si no existen en el archivo."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Tabla de Pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE,
            telefono TEXT,
            fecha_nacimiento DATE NOT NULL
        )
    ''')

    # 2. Tabla de Medicamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            laboratorio TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            precio REAL NOT NULL DEFAULT 0.0
        )
    ''')

    # 3. Tabla de Consultas Médicas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            fecha DATE NOT NULL,
            diagnostico TEXT NOT NULL,
            tratamiento TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("¡Base de datos y tablas inicializadas correctamente!")

if __name__ == "__main__":
    init_db()