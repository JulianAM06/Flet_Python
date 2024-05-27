import flet as ft
import psycopg2
import threading

DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = 'julianalzate06'
DB_NAME = 'inventarioFlet'

productoEncontrado = None

def main (page: ft.Page):

    global productoEncontrado
    
    page.title = "Inventario + PostgreSQL"
    page.padding = 30
    page.bgcolor = ft.colors.BLACK
    page.theme_mode = 'dark'
    page.scroll = 'always'
    page.window_width = 1100  # Ancho de la ventana
    page.window_height = 800  # Alto de la ventana
    

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
                CREATE TABLE IF NOT EXISTS Productos (
                    idProducto SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio FLOAT NOT NULL
                )      
            """)
            conexion.commit()
            cursor.close()
            conexion.close()
    
    def cambio_ruta (route):
        page.views.clear
        page.views.append(
            #Vista para Loguearse
            ft.View(
                "/",
                [
                ft.Container(height=100),
                display,
                loginUsername,
                loginPassword, 
                iniciarSesion,
                ft.ElevatedButton("Registro", on_click=lambda _:page.go("/registro"))
                ], 
                scroll="always",
                vertical_alignment="center",
                horizontal_alignment="center"     
            )
        )
        # Vista Principal 
        if page.route == "/home":
            
            page.views.append(
                ft.View(
                    "/home",
                    [
                    ft.AppBar(title=ft.Text("Home"), bgcolor=ft.colors.RED),
                    ft.Row([ft.ElevatedButton("Crear Producto", on_click=lambda _:page.go("/home/crear"), bgcolor=ft.colors.TEAL, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Actualizar Producto", on_click=lambda _:page.go("/home/actualizar"), bgcolor=ft.colors.TEAL, color=ft.colors.WHITE, height=50, width=300)], alignment="center"),
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )
        # Vista para Crear Productos    
        if page.route == "/home/crear":
            
            page.views.append(
                ft.View(
                    "/crear",
                    [
                    ft.AppBar(title=ft.Text("Crear Producto"), bgcolor=ft.colors.TEAL),                    
                    ft.Container(height=50),
                    display,
                    ft.Row([ft.Container(width=50),producto, cantidad, precio]),
                    ft.Container(height=20),
                    crearProducto,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/home"))
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )
        # Vista para Actualizar Productos
        if page.route == "/home/actualizar":
            
            page.views.append(
                ft.View(
                    "/actualizar",
                    [
                    ft.AppBar(title=ft.Text("Actualizar Producto"), bgcolor=ft.colors.BLUE),                    
                    ft.Container(height=50),
                    display,
                    buscar,
                    ft.Row([ft.Container(width=50),producto, cantidad, precio]),
                    ft.Container(height=20),
                    actualizarProducto,
                    buscarProducto,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/home"))
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )
        # Vista para Registarse
        if page.route == "/registro":
            
            page.views.append(
                ft.View(
                    "/registro",
                    [
                    ft.AppBar(title=ft.Text("Registro"), bgcolor=ft.colors.CYAN),
                    display,
                    username,
                    password,
                    registrarse
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center"
                )
            )
        page.update()
        
    
    def vista_atras(view):
        
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        page.update()

    

    def agregarLogin(e):
        u1 = username.value
        p1 = password.value
        if username.value and password.value:
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
                page.go("/")
                page.update()
            else:
                display.value = "Intenta Nuevamente!!!"
        else:
            username.error_text = "Ingresa Username"
            password.error_text = "Ingresa Password"
        page.update()

    def vistaHome():
        page.go("/home")
        page.update()

    def hacerLogin(e):
        u2 = loginUsername.value
        p2 = loginPassword.value
        if loginUsername.value and loginPassword.value:
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
                        display.value = "Bienvenido al Sistema Inventario"
                        threading.Timer(4.0, limpiarDisplay).start()
                        threading.Timer(4.0, vistaHome).start()
                        page.update()
                else:
                    display.value = "Usuario o Contraseña Incorrecta"
                    threading.Timer(4.0, limpiarDisplay).start()
                    page.update()
        else:
            loginUsername.error_text = "Ingresa Username"
            loginPassword.error_text = "Ingresa Password"
            page.update()
        
        page.update()

    def vistaHome2():
        page.go("/home")
        crearProducto.disabled = False
        producto.value = ""
        cantidad.value = ""
        precio.value = ""
        display.value = ""
        page.update()

    def crearProducto1(e):
        p1 = producto.value.capitalize()
        c1 = cantidad.value
        v1 = precio.value
        if producto.value and cantidad.value and precio.value:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO Productos (nombre, cantidad, precio) VALUES (%s, %s, %s)", (p1, c1, v1))
                conexion.commit()
                cursor.close()
                conexion.close()
                crearProducto.disabled = True
                display.value = "Producto Guardado Exitosamente!!!"
                threading.Timer(4.0, vistaHome2).start()
                page.update()
        else:
            producto.error_text = "Ingresa Producto"
            cantidad.error_text = "Ingresa Cantidad"
            precio.error_text = "Ingresa Precio"
            page.update()

        page.update()

    def buscarProducto1(e):
        global productoEncontrado
        b1 = buscar.value.capitalize()
        if buscar.value:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM Productos WHERE nombre = %s", (b1,))
                datos = cursor.fetchall()
                print(datos)
                conexion.commit()
                cursor.close()
                conexion.close()
                if datos:
                    for i in datos:
                        productoEncontrado = i[0]
                        display.value = "Si Existe Producto, Ingresa los nuevos datos y da clic en Actualizar Producto"
                        producto.disabled = False
                        cantidad.disabled = False
                        precio.disabled = False
                        actualizarProducto.disabled = False
                        threading.Timer(4.0, limpiarDisplay).start()
                        print(productoEncontrado)
                        actualizarProducto.on_click = lambda e: ejecutarActualizar()
                        page.update()
                else:
                    display.value = "No Existe"
                    page.update()

        page.update()

    def ejecutarActualizar():
        global productoEncontrado
        nuevoNombre = producto.value.capitalize()
        nuevaCantidad = cantidad.value
        nuevoPrecio = precio.value
        if productoEncontrado and nuevoNombre and nuevaCantidad and nuevoPrecio:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "UPDATE Productos SET nombre = %s, cantidad = %s, precio = %s WHERE idProducto = %s",
                    (nuevoNombre, nuevaCantidad, nuevoPrecio, productoEncontrado)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
                display.value = "Producto Actualizado Exitosamente!!!"
                producto.value = ""
                cantidad.value = ""
                precio.value = ""
                producto.disabled = True
                cantidad.disabled = True
                precio.disabled = True
                actualizarProducto.disabled = True
                threading.Timer(4.0, limpiarDisplay).start()
                page.update()
            else:
                display.value = "Error al actualizar, intenta nuevamente."



        

    username = ft.TextField(hint_text="Username...", width=300)
    password = ft.TextField(hint_text="Password...", password=True, width=300)
    display = ft.Text(value="", col={"sm": 6}, size=20, text_align='center')
    registrarse = ft.ElevatedButton(text='Registrarse', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK, on_click=agregarLogin)
    loginUsername = ft.TextField(width=300, hint_text='Ingresa Usuario')
    loginPassword = ft.TextField(width=300, hint_text='Ingresa Password', password=True)
    iniciarSesion = ft.ElevatedButton(text='Iniciar Sesion', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK, on_click=hacerLogin)
    producto = ft.TextField(hint_text="Producto", width=300, disabled=True)
    cantidad = ft.TextField(hint_text="Cantidad", width=300, disabled=True)
    precio = ft.TextField(hint_text="Precio", width=300, disabled=True)
    buscar = ft.TextField(hint_text="Buscar", width=300)
    crearProducto = ft.ElevatedButton(text='Crear Producto', col={"sm": 3}, bgcolor=ft.colors.TEAL, color=ft.colors.BLACK, on_click=crearProducto1)
    actualizarProducto = ft.ElevatedButton(text='Actualizar Producto', col={"sm": 3}, bgcolor=ft.colors.BLUE, color=ft.colors.BLACK, disabled=True)
    buscarProducto = ft.ElevatedButton(text='Buscar Producto', col={"sm": 3}, bgcolor=ft.colors.GREEN, color=ft.colors.BLACK, on_click=buscarProducto1)
    
    page.on_route_change = cambio_ruta
    page.on_view_pop = vista_atras
    page.go(page.route)
    crearTabla()
    page.update()
    
ft.app(target=main, assets_dir='assets')