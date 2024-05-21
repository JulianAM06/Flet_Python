import flet as ft

def main(page: ft.Page):
    
    # Forma 1 
    datos = ft.Row(controls=[ft.Text('Python'), ft.Text('Flutter'), ft.Text('Flet')])
    
    page.add(datos)
    
    
    # Forma 2
    page.add(
    ft.Row(controls=[
        ft.Text("Python"),
        ft.Text("Flutter"),
        ft.Text("Flet")
    ])
)
    
    # Forma 3
    lenguajes = ['Python','Flutter', 'Flet']
    etiquetas = []
    
    for i in lenguajes:
        
        etiquetas.append(ft.Text(i))
        
    datos = ft.Row(controls=etiquetas)
    
    page.add(datos)
    
# De las tres maneras anteriores se pueden poder diferentes textos en Fila
    
ft.app(target=main)