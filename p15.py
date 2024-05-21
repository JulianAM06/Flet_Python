import flet as ft

def main (page: ft.Page):
    
    page.title = 'Sistema Seguridad' # Titulo de la Pagina
    page.padding = 30 # Margen interna 
    page.bgcolor = ft.colors.BLACK # Color de Fondo
    page.theme_mode = 'dark'
    page.scroll = 'always' # Scroll para la pagina
    page.update()

    def mostrarValor(e):
        valor = e.control.data
        display.value = valor
        page.update()
     
    
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
    
    generar = ft.ElevatedButton(text='Generar', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK)

    aceptar = ft.ElevatedButton(text='Aceptar', col={"sm": 3}, bgcolor=ft.colors.CYAN, color=ft.colors.BLACK)
    
    page.add(
        ft.ResponsiveRow(
            controls=[display]
        ),
        ft.ResponsiveRow(
            controls=[uno, dos, tres]
        ),
        ft.ResponsiveRow(
            controls=[cuatro, cinco, seis]
        ),
        ft.ResponsiveRow(
            controls=[siete, ocho, nueve]
        ),
        ft.ResponsiveRow(
            controls=[cero]
        ),
        ft.ResponsiveRow(
            controls=[generar, aceptar]
        ),
        
    )
    
ft.app(target=main)