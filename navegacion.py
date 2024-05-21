import flet as ft

def main (page: ft.Page):
    
    page.title = "Navegacion"
    
    def cambio_ruta (route):
        page.views.clear
        page.views.append(
            
            ft.View(
                "/",
                [ft.AppBar(title=ft.Text('Inicio'), bgcolor=ft.colors.CYAN), 
                 ft.ElevatedButton('Ir a Hola', on_click= lambda _: page.go("/hola"))
                ]     
            )
        )
        
        if page.route == "/hola":
            
            page.views.append(
                ft.View(
                    "/hola",
                    [
                    ft.AppBar(title=ft.Text("Hola"), bgcolor=ft.colors.RED),
                    ft.ElevatedButton("Regresar Inicio", on_click=lambda _:page.go("/")),
                    ft.ElevatedButton("Ir Tienda", on_click=lambda _:page.go("/hola/tienda"))
                    ]
                )
            )
            
        if page.route == "/hola/tienda":
            
            page.views.append(
                ft.View(
                    "/tienda",
                    [
                    ft.AppBar(title=ft.Text("Tienda"), bgcolor=ft.colors.TEAL),
                    ft.ElevatedButton("Regresar Hola", on_click=lambda _:page.go("/hola"))
                    ]
                )
            )
        page.update()
        
    
    def vista_atras(view):
        
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
        
    
    page.on_route_change = cambio_ruta
    page.on_view_pop = vista_atras
    page.go(page.route)
    
ft.app(target=main, assets_dir='assets')