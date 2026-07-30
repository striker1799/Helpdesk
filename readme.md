🖥️ DataDesk – Sistema de Gestión de Tickets de Soporte
Python Tkinter JSON Licencia Estado

DataDesk es una aplicación de escritorio para la gestión de tickets de soporte técnico (helpdesk).
Permite crear, visualizar, filtrar, actualizar el estado y eliminar incidencias, con persistencia en un archivo JSON.

Desarrollada con Python y Tkinter, aplicando el patrón de diseño Separación de Responsabilidades (SoC) y principios de Programación Orientada a Objetos (POO).

📸 Vista previa
DataDesk en funcionamiento

Interfaz principal con tema aqua personalizado, tabla interactiva y panel de métricas.

✨ Características principales
CRUD completo de tickets (Crear, Leer, Actualizar estado, Eliminar).
Formulario validado con campos de texto y listas desplegables (categoría, prioridad).
Tabla interactiva (Treeview) que muestra todos los tickets con columnas ordenadas.
Columna de fecha automática: cada ticket registra su fecha y hora de creación.
Buscador en tiempo real: filtra por cualquier campo mientras escribes.
Panel de métricas: total de tickets, pendientes y resueltos actualizados al instante.
Confirmaciones y alertas con messagebox (eliminar, marcar resuelto, validaciones).
Persistencia en JSON: los datos se cargan al iniciar y se guardan automáticamente en cada cambio.
Interfaz personalizada: tema visual aqua con estilos ttk.Style y colores definidos.
🛠️ Tecnologías utilizadas
Python 3.8+ – Lenguaje de programación.
Tkinter / ttk – Biblioteca estándar para interfaces gráficas.
JSON – Almacenamiento persistente de datos.
módulos estándar: datetime, os, tkinter.messagebox.
Git / GitHub – Control de versiones y publicación del portafolio.
📁 Estructura del proyecto
DataDesk/
├── models.py # Capa de lógica de negocio y persistencia (POO)
├── views.py # Capa de interfaz gráfica (Tkinter)
├── main.py # Punto de entrada de la aplicación
├── tickets.json # Archivo de datos (se genera automáticamente)
└── README.md # Documentación del proyecto
El código sigue el patrón Separación de Responsabilidades (SoC):

models.py: define las clases Ticket y TicketManager (CRUD, carga/guardado JSON).
views.py: contiene la clase Aplicacion (hereda de tk.Tk) con todos los widgets y eventos.
main.py: instancia la aplicación e inicia el bucle principal.
🚀 Instalación y ejecución
Requisitos previos
Tener instalado Python 3.8 o superior.
No se necesitan dependencias externas (Tkinter viene incluido en la instalación estándar de Python).
Pasos para ejecutar
Clona el repositorio:
  git clone https://github.com/tu-usuario/DataDesk.git
  cd DataDesk
Clona el repositorio:
git clone https://github.com/tu-usuario/DataDesk.git
cd DataDesk
Ejecuta la aplicación:
python main.py
Usa la aplicación: Completa el formulario y haz clic en Crear Ticket.

Visualiza los tickets en la tabla.

Filtra escribiendo en el campo Filtrar.

Selecciona un ticket y usa los botones Marcar como Resuelto o Eliminar.

Los cambios se guardan automáticamente en tickets.json.

🧪 Cómo probar las funcionalidades Crea varios tickets con diferentes categorías y prioridades.

Utiliza el buscador para filtrar por usuario, estado o cualquier palabra.

Marca algunos como "Resuelto" y observa cómo se actualizan los contadores.

Elimina un ticket y confirma la acción en el diálogo.

Cierra la aplicación, vuelve a abrirla y verifica que los datos persisten.

🎨 Personalización Si deseas cambiar los colores del tema, puedes modificar las variables al inicio de init en views.py:

python

color_primario = "#4FC3F7"
📄 Licencia Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles (si lo incluyes) o añade el texto estándar de la licencia MIT.

🙋‍♂️ Autor Desarrollado por Robert Alin – striker1799 Proyecto creado como parte del portafolio profesional para demostrar habilidades en Python, POO, GUI y persistencia de datos.

⭐ Agradecimientos Si este proyecto te resulta útil, ¡no olvides darle una estrella en GitHub! Cualquier sugerencia o mejora es bienvenida a través de issues o pull requests.
