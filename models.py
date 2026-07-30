import json  # Para leer y escribir el archivo JSON
from datetime import datetime #importar la fecha
class Ticket:
    """Representa un ticket de soporte técnico"""
    def __init__(self, id, usuario, descripcion, categoria, prioridad, estado="Pendiente",fecha=None):
        # Guardamos los datos del ticket como atributos
        self.id = id
        self.usuario = usuario
        self.descripcion = descripcion
        self.categoria = categoria
        self.prioridad = prioridad
        self.estado = estado
        if fecha is None:
            self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        else:
            self.fecha=fecha 
    def to_dict(self):
        """Convierte el ticket a un diccionario para guardarlo en JSON"""
        return {
            "id": self.id,
            "usuario": self.usuario,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "fecha":self.fecha
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un Ticket a partir de un diccionario (lo leído del JSON)"""
        return cls(
            id=datos["id"],
            usuario=datos["usuario"],
            descripcion=datos["descripcion"],
            categoria=datos["categoria"],
            prioridad=datos["prioridad"],
            estado=datos.get("estado", "Pendiente"),  # Si no tiene estado, "Pendiente"
            fecha=datos.get("fecha","")
        )

class TicketManager:
    """Gestiona la lista de tickets y el archivo JSON"""
    def __init__(self, archivo="tickets.json"):
        self.archivo = archivo  # Nombre del archivo donde se guardan los datos
        self.tickets = []        # Lista de objetos Ticket
        self.cargar_datos()      # Al iniciar, carga los tickets que ya existan

    def cargar_datos(self):
        """Lee el archivo JSON y llena la lista de tickets"""
        try:
            with open(self.archivo, "r") as f:
                lista_dicts = json.load(f)      # Lee el JSON y lo convierte a lista de diccionarios
                self.tickets = []               # Vacía la lista actual
                for datos in lista_dicts:
                    ticket = Ticket.from_dict(datos)  # Convierte cada diccionario en un Ticket
                    self.tickets.append(ticket)       # Lo añade a la lista
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o tiene errores, empezamos con lista vacía
            self.tickets = []

    def guardar_datos(self):
        """Guarda la lista de tickets en el archivo JSON"""
        lista_dicts = []
        for ticket in self.tickets:
            lista_dicts.append(ticket.to_dict())  # Convierte cada ticket a diccionario
        with open(self.archivo, "w") as f:
            json.dump(lista_dicts, f, indent=4)   # Guarda con formato legible

    def siguiente_id(self):
        """Devuelve el ID más alto + 1 para un nuevo ticket (o 1 si no hay ninguno)"""
        if not self.tickets:
            return 1
        max_id = max(ticket.id for ticket in self.tickets)  # Busca el ID máximo actual
        return max_id + 1

    def crear_ticket(self, usuario, descripcion, categoria, prioridad):
        """Crea un ticket nuevo, lo guarda y lo devuelve"""
        nuevo = Ticket(
            id=self.siguiente_id(),  # Asigna el siguiente ID disponible
            usuario=usuario,
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad)
        self.tickets.append(nuevo)   # Lo añade a la lista
        self.guardar_datos()         # Guarda los cambios en el archivo
        return nuevo

    def obtener_todos(self):
        """Devuelve la lista completa de tickets"""
        return self.tickets

    def actualizar_estado(self, id, nuevo_estado):
        """Cambia el estado de un ticket por su ID. Devuelve True si lo encontró"""
        for ticket in self.tickets:
            if ticket.id == id:
                ticket.estado = nuevo_estado   # Cambia el estado
                self.guardar_datos()           # Guarda los cambios
                return True                    # Éxito
        return False  # No encontró el ticket con ese ID

    def eliminar_ticket(self, id):
        """Elimina un ticket por su ID. Devuelve True si lo encontró"""
        for i, ticket in enumerate(self.tickets):  # enumerate nos da índice y objeto
            if ticket.id == id:
                del self.tickets[i]   # Borra el ticket de la lista
                self.guardar_datos()  # Guarda los cambios
                return True
        return False  # No lo encontró