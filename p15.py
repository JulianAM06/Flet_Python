# Librearias para el codigo
import flet as ft
import threading

# Funcion Principal del Proyecto
def main (page: ft.Page):
    
    # Configuraciones Iniciales para estructura del Proyecto
    page.title = 'Sistema Seguridad' # Titulo de la Pagina
    page.padding = 30 # Margen interna 
    page.bgcolor = ft.colors.BLACK # Color de Fondo
    page.theme_mode = 'dark' # Modo Oscuro
    page.scroll = 'always' # Scroll para la pagina
    page.window_width = 800  # Ancho de la ventana
    page.window_height = 500  # Alto de la ventana
    page.update()

    # Listas para almacenamiento de Clave Generada y Validacion de Clave
    claveNueva = []
    validarClave = []
    
    # Funcion para la Limpieza del Display (Proyeccion de Mensajes)
    def limpiarDisplay():
        display.value = "" # Vacia el display
        page.update()
    
    # Funcion que nos permite mostrar los valores en el Display, hacer validaciones para almacenar Clave Generada y Clave a Validar
    def mostrarValor(e):
        display.size = 18 # Tamaño del numero en el display
        valor = str(e.control.data)  # Convertir a cadena para asegurar la comparación
        display.value = valor # Mostrar valor en el display

        if generar.disabled: # Valida si el boton Generar cambia de estado
            claveNueva.append(valor) # Ingresa los valores a la lista claveNueva
            if len(claveNueva) == 4 : # Validacion de la longitud de la lista == 4
                display.value = "Clave Guardada Exitosamente" # Muestra mensaje en el display
                threading.Timer(3.0, limpiarDisplay).start() # Cuenta 2 segundos y limpia el display 
                aceptar.disabled = False # Cambia de estado el boton Aceptar
    
            elif not aceptar.disabled: # Validacion de un estado en False  
                    validarClave.append(valor) # Ingresamos valores a la lista validarClave
                    if len(validarClave) == 4: # Validacion de la longitud de la lista == 4
                        display.value = "Clave completa, presiona Aceptar para validar." # Muestra mensaje en el display
                        threading.Timer(3.0, limpiarDisplay).start() # Cuenta 2 segundos y limpia el display 
        page.update()

    # Funcion que nos permite comparar la Clave Generada con la Clave a Validar
    def validar(e):
       
        if validarClave[0] == claveNueva [0] and validarClave[1] == claveNueva[1] and validarClave[2] == claveNueva[2] and validarClave[3] == claveNueva[3]: # Validamos posicion por posicion de cada lista

            display.value = "Acceso Permitido" # Mostramos mensaje en el Display
            aceptar.disabled = True

        else:

            display.value = "Acceso Denegado" # Mostramos mensaje en le Display
            validarClave.clear() # Si la claves no son iguales, limpiamos la lista validarClacve para ingresar una nueva
                            
        page.update()
        threading.Timer(3.0, limpiarDisplay).start()

    # Funcion que nos permite darle la funcionalidad al momento de dar click en el Boton Generar
    def mostrarMensajeGenerar(e):
        mensaje = e.control.data # Variable mensaje alamcena el valor que tiene como data
        display.size = 18 # Tamaño letra para el display
        display.value = mensaje # Le paso lo almacenado en mensaje para que se vea en el display
        generar.disabled = True # Desibilitar el boton Generar
        page.update()
        threading.Timer(3.0, limpiarDisplay).start()

    # Creacion del display, botones numericos, boton Generar y Aceptar. Tambien sus caracteristicas visuales(Front)
    display = ft.Text(value="", col={"sm": 6}, size=30, text_align='center')
    
    siete = ft.ElevatedButton(text='7', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=7, on_click=mostrarValor)
    
    ocho = ft.ElevatedButton(text='8', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=8, on_click=mostrarValor)
    
    nueve = ft.ElevatedButton(text='9', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=9, on_click=mostrarValor)
    
    cuatro = ft.ElevatedButton(text='4', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=4, on_click=mostrarValor)
    
    cinco = ft.ElevatedButton(text='5', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=5, on_click=mostrarValor)
    
    seis = ft.ElevatedButton(text='6', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=6, on_click=mostrarValor)
    
    uno = ft.ElevatedButton(text='1', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=1, on_click=mostrarValor)
    
    dos = ft.ElevatedButton(text='2', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=2, on_click=mostrarValor)
    
    tres = ft.ElevatedButton(text='3', col={"sm": 2}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=3, on_click=mostrarValor)
    
    cero = ft.ElevatedButton(text='0', col={"sm": 6}, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, data=0, on_click=mostrarValor)
    
    generar = ft.ElevatedButton(text='Generar', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK, data="Bienvenido al Sistema de Seguridad, ingresa clave de 4 digitos", on_click=mostrarMensajeGenerar)

    aceptar = ft.ElevatedButton(text='Aceptar', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK, disabled=True, on_click=validar)
    
    # Diseño de columnas y filas para acomodar display y botones
    page.add(
        ft.ResponsiveRow(
            controls=[display], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[uno, dos, tres], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[cuatro, cinco, seis], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[siete, ocho, nueve], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[cero], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ResponsiveRow(
            controls=[generar, aceptar], alignment=ft.MainAxisAlignment.CENTER
        ),
        
    )

# Funcion para correr el programa    
ft.app(target=main)