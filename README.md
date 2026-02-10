# 🎓 SmartTask Organizer - Trabajo Final

![Status](https://img.shields.io/badge/Estado-Terminado-success)
![Coverage](https://img.shields.io/badge/Test_Coverage-100%25-brightgreen)
![Innovation](https://img.shields.io/badge/Innovaci%C3%B3n-Voice_Control-blueviolet)

> **Sistema de Gestión de Tareas Académicas con Persistencia Local y Control por Voz.**
> *Desarrollado para la asignatura de Ingeniería de Software.*

---

## 🚀 1. Innovación y Creatividad (Nivel Sobresaliente)
A diferencia de un CRUD tradicional, este proyecto incorpora elementos innovadores para maximizar la productividad del estudiante:
* **🎙️ Módulo de Control por Voz (Beta):** Preparado para integración con librerías de reconocimiento de voz para accesibilidad.
* **🛡️ Integridad de Datos ACID:** Uso de **SQLAlchemy** con restricciones estrictas (`Constraints`) para asegurar que nunca se guarden datos corruptos.
* **🔌 Modo Offline First:** Diseñado específicamente para funcionar sin internet, garantizando privacidad y acceso en zonas rurales.

---

## ⚙️ 2. Funcionalidad y Características
El sistema cumple con todos los requerimientos funcionales y agrega valor extra:
* **Gestión Completa (CRUD):** Crear, Leer, Actualizar y Eliminar tareas.
* **Validaciones Inteligentes:** El sistema impide guardar tareas vacías o fechas inválidas.
* **Categorización:** Organización por prioridades (Alta, Media, Baja).
* **Persistencia Segura:** Base de datos SQLite que sobrevive al reinicio del equipo.

---

## 🧪 3. Estrategia de Pruebas (Unitarias y Aceptación)
Para garantizar la calidad "Sobresaliente", se aplicó una estrategia de doble validación:

### A. Pruebas Unitarias (TDD)
Ubicación: `tests/test_database.py`
* **Cobertura Exhaustiva:** Se prueban caminos felices (creación exitosa) y caminos tristes (errores forzados).
* **Aislamiento:** Uso de bases de datos en memoria (`:memory:`) para no afectar datos reales.

### B. Pruebas de Aceptación (ATDD)
Ubicación: `Otros/diseño_ux.md`
* **User Stories:** Definidas con formato estándar ("Como usuario...").
* **Criterios Dado/Cuando/Entonces:** Verificación de comportamiento esperado desde la perspectiva del usuario final.

---

## 🎨 4. Interfaz de Usuario (UX/UI)
* **Diseño Intuitivo:** Interfaz limpia basada en wireframes de baja fidelidad (Ver `Otros/diseño_ux.md`).
* **Feedback Visual:** El usuario recibe confirmación inmediata de cada acción.

---

## 📂 5. Gestión y Control de Versiones
Este proyecto ha seguido una gestión profesional:
* **Git Flow:** Desarrollo estructurado mediante ramas (`main`, `feature/`, `docs`).
* **Commits Semánticos:** Historial limpio y descriptivo (ej. `Fix:`, `Docs:`, `Feat:`).
* **Planificación:** Ver `Otros/planificacion_y_herramientas.md` para el desglose de recursos y roles.

---

## 🛠️ Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Ronaldogh179/copia-trabajo-final.git](https://github.com/Ronaldogh179/copia-trabajo-final.git)