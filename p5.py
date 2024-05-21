import flet as ft



def main(page: ft.Page):
    
    text = ft.TextField(label='Digita tu Nombre')
    
    saludo = ft.Text()
    
    def saludar (e):
        
        saludo.value = f'Hola...{text.value}'
        page.update()
    
    entrada = ft.Row(controls=[
        text, 
        ft.ElevatedButton(text='Saludar', on_click=saludar),
        saludo
    
    ])
    
    page.add(entrada)
    
ft.app(target=main)