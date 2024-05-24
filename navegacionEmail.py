import flet as ft

def main (page: ft.Page):
    
    page.title = "Navegacion"
    email = ft.TextField(hint_text="Ingresa Email...", width=300)
    password = ft.TextField(hint_text="Ingresa Password...", password=True, width=300)
    
    def cambio_ruta (route):
        page.views.clear
        page.views.append(
            
            ft.View(
                "/",
                [
                ft.AppBar(title=ft.Text('Inicio'), bgcolor=ft.colors.CYAN),
                ft.Container(height=100),
                email,
                password, 
                ft.ElevatedButton('Login', on_click= ingresar)
                ], 
                scroll="always",
                vertical_alignment="center",
                horizontal_alignment="center"     
            )
        )
        
        if page.route == "/hola":
            
            page.views.append(
                ft.View(
                    "/hola",
                    [
                    ft.AppBar(title=ft.Text("Hola"), bgcolor=ft.colors.RED),
                    ft.Row([ft.Image(src="assets/pizza1.png"), ft.Image(src="assets/pizza1.png")], alignment="center"),
                    ft.Container(height=50),
                    ft.Row([ft.ElevatedButton("Regresar Inicio", on_click=lambda _:page.go("/")), ft.Container(width=50),ft.ElevatedButton("Ir Tienda", on_click=lambda _:page.go("/hola/tienda"))], alignment="center"),
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center" 
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
        
    def ingresar(e):
        email.error_text = ""
        password.error_text = ""
        
        if not email.value:
            email.error_text = "Ingresa Email"  
        
        elif not password.value:
            password.error_text = "Ingresa Password"  
            
        else:
            page.go("/hola")
            
        page.update()
    
    page.on_route_change = cambio_ruta
    page.on_view_pop = vista_atras
    page.go(page.route)
    
ft.app(target=main, assets_dir='assets')