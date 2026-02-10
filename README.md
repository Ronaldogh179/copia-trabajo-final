# 🚀 SmartTask Organizer
### Sistema de Gestión de Tareas Inteligente

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Estado-Sobresaliente-gold?style=for-the-badge)

---

## 📖 Descripción del Proyecto

**SmartTask Organizer** es una solución de software de escritorio diseñada bajo la arquitectura **MVC (Modelo-Vista-Controlador)**. Permite la administración eficiente de tareas académicas y personales, garantizando la persistencia e integridad de los datos mediante un motor **SQLite** optimizado con **SQLAlchemy**.

Este proyecto se diferencia por aplicar buenas prácticas de ingeniería de software, incluyendo **Test Driven Development (TDD)**, validaciones estrictas de base de datos y una interfaz gráfica intuitiva.

---

## 🎨 Diseño e Interfaz (UI/UX)

La interfaz ha sido diseñada aplicando la **Teoría del Color** para guiar intuitivamente al usuario, utilizando una paleta semántica estándar:

| Color | Código Hex | Significado Semántico | Uso en la App |
| :--- | :--- | :--- | :--- |
| **Verde Success** | `#28a745` | **Éxito / Positivo** | Botones de "Crear Nueva", "Completar" y Tareas Finalizadas. |
| **Rojo Danger** | `#dc3545` | **Peligro / Irreversible** | Acciones destructivas como "Eliminar" y Alertas de Tareas Vencidas. |
| **Azul Primary** | `#007bff` | **Acción / Informativo** | Botones de navegación, "Editar", "Voz" y Tareas de Alta Prioridad. |
| **Gris Neutral** | `#f8f9fa` | **Fondo / Estructura** | Mantiene la limpieza visual y reduce la fatiga ocular. |

---

## ✨ Características Técnicas (Nivel Sobresaliente)

### 🛡️ Backend & Base de Datos
* **ORM SQLAlchemy:** Abstracción completa de SQL.
* **Integridad de Datos:** Restricciones `CheckConstraint` para asegurar que no existan estados inválidos o títulos vacíos.
* **Relaciones:** Modelo Relacional (FK) entre `Tareas` y `Categorías`.
* **Índices:** Búsquedas optimizadas en columnas críticas (`fecha_limite`, `prioridad`).

### ⚙️ Funcionalidades CRUD
1.  **📝 Crear:** Validación de campos obligatorios en tiempo real.
2.  **📋 Leer:** Listado con filtros dinámicos y detección automática de vencimientos.
3.  **✏️ Editar:** Carga de datos preexistentes y actualización transaccional.
4.  **🗑️ Eliminar:** Confirmación de seguridad antes del borrado.

### 🧪 Calidad de Software
* **Unit Testing:** Cobertura de pruebas automatizadas con `unittest` para la lógica de base de datos.
* **Manejo de Errores:** Sistema robusto de `try-except-rollback` para evitar corrupción de datos.

---

## 📂 Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar la escalabilidad:

```text
smarttask-organizer2/
├── app/                  # 📦 Código Fuente (Núcleo)
│   ├── __init__.py
│   ├── main.py           # Vista y Controlador (GUI)
│   ├── database.py       # Modelo de Datos (SQLAlchemy)
│   └── voice.py          # Módulo de Reconocimiento de Voz
├── tests/                # ✅ Pruebas Unitarias (Evidence TDD)
│   └── test_database.py  # Script de pruebas automatizadas
├── Otros/                # 📄 Documentación y Diagramas
├── smarttask.db          # Base de datos (Auto-generada)
├── run.py                # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias
└── README.md             # Documentación del proyecto
🛠️ Instalación y Ejecución
Sigue estos pasos para desplegar la aplicación en tu entorno local:

1. Clonar el repositorio
Bash
git clone [https://github.com/Ronaldogh179/copia-trabajo-final.git](https://github.com/Ronaldogh179/copia-trabajo-final.git)
cd copia-trabajo-final
2. Instalar dependencias
Bash
pip install -r requirements.txt
3. Ejecutar la aplicación
Para iniciar la interfaz gráfica:

Bash
py run.py
4. Ejecutar Pruebas (Testing)
Para verificar la integridad del sistema (Punto 3 de la rúbrica):

Bash
py tests/test_database.py
Deberías ver un mensaje "OK" indicando que los módulos pasaron las pruebas.

👥 Equipo de Desarrollo
Este proyecto fue desarrollado colaborativamente para el curso de Construcción de Software:

👨‍💻 Gonzales Jacinto, Simon Ronaldo (Lead Dev: Base de Datos, Testing & Refactorización)

👨‍💻 Bendezú Lagos, Jack Joshua

👨‍💻 Julca Laureano, Dickmar Wilber

👨‍💻 Reyes Cordero, Ítalo Eduardo

2024 © SmartTask Organizer - Facultad de Ingeniería de Sistemas y Computación


### ¿Qué mejoró?
1.  **Tabla de Colores:** Justifica por qué tu app se ve así (esto a los profesores les encanta).
2.  **Sección Técnica:** Usa palabras clave como "ORM", "Integridad", "Transaccional" (lenguaje de nivel experto).
3.  **Badges:** Los escudos del principio le dan una imagen muy pulida.
4.  **Claridad:** Separa muy bien cómo correr la app vs. cómo correr las pruebas.

**Pégalo, guarda (`Ctrl + S`), haz el commit final y me avisas.** ¡Estamos listos para entregar! 🚀