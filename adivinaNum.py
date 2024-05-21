import flet as ft
from random import randint

def main (page: ft.Page):
    
    page.title = 'Adivina Numero'
    page.padding = 50
     
    respuesta = randint(1, 10)
        
        
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "fonts/OpenSans-Regular.ttf",
    }
    
    def reset (e):
        
        num1.value = ""
        num2.value = ""
        resultado.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("El Juego se ha Reseteado"))
        page.snack_bar.open = True
        page.update()
    
    page.floating_action_button = ft.FloatingActionButton(
        
        icon=ft.icons.RESTORE, on_click=reset
    )
    
    num1 = ft.TextField(label='Jugador 1', border_radius=20, border_width=2, border_color=ft.colors.CYAN, col={"sm": 4})
    
    num2 = ft.TextField(label='Jugador 2', border_radius=20, border_width=2, border_color=ft.colors.CYAN, col={"sm": 4})
    
    
    resultado = ft.TextField(width=300, border_radius=20, border_width=2, border_color=ft.colors.CYAN, label='Verificar', col={"sm": 7})
    
    def verificar_numero_n1(e):
        
        if int(num1.value) > respuesta:
            resultado.value = "El numero es Menor"
            
        elif int(num1.value) < respuesta:
            resultado.value = "El numero es Mayor"
        
        elif int(num1.value) == respuesta:
            resultado.value ="Jugador 1...Adivinaste!!! :)"
            
        else:
            resultado.value ="Hay un error :("
            
        page.update()
    
    def verificar_numero_n2(e):
        
        if int(num2.value) > respuesta:
            resultado.value = "El numero es Menor"
            
        elif int(num2.value) < respuesta:
            resultado.value = "El numero es Mayor"
        
        elif int(num2.value) == respuesta:
            resultado.value ="Jugador 2...Adivinaste!!! :)"
            
        else:
            resultado.value ="Hay un error :("
            
        page.update()
    
    
    checkN1 = ft.ElevatedButton("Jugador 1", on_click=verificar_numero_n1, col={"sm": 3})
    
    checkN2 = ft.ElevatedButton("Jugador 2", on_click=verificar_numero_n2, col={"sm": 3})
    
    
    page.add(
        
        ft.Card(
            
            ft.Container(
            
            content = ft.Row(
            
            controls=[ft.Text(value='Adivina Numero', font_family="Kanit", size=30)],  
            ),
            padding= 30
          )
               
        ),
        
        ft.ResponsiveRow([
                
            num1, 
            checkN1,
            
            ]),
        
        ft.ResponsiveRow([
                
            num2, 
            checkN2,
            
            ]),
        
         ft.ResponsiveRow([
                
            resultado
            
            ]),
                
    )
    
ft.app(target=main)