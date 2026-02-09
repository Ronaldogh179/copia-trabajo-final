import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import threading
import sys
import os

# Asegurar que Python encuentra los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar base de datos
try:
    from app.database import db
    print("✅ Base de datos importada")
except ImportError:
    try:
        from database import db
        print("✅ Base de datos importada (relativo)")
    except ImportError as e:
        print(f"❌ Error crítico: {e}")
        sys.exit(1)

# Importar módulo de voz con manejo de errores
try:
    from app.voice import voice_assistant
    print("✅ Módulo de voz importado")
except ImportError:
    # Dummy para desarrollo si falla la voz real
    class DummyVoice:
        def __init__(self):
            self.voice_available = False
            self.is_listening = False

        def hablar(self, texto):
            print(f"🤖 [Simulado]: {texto}")

        def escuchar(self, timeout=5):
            return None

        def iniciar_modo_voz(self):
            print("🎤 Modo voz simulado activado")
            return True

        def detener_modo_voz(self):
            print("🎤 Modo voz desactivado")

    voice_assistant = DummyVoice()


# ============================================================================
# DIÁLOGOS
# ============================================================================

class CrearTareaDialog:
    """HU01 - Crear nueva tarea"""
    def __init__(self, parent, callback=None):
        self.top = tk.Toplevel(parent)
        self.top.title("NUEVA TAREA")
        self.top.geometry("500x550")
        self.top.resizable(False, False)
        self.callback = callback
        self._crear_widgets()
        self._centrar_ventana(parent)

    def _centrar_ventana(self, parent):
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')

    def _crear_widgets(self):
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="NUEVA TAREA",
                  font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2,
                                                   pady=(0, 20), sticky="w")

        self.widgets = {}
        campos = [
            ("Título *", "entry", ""),
            ("Descripción", "text", ""),
            ("Fecha Límite (DD/MM/AAAA)", "entry", ""),
            ("Prioridad", "combo_pri", "media"),
            ("Categoría", "combo_cat", "")
        ]

        row = 1
        for label_text, tipo, valor_default in campos:
            ttk.Label(main_frame, text=label_text).grid(row=row, column=0,
                                                        padx=(0, 10), pady=5, sticky="w")

            if tipo == "entry":
                widget = ttk.Entry(main_frame, width=40)
            elif tipo == "text":
                widget = tk.Text(main_frame, width=40, height=4)
            elif tipo == "combo_pri":
                widget = ttk.Combobox(main_frame, values=["baja", "media", "alta"],
                                      state="readonly", width=38)
                widget.set(valor_default)
            elif tipo == "combo_cat":
                cats = db.obtener_categorias()
                vals = ["Seleccionar..."] + [c['nombre'] for c in cats]
                widget = ttk.Combobox(main_frame, values=vals, state="readonly", width=38)
                widget.set("Seleccionar...")

            widget.grid(row=row, column=1, pady=5, sticky="ew")
            # Guardar referencia usando la primera palabra clave
            key = label_text.split()[0].lower().replace("*", "")
            self.widgets[key] = widget
            row += 1

        ttk.Button(main_frame, text="GUARDAR",
                   command=self._guardar).grid(row=row, column=0, columnspan=2, pady=20)

    def _guardar(self):
        titulo = self.widgets['título'].get().strip()
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio")
            return

        # Obtener valores
        desc = self.widgets['descripción'].get("1.0", tk.END).strip()
        fecha_txt = self.widgets['fecha'].get().strip()
        prioridad = self.widgets['prioridad'].get()
        cat_nom = self.widgets['categoría'].get()

        # Procesar fecha
        fecha_sql = None
        if fecha_txt:
            try:
                dt = datetime.strptime(fecha_txt, "%d/%m/%Y")
                fecha_sql = dt.strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido (DD/MM/AAAA)")
                return

        # Procesar categoría
        cat_id = None
        if cat_nom and cat_nom != "Seleccionar...":
            for c in db.obtener_categorias():
                if c['nombre'] == cat_nom:
                    cat_id = c['id']
                    break

        if db.crear_tarea(titulo, desc, fecha_sql, prioridad, cat_id):
            if self.callback:
                self.callback()
            self.top.destroy()
            messagebox.showinfo("Éxito", "Tarea creada correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar la tarea")


