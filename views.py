# Importamos las herramientas necesarias de tkinter
import tkinter as tk
from tkinter import ttk, messagebox
from models import TicketManager  # La clase que gestiona los tickets y el JSON

class Aplicacion(tk.Tk):
    """Ventana principal de DataDesk"""
    def __init__(self):
        super().__init__()  # Inicializa la ventana de Tkinter
        self.title("DataDesk - Gestión de Tickets -")
        self.geometry("900x600")  # Tamaño de la ventana
        self.minsize(800,500) #Minimo de ventana
        self.gestor = TicketManager()  # Crea el gestor que maneja los datos

        # Construye los widgets (botones, campos, etc.)
        self.crear_widgets()
        # Llena la tabla con los tickets que ya existan
        self.cargar_tabla()
        # Actualiza los contadores de total, pendientes y resueltos
        self.actualizar_metricas()
        #Personalizacion theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
    def crear_widgets(self):
        """Crea todos los elementos visuales de la aplicación"""

        # --- Frame del formulario para crear un nuevo ticket ---
        frame_form = tk.LabelFrame(self, text="Nuevo Ticket", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        # Etiqueta y campo para "Usuario"
        tk.Label(frame_form, text="Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.entry_usuario = tk.Entry(frame_form, width=30)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=2)

        # Etiqueta y campo para "Descripción"
        tk.Label(frame_form, text="Descripción:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
        self.entry_desc = tk.Entry(frame_form, width=40)
        self.entry_desc.grid(row=0, column=3, padx=5, pady=2)

        # Etiqueta y lista desplegable para "Categoría"
        tk.Label(frame_form, text="Categoría:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.combo_cat = ttk.Combobox(frame_form, values=["Hardware", "Software", "Redes"], state="readonly", width=28)
        self.combo_cat.grid(row=1, column=1, padx=5, pady=2)
        self.combo_cat.current(0)  # Opción seleccionada por defecto

        # Etiqueta y lista desplegable para "Prioridad"
        tk.Label(frame_form, text="Prioridad:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
        self.varias_prioridades = ttk.Combobox(frame_form, values=["Baja", "Media", "Alta", "Crítica"], state="readonly", width=38)
        self.varias_prioridades.grid(row=1, column=3, padx=5, pady=2)
        self.varias_prioridades.current(1)  # "Media" por defecto
        
        # Botón para crear el ticket
        btn_crear = tk.Button(frame_form, text="✅ Crear Ticket", command=self.crear_ticket, bg="#4CAF50", fg="white")
        btn_crear.grid(row=2, column=0, columnspan=4, pady=10)

        # --- Frame de métricas (contadores) ---
        frame_metricas = tk.Frame(self)
        frame_metricas.pack(fill="x", padx=10, pady=5)

        # Etiqueta que muestra el total de tickets
        self.lbl_total = tk.Label(frame_metricas, text="Total: 0", font=("Segoe UI", 10, "bold"))
        self.lbl_total.pack(side="left", padx=20)

        # Etiqueta que muestra los tickets pendientes
        self.lbl_pendientes = tk.Label(frame_metricas, text="Pendientes: 0", font=("Segoe UI", 10, "bold"), fg="orange")
        self.lbl_pendientes.pack(side="left", padx=20)

        # Etiqueta que muestra los tickets resueltos
        self.lbl_resueltos = tk.Label(frame_metricas, text="Resueltos: 0", font=("Segoe UI", 10, "bold"), fg="green")
        self.lbl_resueltos.pack(side="left", padx=20)

        # --- Frame de búsqueda / filtro ---
        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack(fill="x", padx=10, pady=(0, 5))

        tk.Label(frame_busqueda, text="Filtrar:").pack(side="left", padx=5)
        self.entry_filtro = tk.Entry(frame_busqueda, width=40)
        self.entry_filtro.pack(side="left", padx=5)
        # Cada vez que se suelta una tecla, se ejecuta el método filtrar_tabla
        self.entry_filtro.bind("<KeyRelease>", self.filtrar_tabla)

        # --- Frame de la tabla (Treeview) ---
        frame_tabla = tk.LabelFrame(self, text="Tickets Registrados", padx=10, pady=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        # Definimos las columnas de la tabla
        columnas = ("ID", "Usuario", "Descripción", "Categoría", "Prioridad", "Estado","Fecha")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        # Configuramos cada columna (título y ancho)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        # Barra de desplazamiento vertical para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # --- Frame de acciones (botones para modificar/eliminar) ---
        frame_acciones = tk.Frame(self)
        frame_acciones.pack(fill="x", padx=10, pady=5)

        # Botón para marcar un ticket como "Resuelto"
        btn_resolver = tk.Button(frame_acciones, text="✔️Marcar como Resuelto", command=self.marcar_resuelto, bg="#2196F3", fg="white")
        btn_resolver.pack(side="left", padx=5)

        # Botón para eliminar un ticket seleccionado
        btn_eliminar = tk.Button(frame_acciones, text="🗑️Eliminar Ticket", command=self.eliminar_ticket, bg="#f44336", fg="white")
        btn_eliminar.pack(side="left", padx=5)

    def cargar_tabla(self, lista_tickets=None):
        """Llena la tabla con los tickets que recibe (o con todos los del gestor)"""
        # Eliminar todas las filas actuales de la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Si no se pasa lista, usar todos los tickets del gestor
        if lista_tickets is None:
            lista_tickets = self.gestor.obtener_todos()

        # Insertar cada ticket como una nueva fila en la tabla
        for ticket in lista_tickets:
            self.tree.insert("", "end", values=(
                ticket.id,
                ticket.usuario,
                ticket.descripcion,
                ticket.categoria,
                ticket.prioridad,
                ticket.estado,
                ticket.fecha
            ))

    def crear_ticket(self):
        """Toma los datos del formulario y crea un nuevo ticket"""
        usuario = self.entry_usuario.get().strip()
        descripcion = self.entry_desc.get().strip()
        categoria = self.combo_cat.get()
        prioridad = self.varias_prioridades.get()

        # Validar que los campos obligatorios no estén vacíos
        if not usuario or not descripcion:
            messagebox.showwarning("Campos vacíos", "Usuario y Descripción son obligatorios.")
            return  # Salir sin hacer nada

        # Pedir al gestor que cree el ticket (se guarda en JSON automáticamente)
        self.gestor.crear_ticket(usuario, descripcion, categoria, prioridad)

        # Limpiar los campos del formulario
        self.entry_usuario.delete(0, "end")
        self.entry_desc.delete(0, "end")

        # Refrescar tabla y métricas
        self.cargar_tabla()
        self.actualizar_metricas()

    def actualizar_metricas(self):
        """Calcula y muestra el total, pendientes y resueltos"""
        tickets = self.gestor.obtener_todos()
        total = len(tickets)
        # Contar cuántos tienen estado "Pendiente"
        pendientes = sum(1 for t in tickets if t.estado == "Pendiente")
        # Contar cuántos tienen estado "Resuelto"
        resueltos = sum(1 for t in tickets if t.estado == "Resuelto")
        
        # Actualizar el texto de las etiquetas
        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_pendientes.config(text=f"Pendientes: {pendientes}")
        self.lbl_resueltos.config(text=f"Resueltos: {resueltos}")

    def filtrar_tabla(self, event=None):
        """Filtra los tickets de la tabla según el texto del buscador"""
        texto = self.entry_filtro.get().strip().lower()  # Texto a buscar (minúsculas)
        todos = self.gestor.obtener_todos()

        if texto == "":
            # Si no hay texto, mostrar todos los tickets
            self.cargar_tabla(todos)
        else:
            # Lista para guardar los que coincidan
            filtrados = []
            for ticket in todos:
                # Si el texto aparece en algún campo del ticket, lo añadimos
                if (texto in ticket.usuario.lower() or
                    texto in ticket.descripcion.lower() or
                    texto in ticket.categoria.lower() or
                    texto in ticket.prioridad.lower() or
                    texto in ticket.estado.lower()):
                    filtrados.append(ticket)
            # Cargar la tabla solo con los tickets filtrados
            self.cargar_tabla(filtrados)

    def marcar_resuelto(self):
        """Cambia el estado del ticket seleccionado a 'Resuelto'"""
        seleccion = self.tree.selection()  # Obtener la fila seleccionada
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un ticket de la tabla.")
            return
        
        item = self.tree.item(seleccion[0])      # Datos de la fila seleccionada
        id_ticket = item["values"][0]            # El ID es el primer valor
        
        # Intentar actualizar el estado a "Resuelto"
        if self.gestor.actualizar_estado(id_ticket, "Resuelto"):
            self.cargar_tabla()
            self.actualizar_metricas()
            messagebox.showinfo("Éxito", f"Ticket #{id_ticket} marcado como Resuelto.")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el ticket.")

    def eliminar_ticket(self):
        """Elimina el ticket seleccionado después de pedir confirmación"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un ticket de la tabla.")
            return
        
        item = self.tree.item(seleccion[0])
        id_ticket = item["values"][0]
        
        # Pedir confirmación antes de eliminar
        if messagebox.askyesno("Confirmar", f"¿Eliminar definitivamente el ticket #{id_ticket}?"):
            if self.gestor.eliminar_ticket(id_ticket):
                self.cargar_tabla()
                self.actualizar_metricas()
                messagebox.showinfo("Eliminado", f"Ticket #{id_ticket} eliminado.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el ticket.")
