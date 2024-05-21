import flet as ft

def main (page):
    
    texto = ft.Text (value='Hola soy Matias', size='60', color='white', bgcolor='black', weight='bold', italic=True)
    
    page.add (texto)
    
ft.app(target=main)