class EditarTareaDialog(CrearTareaDialog):
    """HU03 - Editar tarea existente (Hereda diseño de Crear)"""
    def __init__(self, parent, tarea_id, callback=None):
        self.tarea_id = tarea_id
        # Inicializamos padre pero cambiamos título después
        super().__init__(parent, callback)
        self.top.title(f"EDITAR TAREA #{tarea_id}")
        self._cargar_datos()

    def _cargar_datos(self):
        # Buscar tarea en BD
        # Nota: obtener_todas_tareas devuelve lista de dicts. Buscamos el ID.
        tareas = db.obtener_todas_tareas()
        tarea = next((t for t in tareas if t['id'] == self.tarea_id), None)

        if not tarea:
            messagebox.showerror("Error", "Tarea no encontrada")
            self.top.destroy()
            return

        # Llenar campos
        self.widgets['título'].insert(0, tarea['titulo'])
        self.widgets['descripción'].insert("1.0", tarea['descripcion'] or "")
        
        if tarea['fecha_limite']:
            try:
                f_obj = datetime.strptime(tarea['fecha_limite'], "%Y-%m-%d")
                self.widgets['fecha'].insert(0, f_obj.strftime("%d/%m/%Y"))
            except ValueError:
                pass

        self.widgets['prioridad'].set(tarea['prioridad'])
        
        # Seleccionar categoría actual
        cat_nombre = tarea.get('categoria_nombre')
        if cat_nombre:
            self.widgets['categoría'].set(cat_nombre)

    def _guardar(self):
        # Lógica similar a crear, pero llamando a actualizar
        titulo = self.widgets['título'].get().strip()
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio")
            return

        desc = self.widgets['descripción'].get("1.0", tk.END).strip()
        fecha_txt = self.widgets['fecha'].get().strip()
        prioridad = self.widgets['prioridad'].get()
        cat_nom = self.widgets['categoría'].get()

        fecha_sql = None
        if fecha_txt:
            try:
                dt = datetime.strptime(fecha_txt, "%d/%m/%Y")
                fecha_sql = dt.strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida")
                return

        cat_id = None
        if cat_nom and cat_nom != "Seleccionar...":
            for c in db.obtener_categorias():
                if c['nombre'] == cat_nom:
                    cat_id = c['id']
                    break

        exito = db.actualizar_tarea(
            self.tarea_id,
            titulo=titulo,
            descripcion=desc,
            fecha_limite=fecha_sql,
            prioridad=prioridad,
            categoria_id=cat_id
        )

        if exito:
            if self.callback:
                self.callback()
            self.top.destroy()
            messagebox.showinfo("Éxito", "Tarea actualizada correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar")


# ============================================================================
# APP PRINCIPAL
# ============================================================================

class SmartTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartTask Organizer - Gestor de Tareas")
        self.root.geometry("1100x700")
        
        self.filtro_categoria = tk.StringVar(value="TODAS")
        self.modo_voz_activo = False
        
        self._configurar_estilos()
        self._crear_interfaz()
        self._cargar_tareas()
        self._centrar_ventana()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Accent.TButton', foreground='white', background='#007bff')
        style.map('Accent.TButton', background=[('active', '#0069d9')])
        
        style.configure('Success.TButton', foreground='white', background='#28a745')
        style.map('Success.TButton', background=[('active', '#218838')])
        
        style.configure('Danger.TButton', foreground='white', background='#dc3545')
        style.map('Danger.TButton', background=[('active', '#c82333')])

    def _centrar_ventana(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def _crear_interfaz(self):
        # === Cabecera ===
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header, text="SmartTask Organizer", font=("Arial", 20, "bold")).pack(side=tk.LEFT)
        
        btns = ttk.Frame(header)
        btns.pack(side=tk.RIGHT)
        ttk.Button(btns, text="🎤 VOZ", command=self._alternar_modo_voz,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="+ NUEVA", command=self._abrir_crear,
                   style="Success.TButton").pack(side=tk.LEFT, padx=2)

        # === Filtros ===
        filtro_frame = ttk.Frame(main_frame)
        filtro_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filtro_frame, text="Filtrar: ").pack(side=tk.LEFT)
        
        cats = ["TODAS"] + [c['nombre'] for c in db.obtener_categorias()]
        for c in cats:
            ttk.Radiobutton(filtro_frame, text=c, variable=self.filtro_categoria,
                            value=c, command=self._cargar_tareas).pack(side=tk.LEFT, padx=5)

        # === Lista (Treeview) ===
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        cols = ("ID", "Título", "Descripción", "Fecha Límite", "Estado", "Prioridad", "Categoría")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        
        anchos = [50, 200, 250, 100, 100, 80, 100]
        for col, ancho in zip(cols, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho)
            
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # === Acciones ===
        act_frame = ttk.Frame(main_frame)
        act_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(act_frame, text="📝 Editar", command=self._editar_tarea).pack(side=tk.LEFT, padx=5)
        ttk.Button(act_frame, text="🗑️ Eliminar", command=self._eliminar_tarea,
                   style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(act_frame, text="✅ Completar", command=self._completar_tarea,
                   style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(act_frame, text="🔄 Actualizar", command=self._cargar_tareas).pack(side=tk.RIGHT)

        # === Stats ===
        self.lbl_stats = ttk.Label(main_frame, text="Cargando...")
        self.lbl_stats.pack(anchor="w", pady=5)

    def _cargar_tareas(self):
        # Limpiar
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        filtro = self.filtro_categoria.get()
        if filtro == "TODAS":
            filtro = None
            
        tareas = db.obtener_todas_tareas(filtro)
        
        for t in tareas:
            # Formatear fecha
            fecha = t['fecha_limite']
            if fecha:
                try:
                    fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
                except ValueError:
                    pass
            
            # Verificar vencimiento
            estado = t['estado'].upper()
            if t['estado'] == 'pendiente' and t['fecha_limite']:
                try:
                    limit = datetime.strptime(t['fecha_limite'], "%Y-%m-%d").date()
                    if limit < date.today():
                        estado = "VENCIDA"
                        db.actualizar_tarea(t['id'], estado='vencida')
                except ValueError:
                    pass

            item = self.tree.insert("", tk.END, values=(
                t['id'], t['titulo'], t['descripcion'], fecha,
                estado, t['prioridad'].upper(), t['categoria_nombre']
            ))
            
            # Colores
            if estado == "COMPLETADA":
                self.tree.item(item, tags=('done',))
            elif estado == "VENCIDA":
                self.tree.item(item, tags=('late',))
            elif t['prioridad'] == 'alta':
                self.tree.item(item, tags=('high',))

        self.tree.tag_configure('done', background='#d4edda')
        self.tree.tag_configure('late', background='#f8d7da')
        self.tree.tag_configure('high', background='#fff3cd')
        
        self._actualizar_stats()

    def _actualizar_stats(self):
        s = db.obtener_estadisticas()
        txt = f"📊 Total: {s['total']} | ✅ Completadas: {s['completadas']} | ⏳ Pendientes: {s['pendientes']} | ⚠️ Vencidas: {s['vencidas']}"
        self.lbl_stats.config(text=txt)

    def _abrir_crear(self):
        CrearTareaDialog(self.root, self._cargar_tareas)

    def _editar_tarea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una tarea para editar")
            return
        
        id_tarea = self.tree.item(sel[0], 'values')[0]
        # Aquí usamos la nueva clase que creamos arriba
        EditarTareaDialog(self.root, int(id_tarea), self._cargar_tareas)

    def _eliminar_tarea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una tarea")
            return
            
        id_tarea = self.tree.item(sel[0], 'values')[0]
        titulo = self.tree.item(sel[0], 'values')[1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{titulo}'?"):
            if db.eliminar_tarea(id_tarea):
                self._cargar_tareas()
                messagebox.showinfo("Éxito", "Tarea eliminada")
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    def _completar_tarea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una tarea")
            return
            
        id_tarea = self.tree.item(sel[0], 'values')[0]
        if db.marcar_como_completada(id_tarea):
            self._cargar_tareas()
            messagebox.showinfo("Éxito", "Tarea completada")
        else:
            messagebox.showerror("Error", "No se pudo completar")

    def _alternar_modo_voz(self):
        # Lógica simplificada
        self.modo_voz_activo = not self.modo_voz_activo
        if self.modo_voz_activo:
            messagebox.showinfo("Voz", "Modo voz activado (Simulado).\nUsa la terminal para ver logs.")
            voice_assistant.iniciar_modo_voz()
        else:
            voice_assistant.detener_modo_voz()
            messagebox.showinfo("Voz", "Modo voz desactivado")

def main():
    root = tk.Tk()
    app = SmartTaskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()