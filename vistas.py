import flet as ft
from flet import View, Page, AppBar, ElevatedButton, Text, RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment, TextField

def main (page : Page)-> None:
  
  page.title = "Mi Tienda"
  
  def route_change (e: RouteChangeEvent)-> None:
    
    page.views.clear()
    
    
    # Inicio
    
    page.views.append(
      
      View(
        
        route='/',
        controls=[
          AppBar(title=ft.Text('Inicio'), bgcolor=ft.colors.BLUE),
          Text(value='Inicio', size=30),
          ElevatedButton(text='Ir a Tienda', on_click=lambda _:page.go('/tienda')),
          TextField(label='Digita primer Numero', col={"sm": 4}) 
        ],
        
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
                
      )
  
    )
    
    # Tienda
    
    if page.route == '/tienda':
      
      page.views.append(
      
      View(
        
        route='/tienda',
        controls=[
          AppBar(title=ft.Text('Tienda'), bgcolor=ft.colors.RED),
          Text(value='Tienda', size=30),
          ElevatedButton(text='Regresar', on_click=lambda _:page.go('/')), 
        ],
        
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
                
      )
    )
    
    page.update()
    
  def view_pop(e: ViewPopEvent) -> None:
    
    page.views.pop()
    top_view: View = page.views[-1]
    page.go(top_view.route)
    
  page.on_route_change = route_change
  page.on_view_pop = view_pop
  page.go(page.route)
  

  
ft.app(target=main, view=ft.AppView.WEB_BROWSER)