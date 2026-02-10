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
        - Principios: Aislamiento de pruebas (Clean Slate) y Atomicidad.
        - Recursos: Framework 'unittest' de Python, Motor SQLite en memoria (:memory:).
        - Procedimiento: Setup (Configuración) -> Ejecución -> Validación (Assert) -> Teardown (Limpieza).
    
    8.2 Análisis de Resultados:
        - Clasificación: Se separan pruebas Positivas (Flujo ideal) y Negativas (Control de errores).
        - Validación: Uso de aserciones estrictas (AssertEqual, AssertIsNone) para confirmar resultados.
    =================================================================
    """

    def setUp(self):
        """Procedimiento: Configuración inicial antes de cada prueba (Clean Slate)."""
        # Usamos :memory: para crear una BD volátil aislada para cada test
        self.db = Database(':memory:')
        self.session = self.db.get_session()
        self.engine = self.db.engine

    def tearDown(self):
        """Procedimiento: Limpieza de recursos después de cada prueba."""
        self.session.close()
        Base.metadata.drop_all(self.engine)

    # --- EXPERIMENTO 1: Flujo Positivo (Creación) ---
    def test_crear_tarea_exitosamente(self):
        """Valida que el sistema acepta datos correctos y genera persistencia."""
        tarea_id = self.db.crear_tarea("Estudiar Python", "Para el examen", "2026-02-28", "alta")
        
        # Validación de Resultados (8.2)
        self.assertIsNotNone(tarea_id, "El ID de la tarea no debería ser None (Fallo de persistencia)")
        
        # Verificación profunda en BD
        session = self.db.get_session()
        tarea = session.query(Tarea).filter_by(id=tarea_id).first()
        self.assertEqual(tarea.titulo, "Estudiar Python", "El título guardado no coincide con el enviado")
        session.close()

    # --- EXPERIMENTO 2: Flujo Negativo (Restricciones) ---
    def test_impedir_titulo_vacio(self):
        """Valida que el sistema rechaza datos incompletos (Constraint Check)."""
        # Objetivo: Asegurar que el sistema no acepte tareas sin título
        tarea_id = self.db.crear_tarea("", "Descripción sin título")
        
        # Validación: El sistema debe devolver None indicando rechazo
        self.assertIsNone(tarea_id, "El sistema debería haber rechazado un título vacío")

    # --- EXPERIMENTO 3: Ciclo de Vida (Eliminación) ---
    def test_eliminar_tarea(self):
        """Prueba de integridad al eliminar registros."""
        tid = self.db.crear_tarea("Tarea a borrar")
        eliminado = self.db.eliminar_tarea(tid)
        
        self.assertTrue(eliminado, "La función eliminar debería retornar True")
        
        # Validación: Confirmar que ya no existe en la BD
        session = self.db.get_session()
        tarea = session.query(Tarea).filter_by(id=tid).first()
        self.assertIsNone(tarea, "La tarea debería haber desaparecido de la BD tras eliminarla")
        session.close()

    # --- EXPERIMENTO 4: Modificación de Estado ---
    def test_actualizar_tarea(self):
        """Prueba de actualización de campos específicos."""
        # CORRECCIÓN AQUÍ: 'priority' cambiado a 'prioridad'
        tid = self.db.crear_tarea("Viejo Nombre", prioridad="baja")
        
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