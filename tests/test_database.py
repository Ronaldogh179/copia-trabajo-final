import unittest
import os
import sys

# Ajuste de ruta para importar módulos de la carpeta 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Database, Tarea, Base

class TestSmartTaskDB(unittest.TestCase):
    """
    COMPETENCIA 8: EXPERIMENTACIÓN
    =================================================================
    8.1 Desarrollo de Experimentos:
        - Objetivo: Verificar la integridad transaccional (ACID) y las restricciones de la BD.
        - Principios: Aislamiento de pruebas (cada prueba crea su propia BD en memoria).
        - Recursos: Librería 'unittest' de Python y motor SQLite.
        - Procedimiento: Setup -> Ejecución -> Validación (Assert) -> Teardown.
    
    8.2 Análisis de Resultados:
        - Validación mediante aserciones estrictas (AssertEqual, AssertIsNotNone).
    =================================================================
    """

    def setUp(self):
        """Procedimiento: Configuración inicial antes de cada prueba (Clean Slate)."""
        # Usamos :memory: para no afectar la base de datos real del usuario
        self.db = Database(':memory:')
        self.session = self.db.get_session()
        self.engine = self.db.engine

    def tearDown(self):
        """Procedimiento: Limpieza de recursos después de cada prueba."""
        self.session.close()
        Base.metadata.drop_all(self.engine)

    # --- EXPERIMENTO 1: Creación Exitosa ---
    def test_crear_tarea_exitosamente(self):
        """Prueba que valida la inserción correcta de datos (Positive Test)."""
        tarea_id = self.db.crear_tarea("Estudiar Python", "Para el examen", "2026-02-28", "alta")
        
        # Validación de Resultados
        self.assertIsNotNone(tarea_id, "El ID de la tarea no debería ser None")
        
        # Verificación en BD
        session = self.db.get_session()
        tarea = session.query(Tarea).filter_by(id=tarea_id).first()
        self.assertEqual(tarea.titulo, "Estudiar Python", "El título guardado no coincide")
        session.close()

    # --- EXPERIMENTO 2: Restricciones de Integridad ---
    def test_impedir_titulo_vacio(self):
        """Prueba que valida el rechazo de datos inválidos (Negative Test)."""
        # Objetivo: Asegurar que el sistema no acepte tareas sin título
        tarea_id = self.db.crear_tarea("", "Descripción sin título")
        
        # Validación: El sistema debe devolver None (rechazo)
        self.assertIsNone(tarea_id, "El sistema debería rechazar un título vacío")

    # --- EXPERIMENTO 3: Eliminación de Datos ---
    def test_eliminar_tarea(self):
        """Prueba de ciclo de vida completo (Crear -> Eliminar)."""
        tid = self.db.crear_tarea("Tarea a borrar")
        eliminado = self.db.eliminar_tarea(tid)
        
        self.assertTrue(eliminado, "La función eliminar debería retornar True")
        
        # Validación: Buscar la tarea y confirmar que ya no existe
        session = self.db.get_session()
        tarea = session.query(Tarea).filter_by(id=tid).first()
        self.assertIsNone(tarea, "La tarea debería haber desaparecido de la BD")
        session.close()

    # --- EXPERIMENTO 4: Actualización de Datos ---
    def test_actualizar_tarea(self):
        """Prueba de modificación de estado y persistencia."""
        tid = self.db.crear_tarea("Viejo Nombre", priority="baja")
        
        # Acción: Cambiar datos
        self.db.actualizar_tarea(tid, titulo="Nuevo Nombre", prioridad="alta")
        
        # Validación de Resultados Actualizados
        session = self.db.get_session()
        t = session.query(Tarea).filter_by(id=tid).first()
        self.assertEqual(t.titulo, "Nuevo Nombre")
        self.assertEqual(t.prioridad, "alta")
        session.close()

if __name__ == '__main__':
    unittest.main()