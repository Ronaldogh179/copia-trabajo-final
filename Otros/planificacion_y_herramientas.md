# 📂 Documentación de Gestión y Herramientas
> Evidencia para Competencias 11 (Gestión de Proyectos) y 14 (Herramientas Modernas)

---

## 📅 COMPETENCIA 11: GESTIÓN DE PROYECTOS

### 11.1 Diseño del Proyecto (Propuesta Preliminar)
**Necesidad Identificada:**
Los estudiantes universitarios enfrentan dificultades para organizar tareas académicas dispersas, lo que ocasiona entregas tardías y estrés.
**Propuesta de Solución:**
Desarrollar "SmartTask Organizer", una aplicación de escritorio ligera, sin dependencia de internet, que permita gestión CRUD (Crear, Leer, Actualizar, Eliminar) de tareas con persistencia local segura.

### 11.2 Planificación de la Gestión (Categorización de Recursos)
Para llevar a cabo las actividades identificadas, se han categorizado los siguientes recursos:

| Categoría | Recurso | Justificación |
| :--- | :--- | :--- |
| **Humano** | 4 Desarrolladores | Equipo necesario para dividir backend, frontend, testing y documentación. |
| **Hardware** | Laptops (i5/i7, 8GB RAM) | Equipos estándar para desarrollo y compilación de Python. |
| **Software** | VS Code, Git, SQLite | Herramientas de código abierto (Open Source) para minimizar costos. |
| **Tiempo** | 4 Semanas | Sprints semanales: Diseño -> Desarrollo -> Testing -> Despliegue. |

### 11.3 Ejecución del Proyecto (Coordinación de Equipos)
Se establecieron responsabilidades claras para cumplir las actividades planeadas:

* **Gonzales Jacinto, Simon (Team Lead & Backend):** Arquitectura de Base de Datos, lógica CRUD y coordinación general.
* **Bendezú Lagos, Jack (Frontend):** Diseño de interfaz y experiencia de usuario (UX).
* **Julca Laureano, Dickmar (QA & Testing):** Ejecución de pruebas unitarias y validación de errores.
* **Reyes Cordero, Ítalo (Docs):** Documentación técnica, manual de usuario y diagramas.

---

## 🛠️ COMPETENCIA 14: USO DE HERRAMIENTAS MODERNAS

### 14.1 Uso de Técnicas y Metodologías (Comparativa)
Se compararon metodologías apropiadas para la solución del problema:

| Metodología | ¿Por qué se eligió? | ¿Qué se descartó? |
| :--- | :--- | :--- |
| **MVC (Modelo-Vista-Controlador)** | **Elegida.** Permite separar la lógica de la base de datos de la interfaz gráfica, facilitando el mantenimiento y las pruebas unitarias. | **Monolítica:** Se descartó porque mezcla código, haciendo difícil la depuración en equipo. |
| **TDD (Test Driven Development)** | **Elegida.** Escribir pruebas antes/durante el código asegura que la BD sea robusta desde el inicio. | **Code & Fix:** Se descartó programar "a la rápida" porque genera deuda técnica y bugs difíciles de rastrear. |

### 14.2 Uso de Herramientas (Comparativa Técnica)
Se identificaron y compararon herramientas apropiadas:

* **Lenguaje: Python vs Java**
    * *Selección:* **Python**.
    * *Razón:* Mayor velocidad de desarrollo, sintaxis limpia y librerías potentes para SQL (SQLAlchemy) en comparación con la verbosidad de Java.
* **Base de Datos: SQLite vs MySQL**
    * *Selección:* **SQLite**.
    * *Razón:* Serverless (no requiere instalar un servidor aparte), ideal para una app de escritorio portable. MySQL consumía demasiados recursos para este alcance.
* **Control de Versiones: Git/GitHub**
    * *Selección:* **Git Flow**.
    * *Razón:* Permite trabajo colaborativo mediante ramas (`feature/`, `main`), evitando conflictos de código entre los 4 integrantes.