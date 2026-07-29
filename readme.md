# 🖥️ DataDesk Helpdesk System

**Sistema de escritorio para la gestión de tickets de soporte técnico**  
Desarrollado con **Python**, **Tkinter** y **JSON** como proyecto de portafolio profesional.

![Vista previa de la aplicación](https://via.placeholder.com/800x400?text=DataDesk+en+funcionamiento](https://i.postimg.cc/KY6qYWjn/ejemplo.png)

---

## 📋 Descripción

**DataDesk** es una aplicación de escritorio diseñada para optimizar la gestión de incidencias internas en empresas del sector tecnológico. Permite crear, visualizar, filtrar, actualizar y eliminar tickets de soporte, todo desde una interfaz gráfica intuitiva y con persistencia de datos en archivos JSON.

Este proyecto demuestra habilidades en:

- Programación Orientada a Objetos (POO) en Python.
- Desarrollo de interfaces gráficas con Tkinter y ttk.
- Separación de responsabilidades (SoC) en tres capas bien definidas.
- Persistencia de datos sin base de datos externa.
- Escritura de código limpio, tipado estático y documentado.

---

## ✨ Características principales

- **CRUD completo** de tickets (Crear, Leer, Actualizar, Eliminar).
- **Formulario de entrada** con validación de campos y combos desplegables.
- **Tabla interactiva** (Treeview) que muestra todos los tickets con colores según estado.
- **Búsqueda en tiempo real** para filtrar tickets por cualquier campo.
- **Panel de métricas** automático: total de tickets, pendientes y resueltos.
- **Mensajes de alerta** (messagebox) para confirmar borrados y mostrar errores.
- **Persistencia en JSON**: los datos se guardan automáticamente al modificar un ticket.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.x** (tipado estático con `typing`)
- **Tkinter / ttk** (interfaz gráfica nativa)
- **JSON** (almacenamiento persistente)
- **Módulos estándar** (`os`, `json`, `tkinter.messagebox`)

---

## 📁 Estructura del proyecto

El código sigue el patrón **Separación de Responsabilidades (SoC)** y se divide en tres módulos:
