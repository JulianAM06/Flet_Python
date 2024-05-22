import flet as ft
import psycopg2
import os
import threading

# Definir variables de entorno para la conexión a la base de datos
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = 'julianalzate06'
DB_NAME = 'PruebaFlet'

def main(page: ft.Page):
    page.title = 'CRUD + PostgreSQL'
    page.padding = 30
    page.bgcolor = ft.colors.BLACK
    page.theme_mode = 'dark'
    page.scroll = 'always'

    def conectar_bd():
        try:
            return psycopg2.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        except psycopg2.Error as err:
            print(f"Error de conexión: {err}")
            return None

    def crear_tabla():
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL
                )
            """)
            conexion.commit()
            cursor.close()
            conexion.close()

    def cargar_datos():
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM items")
            records = cursor.fetchall()
            lista_items.controls.clear()
            for row in records:
                lista_items.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(row[1], size=18),  # Nombre del ítem
                                ft.Text(f"ID: {row[0]}", size=16),  # ID del ítem
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    on_click=lambda e, id=row[0], nombre=row[1]: editar_item(id, nombre)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, id=row[0]: eliminar_item(id)
                                ),
                            ],
                            alignment="center",  # Centra los elementos en el Row
                            spacing=10  # Espacio entre los elementos
                        ),
                        padding=ft.padding.all(10),  # Añade algo de padding alrededor del contenedor
                        border_radius=ft.border_radius.all(5),  # Bordes redondeados para el contenedor
                    )
                )
            cursor.close()
            conexion.close()
            page.update()


    def agregar_item(e):
        nombre = input_nombre.value
        if nombre:
            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO items (nombre) VALUES (%s)", (nombre,))
                conexion.commit()
                cursor.close()
                conexion.close()
                input_nombre.value = ""
                cargar_datos()

    def editar_item(id, nombre):
        input_nombre.value = nombre
        boton_guardar.on_click = lambda e: actualizar_item(id)
        page.update()

    def actualizar_item(id):
        nuevo_nombre = input_nombre.value
        if nuevo_nombre:
            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("UPDATE items SET nombre = %s WHERE id = %s", (nuevo_nombre, id))
                conexion.commit()
                cursor.close()
                conexion.close()
                input_nombre.value = ""
                boton_guardar.on_click = agregar_item
                cargar_datos()

    def eliminar_item(id):
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM items WHERE id = %s", (id,))
            conexion.commit()
            cursor.close()
            conexion.close()
            cargar_datos()

    def buscar_item(e):
        nombre = input_nombre.value.capitalize()
        if nombre:
            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM items WHERE nombre = %s", (nombre,))
                datos = cursor.fetchall()
                print(datos)
                if datos:
                    input_nombre.value = "Si Existe"
                else:
                    input_nombre.value = "No Existe"
                conexion.commit()
                cursor.close()
                conexion.close()
                threading.Timer(2.0, limpiarInput).start()
                cargar_datos()
    
    def limpiarInput():
        input_nombre.value = ""
        page.update()
        cargar_datos()


    # Crear tabla si no existe
    crear_tabla()

    # UI Elements
    display = ft.Text(value="", col={"sm": 6}, size=20, text_align='center')
    input_nombre = ft.TextField(label='Nombre')
    boton_guardar = ft.ElevatedButton(text='Agregar', on_click=agregar_item)
    boton_buscar = ft.ElevatedButton(text='Buscar', on_click=buscar_item)
    lista_items = ft.ListView()

    page.add(
        ft.Column(
            controls=[
                display,
                input_nombre,
                boton_guardar,
                boton_buscar,
                lista_items
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    # Cargar datos iniciales
    cargar_datos()

ft.app(target=main)
