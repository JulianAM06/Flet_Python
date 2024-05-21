import flet as ft

def main(page):

    def click (e):
        
        if not texto.value:
            
            texto.error_text = 'Por favor ingresa tu Nombre'
            page.update()
            
        else:
            
            name = texto.value
            page.clean()
            page.add(ft.Text(f"Hola... {name}"))
            
    
    texto = ft.TextField(label='Nombre')
    
    page.add(
        
        texto,
        ft.ElevatedButton("Saludar", on_click=click),
        
        
    )
    

ft.app(target=main)