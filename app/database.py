import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# --- CONFIGURACIÓN DE SQLALCHEMY ---
Base = declarative_base()
DB_NAME = "smarttask.db"

# 1. DEFINICIÓN DE MODELOS (Nivel Sobresaliente: Relaciones + Índices + Validaciones)


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)
    descripcion = Column(String(200))

    tareas = relationship("Tarea", back_populates="categoria")


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    fecha_limite = Column(String(20), nullable=True, index=True)
    estado = Column(String(20), default="pendiente", index=True)
    prioridad = Column(String(20), default="media", index=True)
    fecha_creacion = Column(DateTime, default=datetime.now)

    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="tareas")

    __table_args__ = (
        CheckConstraint(
            "estado IN ('pendiente', 'completada', 'vencida')",
            name="check_estado_valido",
        ),
        CheckConstraint(
            "prioridad IN ('baja', 'media', 'alta')", name="check_prioridad_valida"
        ),
    )


# --- CLASE GESTORA DE LA BASE DE DATOS ---


class Database:
    def __init__(self, db_name=DB_NAME):
        self.engine = create_engine(f"sqlite:///{db_name}", echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.init_db()

    def init_db(self):
        Base.metadata.create_all(self.engine)
        self._crear_datos_semilla()

    def get_session(self):
        return self.Session()

    def _crear_datos_semilla(self):
        session = self.get_session()
        if session.query(Categoria).count() == 0:
            cats = [
                Categoria(nombre="Trabajo", descripcion="Temas laborales"),
                Categoria(nombre="Personal", descripcion="Cosas mías"),
                Categoria(nombre="Hogar", descripcion="Casa y compras"),
                Categoria(nombre="Estudio", descripcion="Universidad"),
                Categoria(nombre="Salud", descripcion="Médico y deporte"),
                Categoria(nombre="Finanzas", descripcion="Pagos y bancos"),
            ]
            session.add_all(cats)
            session.commit()
        session.close()

    # ===== OPERACIONES CRUD (Backend) =====

    def crear_tarea(
        self,
        titulo,
        descripcion="",
        fecha_limite=None,
        prioridad="media",
        categoria_id=None,
    ):
        # --- VALIDACIÓN NUEVA PARA PASAR LA PRUEBA ---
        if not titulo or titulo.strip() == "":
            print("❌ Validación fallida: El título no puede estar vacío.")
            return None

        session = self.get_session()
        try:
            if not categoria_id:
                cat_def = session.query(Categoria).first()
                if cat_def:
                    categoria_id = cat_def.id

            nueva_tarea = Tarea(
                titulo=titulo,
                descripcion=descripcion,
                fecha_limite=fecha_limite,
                prioridad=prioridad,
                categoria_id=categoria_id,
            )
            session.add(nueva_tarea)
            session.commit()
            return nueva_tarea.id
        except Exception as e:
            session.rollback()
            print(f"Error crítico al crear tarea: {e}")
            return None
        finally:
            session.close()

    def obtener_todas_tareas(self, categoria_filtro=None):
        session = self.get_session()
        try:
            query = session.query(Tarea).join(Categoria)
            if categoria_filtro and categoria_filtro != "TODAS":
                query = query.filter(Categoria.nombre == categoria_filtro)

            resultados = query.all()
            tareas_lista = []
            for t in resultados:
                tarea_dict = {
                    "id": t.id,
                    "titulo": t.titulo,
                    "descripcion": t.descripcion,
                    "fecha_limite": t.fecha_limite,
                    "estado": t.estado,
                    "prioridad": t.prioridad,
                    "categoria_id": t.categoria_id,
                    "categoria_nombre": (
                        t.categoria.nombre if t.categoria else "General"
                    ),
                }
                tareas_lista.append(tarea_dict)
            return tareas_lista
        finally:
            session.close()

    def actualizar_tarea(self, tarea_id, **kwargs):
        session = self.get_session()
        try:
            tarea = session.query(Tarea).filter_by(id=tarea_id).first()
            if tarea:
                for key, value in kwargs.items():
                    if hasattr(tarea, key) and value is not None:
                        setattr(tarea, key, value)
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def eliminar_tarea(self, tarea_id):
        session = self.get_session()
        try:
            tarea = session.query(Tarea).filter_by(id=tarea_id).first()
            if tarea:
                session.delete(tarea)
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def marcar_como_completada(self, tarea_id):
        return self.actualizar_tarea(tarea_id, estado="completada")

    def obtener_categorias(self):
        session = self.get_session()
        try:
            cats = session.query(Categoria).all()
            return [{"id": c.id, "nombre": c.nombre} for c in cats]
        finally:
            session.close()

    def obtener_estadisticas(self):
        session = self.get_session()
        try:
            total = session.query(Tarea).count()
            completadas = session.query(Tarea).filter_by(estado="completada").count()
            pendientes = session.query(Tarea).filter_by(estado="pendiente").count()
            vencidas = session.query(Tarea).filter_by(estado="vencida").count()
            return {
                "total": total,
                "completadas": completadas,
                "pendientes": pendientes,
                "vencidas": vencidas,
            }
        finally:
            session.close()


# Instancia global
db = Database()
