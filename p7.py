import flet as ft 

def main(page):
    
    nombre = ft.TextField(width=300, hint_text='Ingresa tu Nombre') # Hint_Text es un Placeholder
    apellido = ft.TextField(width=300, hint_text='Ingresa tu Apellido') # Hint_Text es un Placeholder
    
    # Para deshabilitar el campo individualmente
    
    #nombre.disabled = True
    #apellido.disabled = True
    
    c = ft.Column(controls=[nombre,apellido])
    
    # Para deshabilitar el campo grupal
    
    # c.disabled = True
    
    page.add(c)
    
ft.app(target=main)