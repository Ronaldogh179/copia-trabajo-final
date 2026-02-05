````md
# 🚀 SmartTask Organizer

Sistema de gestión de tareas desarrollado en **Python**, que permite organizar, administrar y persistir tareas utilizando una base de datos **SQLite**, aplicando buenas prácticas de ingeniería de software.

---

## ✨ Características

### ✅ Funcionalidades implementadas

- 📝 **Crear tarea**  
  Permite registrar nuevas tareas en el sistema y almacenarlas de forma persistente.

- 📋 **Listar tareas**  
  Visualización de todas las tareas registradas en la base de datos.

- ✏️ **Editar tarea**  
  Modificación de la información de una tarea existente.

- 🗑️ **Eliminar tarea**  
  Eliminación de tareas almacenadas en el sistema.

- ✅ **Marcar tarea como completada**  
  Actualización del estado de la tarea para indicar su finalización.

- 💾 **Persistencia de datos**  
  Todas las tareas se almacenan en una base de datos SQLite, garantizando la conservación de la información entre ejecuciones.

---

## 🎤 Funcionalidades adicionales

- 🎙️ Reconocimiento de voz para interactuar con la aplicación  
- 🗄️ Base de datos SQLite para la persistencia de la información  
- 🧩 Estructura modular del proyecto para facilitar mantenimiento y escalabilidad  
- 💻 Ejecución en consola, adecuada para fines académicos  
- 🔮 Preparado para pruebas y extensiones futuras  

---

## 🛠️ Instalación y ejecución

### 🔹 Requisitos previos

- 🐍 **Python 3.9 o superior**
- 🌱 **Git** (opcional)

---

### 🔹 Paso 1: Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd smarttask-organizer1
````

---

### 🔹 Paso 2: Crear y activar entorno virtual (opcional)

#### 🪟 Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### 🐧 Linux / 🍎 macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

### 🔹 Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 🔹 Paso 4: Ejecutar la aplicación

```bash
python run.py
```

📌 La aplicación utilizará el archivo **`smarttask.db`** como base de datos SQLite para almacenar las tareas.

---

## 📂 Estructura del proyecto

```text
smarttask-organizer1/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── voice.py
├── smarttask.db
├── run.py
├── setup.bat
├── requirements.txt
└── README.md
```

---

## 👥 Integrantes del equipo

* 👨‍💻 **Bendezú Lagos, Jack Joshua**
* 👨‍💻 **Gonzales Jacinto, Simon Ronaldo**
* 👨‍💻 **Julca Laureano, Dickmar Wilber**
* 👨‍💻 **Reyes Cordero, Ítalo Eduardo**

---

## 🎓 Contexto académico

Este proyecto fue desarrollado como parte del curso **Construcción de Software**, con el objetivo de aplicar:

* 📐 Programación orientada a objetos en Python
* 🗄️ Persistencia de datos con SQLite
* 🏗️ Organización de proyectos de software
* 📝 Buenas prácticas de documentación
* 🌍 Control de versiones con Git y GitHub

---

```
```
