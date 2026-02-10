classDiagram
    %% Diagrama de Clases del Proyecto SmartTask Organizer
    %% Generado para la documentación técnica

    class Categoria {
        +Integer id (PK)
        +String nombre
        +String descripcion
        --
        +tareas: relationship
    }

    class Tarea {
        +Integer id (PK)
        +String titulo
        +String descripcion
        +String fecha_limite
        +String estado
        +String prioridad
        +DateTime fecha_creacion
        +Integer categoria_id (FK)
        --
        +categoria: relationship
    }

    %% Relación: Una Categoría tiene muchas Tareas (1 a N)
    Categoria "1" --> "0..*" Tarea : contiene
    
    note for Tarea "Constraints:\n- estado IN ('pendiente', 'completada', 'vencida')\n- prioridad IN ('baja', 'media', 'alta')"