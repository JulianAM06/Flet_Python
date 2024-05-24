import flet as ft
import psycopg2
import os
import threading

# Definir variables de entorno para la conexión a la base de datos
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = 'julianalzate06'
DB_NAME = 'loginFlet'

def main(page: ft.Page):
    page.title = 'Login + PostgreSQL'
    page.padding = 30
    page.bgcolor = ft.colors.BLACK
    page.theme_mode = 'dark'
    page.scroll = 'always'
    page.window_width = 800  # Ancho de la ventana
    page.window_height = 500  # Alto de la ventana

    def limpiarDisplay():
        display.value = ""
        page.update()

    def conectarBD():
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
        
    def crearTabla():
        conexion = conectarBD()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Login (
                    idLogin SERIAL PRIMARY KEY,
                    usuario VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL
                )      
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Estudiante (
                    idEstudiante SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    contacto INTEGER NOT NULL
                )      
            """)
            conexion.commit()
            cursor.close()
            conexion.close()

    def agregarLogin(e):
        u1 = username.value
        p1 = password.value
        conexion = conectarBD()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO Login (usuario, password) VALUES(%s,%s)", (u1, p1))
            conexion.commit()
            cursor.close()
            conexion.close()
            username.value = ""
            password.value = ""
            display.value = "Guardado Exitosamente!!!"
            threading.Timer(4.0, limpiarDisplay).start()
            page.update()
        else:
            display.value = "Intenta Nuevamente!!!"

        page.update()

    def hacerLogin(e):
        u2 = loginUsername.value
        p2 = loginPassword.value
        conexion = conectarBD()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Login WHERE usuario = (%s) AND password = (%s) ", (u2, p2))
            datos = cursor.fetchall()
            if datos:
                for i in datos:
                    username1 = i[1]
                    password1 = i[2]
                if username1 == u2 and password1 == p2:
                    loginUsername.value = ""
                    loginPassword.value = ""
                    display.value = "Bienvenido al Sistema"
                    threading.Timer(4.0, limpiarDisplay).start()
                    page.update()
            else:
                display.value = "Usuario o Contraseña Incorrecta"
                threading.Timer(4.0, limpiarDisplay).start()
                page.update()
        
        page.update()

    
    display = ft.Text(value="", col={"sm": 6}, size=20, text_align='center')
    username = ft.TextField(width=300, hint_text='Ingresa Usuario')
    password = ft.TextField(width=300, hint_text='Ingresa Password', password=True)
    registrarse = ft.ElevatedButton(text='Registrarse', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK, on_click=agregarLogin)
    loginUsername = ft.TextField(width=300, hint_text='Ingresa Usuario')
    loginPassword = ft.TextField(width=300, hint_text='Ingresa Password', password=True)
    iniciarSesion = ft.ElevatedButton(text='Iniciar Sesion', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK, on_click=hacerLogin)

    page.add(
        ft.ResponsiveRow(
            controls=[display], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[username], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[password], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[registrarse], alignment=ft.MainAxisAlignment.CENTER
        ),
         ft.ResponsiveRow(
            controls=[loginUsername], alignment=ft.MainAxisAlignment.CENTER
        ),
         ft.ResponsiveRow(
            controls=[loginPassword], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[iniciarSesion], alignment=ft.MainAxisAlignment.CENTER
        )
    )

    crearTabla()
        
ft.app(target=main)

