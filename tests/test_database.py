import unittest
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- TRUCO PARA IMPORTAR LA APP DESDE LA CARPETA TESTS ---
# Esto le dice a Python: "Busca la carpeta 'app' un nivel más arriba"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos tu código real
from app.database import Database, Base, Tarea, Categoria

class TestSmartTaskDB(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta AUTOMÁTICAMENTE antes de cada prueba"""
        # 1. Usamos una base de datos en memoria (RAM) para no tocar tu archivo real
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=self.engine)
        
        # 2. Conectamos tu clase Database a esta memoria temporal
        self.db = Database(db_name=":memory:") 
        self.db.engine = self.engine
        self.db.Session = self.Session
        
        # 3. Creamos las tablas vacías
        Base.metadata.create_all(self.engine)
        
        # 4. Creamos una categoría obligatoria para las pruebas
        session = self.db.get_session()
        cat = Categoria(nombre="General", descripcion="Categoría de prueba")
        session.add(cat)
        session.commit()
        self.cat_id = cat.id
        session.close()

    def tearDown(self):
        """Se ejecuta al final de cada prueba: Limpia todo"""
        Base.metadata.drop_all(self.engine)

    # --- PRUEBA 1: CREAR ---
    def test_crear_tarea_exitosamente(self):
        """Prueba que se crea una tarea correctamente"""
        tarea_id = self.db.crear_tarea("Estudiar Python", "Para el examen", "2024-12-31", "alta", self.cat_id)
        
        # Verificamos que nos devuelva un ID (significa que se creó)
        self.assertIsNotNone(tarea_id)
        
        # Verificamos que los datos estén en la base de datos
        session = self.db.get_session()
        tarea = session.query(Tarea).filter_by(id=tarea_id).first()
        self.assertEqual(tarea.titulo, "Estudiar Python")
        session.close()

    # --- PRUEBA 2: VALIDACIÓN (El punto Sobresaliente) ---
    def test_impedir_titulo_vacio(self):
        """Prueba que NO deja crear tareas sin título (Constraint)"""
        # Intentamos crear una tarea con título vacío ""
        tarea_id = self.db.crear_tarea("", "Descripción", "2024-12-31")
        
        # Esperamos que falle y devuelva None (porque tu código captura el error)
        self.assertIsNone(tarea_id)

    # --- PRUEBA 3: ELIMINAR ---
    def test_eliminar_tarea(self):
        """Prueba que borra correctamente"""
        # Primero creamos una
        tid = self.db.crear_tarea("Borrarme", "", None, "media", self.cat_id)
        
        # Luego la borramos
        resultado = self.db.eliminar_tarea(tid)
        self.assertTrue(resultado)
        
        # Verificamos que ya no exista
        session = self.db.get_session()
        cuenta = session.query(Tarea).filter_by(id=tid).count()
        self.assertEqual(cuenta, 0)
        session.close()

    # --- PRUEBA 4: ACTUALIZAR ---
    def test_actualizar_tarea(self):
        """Prueba que edita correctamente"""
        tid = self.db.crear_tarea("Viejo Nombre", "", None, "baja", self.cat_id)
        
        # Cambiamos el nombre y prioridad
        self.db.actualizar_tarea(tid, titulo="Nuevo Nombre", prioridad="alta")
        
        # Verificamos cambios
        session = self.db.get_session()
        t = session.query(Tarea).filter_by(id=tid).first()
        self.assertEqual(t.titulo, "Nuevo Nombre")
        self.assertEqual(t.prioridad, "alta")
        session.close()

if __name__ == '__main__':
    unittest.main()