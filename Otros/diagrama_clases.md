```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#007bff', 'secondaryColor': '#ff0000', 'tertiaryColor': '#f8f9fa'}}}%%
classDiagram
    direction TD

    %% =========================================
    %% DIAGRAMA DE CLASES - SMARTTASK ORGANIZER
    %% Nivel: Profesional / Ingeniería de Datos
    %% =========================================

    class Categoria["🗂️ Categoria (Catálogo)"] {
        %% Entidad fuerte independiente
        -- Columnas DB --
        +id : Integer <<PK>> <<Auto Increment>>
        +nombre : String(50) <<Unique>> <<Not Null>> <<Index>>
        +descripcion : String(200) <<Nullable>>
        -- ORM --
        #tareas : relationship(List~Tarea~)
    }

    class Tarea["📝 Tarea (Transaccional)"] {
        %% Entidad débil dependiente de Categoria
        -- Columnas DB --
        +id : Integer <<PK>> <<Auto Increment>>
        +titulo : String(100) <<Not Null>> <<Index>>
        +descripcion : Text <<Nullable>>
        +fecha_limite : String(20) <<Nullable>> <<Index>>
        +estado : String(20) <<Default: 'pendiente'>> <<Index>>
        +prioridad : String(20) <<Default: 'media'>> <<Index>>
        +fecha_creacion : DateTime <<Default: Now()>>
        -- Claves Foráneas --
        +categoria_id : Integer <<FK>> <<Nullable>>
        -- ORM --
        #categoria : relationship(Categoria)
    }

    %% --- RELACIONES ---
    %% Cardinalidad: 1 Categoría contiene N Tareas (Relación Uno a Muchos)
    %% La relación es de agregación (una tarea puede existir sin categoría si es NULL)
    Categoria "1" o--|| "0..*" Tarea : "agrupa a"

    %% --- NOTAS TÉCNICAS DE INTEGRIDAD ---
    note for Tarea "🔐 DB Constraints (Reglas de Negocio):\n\n1. CHECK(estado IN ('pendiente', 'completada', 'vencida'))\n2. CHECK(prioridad IN ('baja', 'media', 'alta'))"

    %% --- ESTILOS PERSONALIZADOS (The 'Crack' look) ---
    style Categoria fill:#f1f3f5,stroke:#0d6efd,stroke-width:3px,color:#212529,font-weight:bold
    style Tarea fill:#f1f3f5,stroke:#198754,stroke-width:3px,color:#212529,font-weight:bold
```