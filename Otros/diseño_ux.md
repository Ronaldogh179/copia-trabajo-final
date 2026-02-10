# 🎨 Diseño de Experiencia de Usuario (UX) y Requisitos

---

## 👤 Historia de Usuario (PBI - Product Backlog Item)
**ID:** US-01  
**Título:** Gestión de Tareas Académicas  

**Como** estudiante universitario con alta carga académica,  
**Quiero** registrar, visualizar y organizar mis tareas pendientes en una base de datos local,  
**Para** evitar olvidar entregas importantes y reducir mi estrés durante el semestre.

### ✅ Criterios de Aceptación (ATDD)
1.  **Dado** que el usuario abre la aplicación, **Cuando** ingresa un título y presiona "Agregar", **Entonces** la tarea debe aparecer en la lista inferior inmediatamente.
2.  **Dado** que existe una tarea creada, **Cuando** el usuario intenta crear otra con el título vacío, **Entonces** el sistema debe mostrar un error y no guardar nada.
3.  **Dado** que una tarea ya fue realizada, **Cuando** el usuario hace clic en "Completar", **Entonces** el estado debe cambiar a "Completada" visualmente.

---

## 🖥️ Wireframe (Prototipo de Baja Fidelidad)
Diseño esquemático de la interfaz gráfica implementada en Tkinter.

```text
+---------------------------------------------------------------+
|  SmartTask Organizer v1.0                         [-][O][X]   |
+---------------------------------------------------------------+
|                                                               |
|  [ 📂 Categoria ▼ ]   [ 📅 Fecha Límite ▼ ]                   |
|                                                               |
|  Título:      [___________________________________________]   |
|  Descripción: [___________________________________________]   |
|                                                               |
|  Prioridad:   ( ) Baja   (•) Media   ( ) Alta                 |
|                                                               |
|  +----------------+   +----------------+   +----------------+ |
|  | ➕ Crear Tarea |   | 🎤 Voz (BETA)  |   | 💾 Guardar     | |
|  +----------------+   +----------------+   +----------------+ |
|                                                               |
|  -----------------------------------------------------------  |
|  LISTA DE TAREAS:                                             |
|  -----------------------------------------------------------  |
|  ID | TÍTULO           | FECHA      | ESTADO     | ACCIÓN     |
|  ---|------------------|------------|------------|------------|
|  01 | Examen Python    | 2026-02-28 | Pendiente  | [Editar]   |
|  02 | Ensayo Ética     | 2026-03-05 | Completada | [Borrar]   |
|  03 | Tesis Avance 1   | 2026-03-10 | Alta       | [Editar]   |
|                                                               |
|                                                               |
+---------------------------------------------------------------+