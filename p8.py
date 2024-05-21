import flet as ft 

def main (page):
    
    nombre = ft.TextField(label="Campo Nombre", width=500, autofocus=True)
    apellido = ft.TextField(label="Campo Apellido", width=500)
    columna = ft.Column()
    
    def btnClick(e):
        
        columna.controls.append(ft.Text(f'¡Hola {nombre.value} {apellido.value}!'))
        nombre.value = ""
        apellido.value = ""
        page.update()
        nombre.focus()
    
    page.add(
        nombre,
        apellido,
        ft.ElevatedButton('Saludar', on_click=btnClick),
        columna,
    )
    
ft.app(target=main)