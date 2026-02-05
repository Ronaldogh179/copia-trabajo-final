"""
SmartTask Organizer - Aplicación principal
Versión CORREGIDA para Visual Studio Code
"""
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
except ImportError as e:
    print(f"❌ Error importando base de datos: {e}")
    print("Intentando importar directamente...")
    # Intentar importación relativa
    from database import db

# Importar módulo de voz con manejo de errores
try:
    from app.voice import voice_assistant
    print("✅ Módulo de voz importado")
except ImportError as e:
    print(f"⚠️  Error importando voz: {e}")
    print("Usando voz simulada...")
    
    # Dummy para desarrollo
    class DummyVoice:
        def __init__(self): 
            self.voice_available = True
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
# DIÁLOGOS (las mismas clases de antes, pero adaptadas)
# ============================================================================

class CrearTareaDialog:
    """HU01 - Crear nueva tarea"""
    def __init__(self, parent, callback=None):
        self.top = tk.Toplevel(parent)
        self.top.title("NUEVA TAREA")
        self.top.geometry("500x500")
        self.top.resizable(False, False)
        
        self.callback = callback
        self.resultado = False
        
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
        
        campos = [
            ("Título *", "entry", ""),
            ("Descripción", "text", ""),
            ("Fecha Límite (DD/MM/AAAA)", "entry", ""),
            ("Prioridad", "combo_pri", "media"),
            ("Categoría", "combo_cat", "")
        ]
        
        self.widgets = {}
        row = 1
        
        for label_text, tipo, valor_default in campos:
            ttk.Label(main_frame, text=label_text).grid(row=row, column=0, 
                                                       padx=(0, 10), pady=5, 
                                                       sticky="w")
            
            if tipo == "entry":
                widget = ttk.Entry(main_frame, width=40)
                widget.grid(row=row, column=1, pady=5, sticky="ew")
                
            elif tipo == "text":
                widget = tk.Text(main_frame, width=40, height=4)
                widget.grid(row=row, column=1, pady=5, sticky="ew")
                
            elif tipo == "combo_pri":
                widget = ttk.Combobox(main_frame, values=["baja", "media", "alta"], 
                                     state="readonly", width=38)
                widget.set(valor_default)
                widget.grid(row=row, column=1, pady=5, sticky="ew")
                
            elif tipo == "combo_cat":
                categorias = db.obtener_categorias()
                valores = ["Seleccionar..."] + [cat['nombre'] for cat in categorias]
                widget = ttk.Combobox(main_frame, values=valores, 
                                     state="readonly", width=38)
                widget.set("Seleccionar...")
                widget.grid(row=row, column=1, pady=5, sticky="ew")
            
            self.widgets[label_text.split()[0].lower()] = widget
            row += 1
        
        main_frame.columnconfigure(1, weight=1)
        
        ttk.Separator(main_frame, orient="horizontal").grid(row=row, column=0, 
                                                           columnspan=2, 
                                                           pady=20, sticky="ew")
        row += 1
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="GUARDAR", width=15,
                  command=self._guardar).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(btn_frame, text="CANCELAR", width=15,
                  command=self.top.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _guardar(self):
        titulo = self.widgets['título'].get().strip()
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio")
            return
        
        descripcion = ""
        if 'descripción' in self.widgets:
            descripcion = self.widgets['descripción'].get("1.0", tk.END).strip()
        
        fecha_text = self.widgets['fecha'].get().strip()
        fecha_sql = None
        if fecha_text:
            try:
                fecha_obj = datetime.strptime(fecha_text, "%d/%m/%Y")
                fecha_sql = fecha_obj.strftime("%Y-%m-%d")
                
                if fecha_obj.date() < date.today():
                    messagebox.showerror("Error", "La fecha límite no puede ser en el pasado")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA")
                return
        
        prioridad = self.widgets['prioridad'].get()
        categoria_nombre = self.widgets['categoría'].get()
        
        categoria_id = None
        if categoria_nombre and categoria_nombre != "Seleccionar...":
            categorias = db.obtener_categorias()
            for cat in categorias:
                if cat['nombre'] == categoria_nombre:
                    categoria_id = cat['id']
                    break
        
        try:
            tarea_id = db.crear_tarea(
                titulo=titulo,
                descripcion=descripcion,
                fecha_limite=fecha_sql,
                prioridad=prioridad,
                categoria_id=categoria_id
            )
            
            self.resultado = True
            if self.callback:
                self.callback()
            
            self.top.destroy()
            messagebox.showinfo("Éxito", "Tarea creada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la tarea:\n{str(e)}")

# (Las clases EditarTareaDialog y EliminarTareaDialog se mantienen igual que antes,
# pero por brevedad las omito. Si las necesitas, dime y te las paso completas)

# ============================================================================
# VENTANA PRINCIPAL
# ============================================================================

class SmartTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartTask Organizer - Gestor de Tareas")
        self.root.geometry("1100x700")
        
        # Variables
        self.filtro_categoria = tk.StringVar(value="TODAS")
        self.modo_voz_activo = False
        
        # Configurar estilos
        self._configurar_estilos()
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Cargar tareas
        self._cargar_tareas()
        
        # Centrar ventana
        self._centrar_ventana()
        
        print("✅ Aplicación inicializada correctamente")
    
    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Accent.TButton', 
                       foreground='white', 
                       background='#007bff')
        style.map('Accent.TButton',
                 background=[('active', '#0069d9')])
        
        style.configure('Success.TButton',
                       foreground='white',
                       background='#28a745')
        style.map('Success.TButton',
                 background=[('active', '#218838')])
        
        style.configure('Danger.TButton',
                       foreground='white',
                       background='#dc3545')
        style.map('Danger.TButton',
                 background=[('active', '#c82333')])
    
    def _centrar_ventana(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabecera
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="SmartTask Organizer", 
                 font=("Arial", 20, "bold")).pack(side=tk.LEFT)
        
        # Botones de acción
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="🎤 VOZ", 
                  command=self._alternar_modo_voz,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=2)
        
        ttk.Button(btn_frame, text="+ NUEVA", 
                  command=self._abrir_crear_tarea,
                  style="Success.TButton").pack(side=tk.LEFT, padx=2)
        
        # Filtros (HU02)
        filtro_frame = ttk.Frame(main_frame)
        filtro_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filtro_frame, text="Filtrar:", 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        categorias = db.obtener_categorias()
        filtros = ["TODAS"] + [cat['nombre'] for cat in categorias]
        
        for filtro in filtros:
            ttk.Radiobutton(filtro_frame, text=filtro, 
                           variable=self.filtro_categoria,
                           value=filtro, 
                           command=self._cargar_tareas).pack(side=tk.LEFT, padx=5)
        
        # Treeview para tareas
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Título", "Descripción", "Fecha Límite", "Estado", "Prioridad", "Categoría")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Configurar columnas
        column_widths = {
            "ID": 50,
            "Título": 200,
            "Descripción": 250,
            "Fecha Límite": 100,
            "Estado": 100,
            "Prioridad": 80,
            "Categoría": 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar expansión
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="📝 Editar", 
                  command=self._editar_tarea).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="🗑️ Eliminar", 
                  command=self._eliminar_tarea,
                  style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="✅ Completar", 
                  command=self._completar_tarea,
                  style="Success.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="🔄 Actualizar", 
                  command=self._cargar_tareas).pack(side=tk.RIGHT, padx=5)
        
        # Estadísticas
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.lbl_stats = ttk.Label(stats_frame, text="Cargando estadísticas...")
        self.lbl_stats.pack(anchor="w")
        
        # Configurar expansión
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def _cargar_tareas(self):
        """HU02 - Listar todas las tareas"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtro = self.filtro_categoria.get()
        if filtro == "TODAS":
            filtro = None
        
        tareas = db.obtener_todas_tareas(filtro)
        
        for tarea in tareas:
            fecha = ""
            if tarea['fecha_limite']:
                try:
                    fecha_obj = datetime.strptime(tarea['fecha_limite'], "%Y-%m-%d")
                    fecha = fecha_obj.strftime("%d/%m/%Y")
                except:
                    fecha = tarea['fecha_limite']
            
            estado = tarea['estado'].upper()
            
            # HU06 - Verificar si está vencida
            if tarea['estado'] == 'pendiente' and tarea['fecha_limite']:
                try:
                    fecha_limite = datetime.strptime(tarea['fecha_limite'], "%Y-%m-%d").date()
                    if fecha_limite < date.today():
                        estado = "VENCIDA"
                        db.actualizar_tarea(tarea['id'], estado='vencida')
                except:
                    pass
            
            item_id = self.tree.insert("", tk.END, values=(
                tarea['id'],
                tarea['titulo'],
                tarea['descripcion'] or "",
                fecha,
                estado,
                tarea['prioridad'].upper(),
                tarea['categoria_nombre'] or "Sin categoría"
            ))
            
            # Colorear
            if estado == "COMPLETADA":
                self.tree.item(item_id, tags=('completada',))
            elif estado == "VENCIDA":
                self.tree.item(item_id, tags=('vencida',))
            elif tarea['prioridad'] == 'alta':
                self.tree.item(item_id, tags=('alta',))
        
        self.tree.tag_configure('completada', background='#d4edda')
        self.tree.tag_configure('vencida', background='#f8d7da')
        self.tree.tag_configure('alta', background='#fff3cd')
        
        self._actualizar_estadisticas()
    
    def _actualizar_estadisticas(self):
        stats = db.obtener_estadisticas()
        texto = f"📊 Total: {stats['total']} | ✅ Completadas: {stats['completadas']} | ⏳ Pendientes: {stats['pendientes']} | ⚠️ Vencidas: {stats['vencidas']}"
        self.lbl_stats.config(text=texto)
    
    def _abrir_crear_tarea(self):
        """HU01 - Crear nueva tarea"""
        dialog = CrearTareaDialog(self.root, self._cargar_tareas)
        self.root.wait_window(dialog.top)
    
    def _editar_tarea(self):
        """HU03 - Editar tarea"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para editar")
            return
        
        item = seleccion[0]
        tarea_id = self.tree.item(item, 'values')[0]
        
        # Para simplificar, mostramos mensaje
        messagebox.showinfo("Editar", f"Editar tarea ID: {tarea_id}\n\nEsta funcionalidad requiere la clase EditarTareaDialog completa.")
    
    def _eliminar_tarea(self):
        """HU04 - Eliminar tarea"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")
            return
        
        item = seleccion[0]
        valores = self.tree.item(item, 'values')
        tarea_id = valores[0]
        titulo = valores[1]
        
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar la tarea:\n\n'{titulo}'?\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            if db.eliminar_tarea(tarea_id):
                self._cargar_tareas()
                messagebox.showinfo("Éxito", "Tarea eliminada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tarea")
    
    def _completar_tarea(self):
        """HU05 - Marcar como completada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para completar")
            return
        
        item = seleccion[0]
        tarea_id = self.tree.item(item, 'values')[0]
        titulo = self.tree.item(item, 'values')[1]
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Marcar '{titulo}' como completada?"
        )
        
        if respuesta:
            if db.marcar_como_completada(tarea_id):
                self._cargar_tareas()
                messagebox.showinfo("Éxito", "Tarea marcada como completada")
            else:
                messagebox.showerror("Error", "No se pudo completar la tarea")
    
    def _alternar_modo_voz(self):
        """Alternar modo voz"""
        if not self.modo_voz_activo:
            self.modo_voz_activo = True
            
            if voice_assistant.iniciar_modo_voz():
                messagebox.showinfo(
                    "Modo Voz", 
                    "Modo voz activado.\n\n"
                    "Instrucciones:\n"
                    "1. Los comandos se ingresan por TECLADO en la terminal\n"
                    "2. La respuesta se escuchará por ALTAVOCES\n"
                    "3. Escribe 'ayuda' para ver comandos\n"
                    "4. Escribe 'salir' para terminar"
                )
                
                # Ejecutar en segundo plano
                thread = threading.Thread(target=self._ejecutar_modo_voz, daemon=True)
                thread.start()
            else:
                self.modo_voz_activo = False
                messagebox.showerror("Error", "No se pudo iniciar el modo voz")
        else:
            self.modo_voz_activo = False
            voice_assistant.detener_modo_voz()
            messagebox.showinfo("Modo Voz", "Modo voz desactivado")
    
    def _ejecutar_modo_voz(self):
        """Ejecutar modo voz en segundo plano"""
        while self.modo_voz_activo:
            try:
                comando = voice_assistant.escuchar(timeout=10)
                
                if comando:
                    if "salir" in comando or "terminar" in comando:
                        self.modo_voz_activo = False
                        voice_assistant.hablar("Saliendo del modo voz")
                        break
                    elif "crear tarea" in comando:
                        voice_assistant.hablar("Para crear una tarea, usa el botón 'NUEVA' en la interfaz")
                    elif "listar tareas" in comando:
                        voice_assistant.hablar(f"Tienes {len(self.tree.get_children())} tareas en la lista")
                    elif "ayuda" in comando:
                        voice_assistant.hablar("Comandos: crear tarea, listar tareas, ayuda, salir")
                    else:
                        voice_assistant.hablar(f"Comando '{comando}' recibido")
            except:
                pass

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

def main():
    """Función principal"""
    try:
        root = tk.Tk()
        app = SmartTaskApp(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    print("="*60)
    print("SMARTTASK ORGANIZER - Iniciando...")
    print("="*60)
    main()