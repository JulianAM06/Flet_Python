import flet as ft

def main(page:ft.Page):
    
    page.add(ft.Text(f"Ruta Inicial: {page.route}"))
    
    def cambio_ruta(ruta):
        
        page.add(ft.Text(f"Nueva Ruta: {page.route}"))
        page.update()
    
    def tienda(e):
        
        page.route = "/tienda"
        page.update()   
        
    
    page.on_route_change = cambio_ruta
    
    page.add(ft.ElevatedButton('Ir a Tienda', on_click=tienda))
    
   

ft.app(target=main, view=ft.AppView.WEB_BROWSER ,assets_dir='assets')