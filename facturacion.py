import flet as ft
import psycopg2
import threading

DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = 'julianalzate06'
DB_NAME = 'inventarioFlet'

productoEncontrado = None

usuarioEncontrado = None

clienteEncontrado = None

productos_table = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Producto")),
        ft.DataColumn(ft.Text("Cantidad")),
        ft.DataColumn(ft.Text("Precio"))
    ],
    rows=[]
)

def main (page: ft.Page):

    global productoEncontrado

    global usuarioEncontrado

    global clienteEncontrado
    
    page.title = "Facturacion + Inventario + PostgreSQL"
    page.padding = 30
    page.bgcolor = ft.colors.BLACK
    page.theme_mode = 'dark'
    page.scroll = 'always'
    page.window_width = 1100  # Ancho de la ventana
    page.window_height = 580  # Alto de la ventana
    

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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Clientes (
                    idCliente SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    cedula VARCHAR(100) UNIQUE NOT NULL,
                    contacto VARCHAR(100) NOT NULL
                )      
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Facturas (
                    idFactura SERIAL PRIMARY KEY,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    cantidad INTEGER NOT NULL,
                    total FLOAT NOT NULL,
                    fkCliente INTEGER NOT NULL,
                    fkProducto INTEGER NOT NULL,
                    FOREIGN KEY (fkCliente) REFERENCES Clientes(idCliente),
                    FOREIGN KEY (fkProducto) REFERENCES Productos(idProducto)      
                    
                )      
            """)
            conexion.commit()
            cursor.close()
            conexion.close()

    def cargar_datos():
        conexion = conectarBD()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Productos")
            records = cursor.fetchall()
            productos_table.rows.clear()
            for row in records:
                productos_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row[1])),  # Nombre del producto
                            ft.DataCell(ft.Text(str(row[2]))),  # Cantidad del producto
                            ft.DataCell(ft.Text(f"${row[3]}"))  # Precio del producto
                        ]
                    )
                )
            cursor.close()
            conexion.close()
            page.update()
    
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
                ft.ElevatedButton("Registrarse", on_click=lambda _:page.go("/registro")),
                ft.ElevatedButton("Cambiar Contraseña", on_click=lambda _:page.go("/cambiarContraseña"))
                ], 
                scroll="always",
                vertical_alignment="center",
                horizontal_alignment="center"     
            )
        )
        # Vista Principal 
        if page.route == "/home":
            cargar_datos()
            page.views.append(
                ft.View(
                    "/home",
                    [
                    ft.AppBar(title=ft.Text("Sistema Facturacion + Inventario"), bgcolor=ft.colors.TEAL),
                    ft.Row([ft.ElevatedButton("Productos", on_click=lambda _:page.go("/productos"), bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Clientes", on_click=lambda _:page.go("/clientes"), bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Facturas", on_click=lambda _:page.go("/facturas"), bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE, height=50, width=300)], alignment="center"),
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista Principal Facturas    
        if page.route == "/facturas":
            cargar_datos()
            page.views.append(
                ft.View(
                    "/facturas",
                    [
                    ft.AppBar(
                        title=ft.Text("Facturas"), 
                        bgcolor=ft.colors.ORANGE,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/home") 
                            )
                    ),
                    ft.Row([ft.ElevatedButton("Crear Factura", on_click=lambda _:page.go("/facturas/crear"), bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Actualizar Factura", on_click=lambda _:page.go("/facturas/actualizar"), bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Eliminar Factura", on_click=lambda _:page.go("/facturas/eliminar"), bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE, height=50, width=300)], alignment="center"),
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista Principal Clientes    
        if page.route == "/clientes":
            cargar_datos()
            page.views.append(
                ft.View(
                    "/clientes",
                    [
                    ft.AppBar(
                        title=ft.Text("Clientes"), 
                        bgcolor=ft.colors.GREEN,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/home") 
                            )
                    ),
                    ft.Row([ft.ElevatedButton("Crear Cliente", on_click=lambda _:page.go("/clientes/crear"), bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Actualizar Cliente", on_click=lambda _:page.go("/clientes/actualizar"), bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Eliminar Cliente", on_click=lambda _:page.go("/clientes/eliminar"), bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, height=50, width=300)], alignment="center"),
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista para Crear Clientes
        if page.route == "/clientes/crear":
            cargar_datos()
            page.views.append(
                ft.View(
                    "/clientes",
                    [
                    ft.AppBar(
                        title=ft.Text("Crear Cliente"), 
                        bgcolor=ft.colors.GREEN,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/clientes") 
                            )
                    ),
                    ft.Container(height=50),
                    display,
                    ft.Row([ft.Container(width=50),clienteCrearNombre, clienteCrearApellido, clienteCrearCedula, clienteCrearContacto]),
                    ft.Container(height=20),
                    crearCliente,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/clientes"))
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )
        
        # Vista para Actualizar Clientes
        if page.route == "/clientes/actualizar":
            
            page.views.append(
                ft.View(
                    "/actualizar",
                    [
                    ft.AppBar(
                        title=ft.Text("Actualizar Cliente"), 
                        bgcolor=ft.colors.GREEN,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/clientes") 
                            )
                    ),                    
                    ft.Container(height=50),
                    display,
                    buscarCliente,
                    ft.Row([ft.Container(width=50),clienteNombre, clienteApellido, clienteCedula, clienteContacto]),
                    ft.Container(height=20),
                    actualizarCliente,
                    buscarClienteActualizar,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/clientes"))
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista para Eliminar Clientes
        if page.route == "/clientes/eliminar":
            
            page.views.append(
                ft.View(
                    "/eliminar",
                    [
                    ft.AppBar(
                        title=ft.Text("Eliminar Cliente"), 
                        bgcolor=ft.colors.GREEN,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/clientes") 
                            )
                    ),                    
                    ft.Container(height=50),
                    display,
                    buscarCliente,
                    ft.Container(height=20),
                    eliminarCliente,
                    buscarClienteEliminar,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/clientes"))
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista Principal Productos
        if page.route == "/productos":
            cargar_datos()
            page.views.append(
                ft.View(
                    "/productos",
                    [
                    ft.AppBar(
                        title=ft.Text("Productos"), 
                        bgcolor=ft.colors.BLUE,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/home") 
                            )
                    ),
                    ft.Row([ft.ElevatedButton("Crear Producto", on_click=lambda _:page.go("/productos/crear"), bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Actualizar Producto", on_click=lambda _:page.go("/productos/actualizar"), bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, height=50, width=300), ft.ElevatedButton("Eliminar Producto", on_click=lambda _:page.go("/productos/eliminar"), bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, height=50, width=300)], alignment="center"),
                    productos_table
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista para Crear Productos    
        if page.route == "/productos/crear":
            
            page.views.append(
                ft.View(
                    "/crear",
                    [
                    ft.AppBar(
                        title=ft.Text("Crear Producto"), 
                        bgcolor=ft.colors.BLUE,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/productos") 
                            )
                    ),                    
                    ft.Container(height=50),
                    display,
                    ft.Row([ft.Container(width=50),productoCrear, cantidadCrear, precioCrear]),
                    ft.Container(height=20),
                    crearProducto,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/productos"))
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista para Actualizar Productos
        if page.route == "/productos/actualizar":
            
            page.views.append(
                ft.View(
                    "/actualizar",
                    [
                    ft.AppBar(
                        title=ft.Text("Actualizar Producto"), 
                        bgcolor=ft.colors.BLUE,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/productos") 
                            )
                    ),                    
                    ft.Container(height=50),
                    display,
                    buscarProducto,
                    ft.Row([ft.Container(width=50),producto, cantidad, precio]),
                    ft.Container(height=20),
                    actualizarProducto,
                    buscarProductoActualizar,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/productos"))
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
                )
            )

        # Vista para Eliminar Productos
        if page.route == "/productos/eliminar":
            
            page.views.append(
                ft.View(
                    "/eliminar",
                    [
                    ft.AppBar(
                        title=ft.Text("Eliminar Producto"), 
                        bgcolor=ft.colors.BLUE,
                        leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/productos")  
                            )
                    ),                    
                    ft.Container(height=50),
                    display,
                    buscarProducto,
                    ft.Container(height=20),
                    eliminarProducto,
                    buscarProductoEliminar,
                    ft.ElevatedButton("Regresar", on_click=lambda _:page.go("/productos"))
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
                    ft.AppBar(title=ft.Text("Registrarse"), bgcolor=ft.colors.TEAL),
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

        # Vista para cambiar o actualizar contraseña (Seguridad o Perdida)
        if page.route == "/cambiarContraseña":
            
            page.views.append(
                ft.View(
                    "/cambiarContraseña",
                    [
                    ft.AppBar(title=ft.Text("Cambiar Contraseña"), bgcolor=ft.colors.TEAL),
                    display,
                    username2,
                    nuevaContraseña,
                    confirmarContraseña,
                    actualizarContraseña,
                    buscarUsuario
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

    def vistaHome():
        page.go("/home")
        page.update()

    def vistaLogin():
        page.go("/")
        page.update()

    def vistaClientes():
        page.go("/clientes")
        display.value = ""
        crearCliente.disabled = False
        clienteCrearNombre.value = ""
        clienteCrearApellido.value = ""
        clienteCrearCedula.value = ""
        clienteCrearContacto.value = ""
        page.update()

    def vistaProductos():
        page.go("/productos")
        crearProducto.disabled = False
        producto.value = ""
        cantidad.value = ""
        precio.value = ""
        display.value = ""
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
                threading.Timer(3.0, limpiarDisplay).start()
                page.go("/")
                page.update()
            else:
                display.value = "Intenta Nuevamente!!!"
        else:
            username.error_text = "Ingresa Username"
            password.error_text = "Ingresa Password"
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
                        display.value = "Bienvenido al Sistema Facturacion"
                        threading.Timer(3.0, limpiarDisplay).start()
                        threading.Timer(3.0, vistaHome).start()
                        page.update()
                else:
                    display.value = "Usuario o Contraseña Incorrecta"
                    threading.Timer(3.0, limpiarDisplay).start()
                    page.update()
        else:
            loginUsername.error_text = "Ingresa Username"
            loginPassword.error_text = "Ingresa Password"
            page.update()
        
        page.update()

    def crearProducto1(e):
        p1 = productoCrear.value.capitalize()
        c1 = cantidadCrear.value
        v1 = precioCrear.value
        if p1 and c1 and v1:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO Productos (nombre, cantidad, precio) VALUES (%s, %s, %s)", (p1, c1, v1))
                conexion.commit()
                cursor.close()
                conexion.close()
                crearProducto.disabled = True
                display.value = "Producto Guardado Correctamente!!!"
                threading.Timer(3.0, vistaProductos).start()
                page.update()
        else:
            productoCrear.error_text = "Ingresa Producto"
            cantidadCrear.error_text = "Ingresa Cantidad"
            precioCrear.error_text = "Ingresa Precio"
            page.update()

        page.update()

    def buscarProducto1(e):
        global productoEncontrado
        b1 = buscarProducto.value.capitalize()
        if buscarProducto.value:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM Productos WHERE nombre = %s", (b1,))
                datos = cursor.fetchall()
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
                        threading.Timer(3.0, limpiarDisplay).start()
                        actualizarProducto.on_click = lambda e: ejecutarActualizarProducto()
                        page.update()
                else:
                    display.value = "No Existe Producto"
                    threading.Timer(3.0, limpiarDisplay).start()
                    page.update()
        else:
            buscarProducto.error_text = "Ingresa Producto"

        page.update()

    def ejecutarActualizarProducto():
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
                display.value = "Producto Actualizado Correctamente!!!"
                producto.value = ""
                cantidad.value = ""
                precio.value = ""
                buscarProducto.value = ""
                producto.disabled = True
                cantidad.disabled = True
                precio.disabled = True
                actualizarProducto.disabled = True
                threading.Timer(3.0, limpiarDisplay).start()
                page.update()
            else:
                display.value = "Error al actualizar, intenta nuevamente."
                threading.Timer(3.0, limpiarDisplay).start()
                page.update()
        else:
            producto.error_text = "Ingresa Producto"
            cantidad.error_text = "Ingresa Cantidad"
            precio.error_text = "Ingresa Precio"
            page.update()

        page.update()

    def buscarProducto2(e):
        global productoEncontrado
        b2 = buscarProducto.value.capitalize()
        if buscarProducto.value:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM Productos WHERE nombre = %s", (b2,))
                datos = cursor.fetchall()
                conexion.commit()
                cursor.close()
                conexion.close()
                if datos:
                    for i in datos:
                        productoEncontrado = i[0]
                        display.value = "Si Existe Producto, deseas Eliminarlo?"
                        eliminarProducto.disabled = False
                        eliminarProducto.on_click = lambda e: ejecutarEliminar()
                        page.update()

                else:
                    display.value = "No Existe Producto"
                    threading.Timer(3.0, limpiarDisplay).start()
                    page.update()

        page.update()

    def ejecutarEliminar():
        display.value = ""
        global productoEncontrado
        if productoEncontrado:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM Productos WHERE idProducto = %s", (productoEncontrado,))
                conexion.commit()
                cursor.close()
                conexion.close()
                display.value = "Prodcuto Eliminado Correctamente"
                threading.Timer(3.0, limpiarDisplay).start()
                eliminarProducto.disabled = True
                buscarProducto.value = ""
                page.update()

        else:
            display.value = "No Existe Producto"
            page.update()

        page.update()

    def buscarUsuario1(e):
        global usuarioEncontrado
        u3 = username2.value
        if u3:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM Login WHERE usuario = %s", (u3,))
                datos = cursor.fetchall()
                conexion.commit()
                cursor.close()
                conexion.close()
                if datos:
                    for i in datos:
                        usuarioEncontrado = i[0]
                    display.value = "Usuario encontrado, ingresa Nueva Clave y Confirmacion"
                    nuevaContraseña.disabled = False
                    confirmarContraseña.disabled = False
                    actualizarContraseña.disabled = False
                    threading.Timer(3.0, limpiarDisplay).start()
                    actualizarContraseña.on_click = lambda e: actualizarContraseña1()
                    page.update()

                else:
                    display.value = "Usuario No Encontrado"
                    threading.Timer(3.0, limpiarDisplay).start()
                    page.update()

        else:
            username2.error_text = "Ingresa Username"
            page.update()

        page.update()


    def actualizarContraseña1():
        global usuarioEncontrado
        n1 = nuevaContraseña.value
        n2 = confirmarContraseña.value
        if usuarioEncontrado:
            if nuevaContraseña.value != "":
                if confirmarContraseña.value != "":
                    if n1 == n2:
                        conexion = conectarBD()
                        if conexion:
                            cursor = conexion.cursor()
                            cursor.execute("UPDATE Login SET password = %s WHERE idLogin = %s", (n2, usuarioEncontrado))
                            conexion.commit()
                            cursor.close()
                            conexion.close()
                            display.value = "Contraseña Actualizada Correctamente!!!"
                            username2.value = ""
                            nuevaContraseña.value = ""
                            confirmarContraseña.value = ""
                            nuevaContraseña.disabled = True
                            confirmarContraseña.disabled = True
                            actualizarContraseña.disabled = True
                            threading.Timer(3.0, limpiarDisplay).start()
                            threading.Timer(3.0, vistaLogin).start()
                            page.update()
                    else:
                        display.value = "Las contraseñas no son iguales"
                        threading.Timer(3.0, limpiarDisplay).start()
                        page.update()
                else:
                    confirmarContraseña.error_text = "Ingresa Contraseña Confirmacion"

            else:
                nuevaContraseña.error_text = "Ingresa Contraseña Nueva"

        else:
            display.value = "Usuario No Encontrado"
            threading.Timer(3.0, limpiarDisplay).start()
            page.update()

        page.update()

    def crearCliente1(e):
        n1 = clienteCrearNombre.value.capitalize()
        a1 = clienteCrearApellido.value.capitalize()
        ce1 = clienteCrearCedula.value
        co1 = clienteCrearContacto.value
        if n1 and a1 and ce1 and co1:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO Clientes (nombre, apellido, cedula, contacto) VALUES (%s,%s,%s,%s)", (n1, a1, ce1, co1))
                conexion.commit()
                cursor.close()
                conexion.close()
                crearCliente.disabled = True
                display.value = "Cliente Guardado Correctamente!!!"
                threading.Timer(3.0, vistaClientes).start()
                page.update()
        else:
            clienteCrearNombre.error_text = "Ingresa Nombre"
            clienteCrearApellido.error_text = "Ingresa Apellido"
            clienteCrearCedula.error_text = "Ingresa Cedula"
            clienteCrearContacto.error_text = "Ingresa Contacto"
            page.update()

        page.update()

    def buscarCliente1(e):
        global clienteEncontrado
        b3 = buscarCliente.value
        if b3:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM Clientes WHERE cedula = %s", (b3,))
                datos = cursor.fetchall()
                conexion.commit()
                cursor.close()
                conexion.close()
                if datos:
                    for i in datos:
                        clienteEncontrado = i[0]
                        display.value = "Cliente Encontrado, Ingresa los nuevos datos y da clic en Actualizar Cliente"
                        clienteNombre.disabled = False
                        clienteApellido.disabled = False
                        clienteCedula.disabled = False
                        clienteContacto.disabled = False
                        actualizarCliente.disabled = False
                        threading.Timer(3.0, limpiarDisplay).start()
                        actualizarCliente.on_click = lambda e: ejecutarActualizarCliente()
                        page.update()
                else:
                    display.value = "No Existe Cliente"
                    threading.Timer(3.0, limpiarDisplay).start()
                    page.update()
        else:
            buscarCliente.error_text = "Ingresa Cedula"
            page.update()

        page.update()

    def ejecutarActualizarCliente():
        global clienteEncontrado
        n2 = clienteNombre.value
        a2 = clienteApellido.value
        ce2 = clienteCedula.value
        co2 = clienteContacto.value
        if n2 and a2 and ce2 and co2:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("UPDATE Clientes SET nombre = %s, apellido = %s, cedula = %s, contacto = %s WHERE idCliente = %s", 
                               (n2, a2, ce2, co2, clienteEncontrado))
                conexion.commit()
                cursor.close()
                conexion.close()
                display.value = "Cliente Actualizado Correctamente!!!"
                clienteNombre.value = ""
                clienteApellido.value = ""
                clienteCedula.value = ""
                clienteContacto.value = ""
                buscarCliente.value = ""
                clienteNombre.disabled = True
                clienteApellido.disabled = True
                clienteCedula.disabled = True
                clienteContacto.disabled = True
                actualizarCliente.disabled = True
                threading.Timer(3.0, limpiarDisplay).start()
                page.update()
            else:
                display.value = "Error al Actualizar, intenta nuevamente."
                threading.Timer(3.0, limpiarDisplay).start()
                page.update()
        else:
            clienteNombre.error_text = "Ingresa Nombre"
            clienteApellido.error_text = "Ingresa Apellido"
            clienteCedula.error_text = "Ingresa Cedula"
            clienteContacto.error_text = "Ingresa Contacto"
            page.update()

        page.update()

    def buscarCliente2(e):
        global clienteEncontrado
        b4 = buscarCliente.value
        if b4:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM Clientes WHERE cedula = %s", (b4,))
                datos = cursor.fetchall()
                conexion.commit()
                cursor.close()
                conexion.close()
                if datos:
                    for i in datos:
                        clienteEncontrado = i[0]
                        display.value = "Si Existe Cliente, deseas Eliminarlo?"
                        eliminarCliente.disabled = False
                        eliminarCliente.on_click = lambda e: ejecutarEliminarCliente()
                        page.update()
                else:
                    display.value = "No Existe Cliente"
                    threading.Timer(3.0, limpiarDisplay).start()
                    page.update()
        else:
            buscarCliente.error_text = "Ingresa Cedula"
            page.update()

        page.update()

    def ejecutarEliminarCliente():
        global clienteEncontrado
        display.value = ""
        if clienteEncontrado:
            conexion = conectarBD()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM Clientes WHERE idCliente = %s", (clienteEncontrado,))
                conexion.commit()
                cursor.close()
                conexion.close()
                display.value = "Cliente Eliminado Correctamente"
                threading.Timer(3.0, limpiarDisplay).start()
                eliminarCliente.disabled = True
                buscarCliente.value = ""
                page.update()

        else:
            display.value = "No Existe Cliente"
            page.update()

        page.update()





    display = ft.Text(value="", col={"sm": 6}, size=20, text_align='center')
    buscarProducto = ft.TextField(hint_text="Buscar/Nombre Producto", width=300)
    buscarCliente = ft.TextField(hint_text="Buscar/Cedula Cliente", width=300)

    username = ft.TextField(hint_text="Username...", width=300)
    password = ft.TextField(hint_text="Password...", password=True, width=300)
    registrarse = ft.ElevatedButton(text='Registrarse', col={"sm": 3}, bgcolor=ft.colors.TEAL, color=ft.colors.BLACK, on_click=agregarLogin)
    actualizarContraseña = ft.ElevatedButton(text='Actualizar Contraseña', col={"sm": 6}, bgcolor=ft.colors.RED, color=ft.colors.BLACK, on_click=actualizarContraseña1, disabled=True)
    username2 = ft.TextField(hint_text="Username", width=300)
    nuevaContraseña = ft.TextField(hint_text="Nueva Contraseña", width=300, password=True, disabled=True)
    confirmarContraseña = ft.TextField(hint_text="Confirmar Contraseña", password=True, width=300, disabled=True)
    loginUsername = ft.TextField(width=300, hint_text='Ingresa Usuario')
    loginPassword = ft.TextField(width=300, hint_text='Ingresa Password', password=True)
    iniciarSesion = ft.ElevatedButton(text='Iniciar Sesion', col={"sm": 3}, bgcolor=ft.colors.TEAL, color=ft.colors.BLACK, on_click=hacerLogin)

    productoCrear = ft.TextField(hint_text="Producto", width=300)
    cantidadCrear = ft.TextField(hint_text="Cantidad", width=300)
    precioCrear = ft.TextField(hint_text="Precio", width=300)
    producto = ft.TextField(hint_text="Producto", width=300, disabled=True)
    cantidad = ft.TextField(hint_text="Cantidad", width=300, disabled=True)
    precio = ft.TextField(hint_text="Precio", width=300, disabled=True)
    
    clienteCrearNombre = ft.TextField(hint_text="Nombre", width=240)
    clienteCrearApellido = ft.TextField(hint_text="Apellido", width=240)
    clienteCrearCedula = ft.TextField(hint_text="Cedula", width=240)
    clienteCrearContacto = ft.TextField(hint_text="Contacto", width=240)
    clienteNombre = ft.TextField(hint_text="Nombre", width=240, disabled=True)
    clienteApellido = ft.TextField(hint_text="Apellido", width=240, disabled=True)
    clienteCedula = ft.TextField(hint_text="Cedula", width=240, disabled=True)
    clienteContacto = ft.TextField(hint_text="Contacto", width=240, disabled=True)
    crearCliente = ft.ElevatedButton(text='Crear Cliente', col={"sm": 3}, bgcolor=ft.colors.GREEN, color=ft.colors.BLACK, on_click=crearCliente1)

    crearProducto = ft.ElevatedButton(text='Crear Producto', col={"sm": 3}, bgcolor=ft.colors.BLUE, color=ft.colors.BLACK, on_click=crearProducto1)
    actualizarProducto = ft.ElevatedButton(text='Actualizar Producto', col={"sm": 3}, bgcolor=ft.colors.BLUE, color=ft.colors.BLACK, disabled=True)
    buscarProductoActualizar = ft.ElevatedButton(text='Buscar Producto', col={"sm": 3}, bgcolor=ft.colors.ORANGE, color=ft.colors.BLACK, on_click=buscarProducto1)
    buscarProductoEliminar = ft.ElevatedButton(text='Buscar Producto', col={"sm": 3}, bgcolor=ft.colors.ORANGE, color=ft.colors.BLACK, on_click=buscarProducto2)
    buscarUsuario = ft.ElevatedButton(text='Buscar Usuario', col={"sm": 3}, bgcolor=ft.colors.ORANGE, color=ft.colors.BLACK, on_click=buscarUsuario1)
    eliminarProducto = ft.ElevatedButton(text='Eliminar Producto', col={"sm": 3}, bgcolor=ft.colors.BLUE, color=ft.colors.BLACK, disabled=True)
    buscarClienteActualizar = ft.ElevatedButton(text='Buscar Cliente', col={"sm": 3}, bgcolor=ft.colors.ORANGE, color=ft.colors.BLACK, on_click=buscarCliente1)
    actualizarCliente = ft.ElevatedButton(text='Actualizar Cliente', col={"sm": 3}, bgcolor=ft.colors.GREEN, color=ft.colors.BLACK, disabled=True)
    buscarClienteEliminar = ft.ElevatedButton(text='Buscar Cliente', col={"sm": 3}, bgcolor=ft.colors.ORANGE, color=ft.colors.BLACK, on_click=buscarCliente2)
    eliminarCliente = ft.ElevatedButton(text='Eliminar Producto', col={"sm": 3}, bgcolor=ft.colors.GREEN, color=ft.colors.BLACK, disabled=True)
    
    page.on_route_change = cambio_ruta
    page.on_view_pop = vista_atras
    page.go(page.route)
    crearTabla()
    page.update()
    
    
ft.app(target=main, assets_dir='assets')