import flet as ft

def main(page: ft.Page):
    
    def reset (e):
        
        valor1.value = ""
        valor2.value = ""
        txtresultado.value = ""
        operacion.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("La Calculadora se ha Reseteado"))
        page.snack_bar.open = True
        page.update()
    
    page.floating_action_button = ft.FloatingActionButton(
        
        icon=ft.icons.RESTORE, on_click=reset
    )
    
    def resultado(e):
        
        if operacion.value == "+":
            txtresultado.value = str(int(valor1.value) + int(valor2.value))
            page.update()
            
        elif operacion.value == "-":
            txtresultado.value = str(int(valor1.value) - int(valor2.value))
            page.update()
        
        elif operacion.value == "*":
            txtresultado.value = str(int(valor1.value) * int(valor2.value))
            page.update()
            
        elif operacion.value == "/":
            txtresultado.value = str(int(valor1.value) / int(valor2.value))
            page.update()
    
    valor1 = ft.TextField(label='Digita primer Numero', col={"sm": 4})
    
    operacion = ft.Dropdown(label='Operacion', col={"sm": 2.5}, options=[
            ft.dropdown.Option("+"),
            ft.dropdown.Option("-"),
            ft.dropdown.Option("*"),
            ft.dropdown.Option("/"),
            ])  
    
    valor2 = ft.TextField(label='Digita segundo Numero', col={"sm": 4})
    
    igual = ft.ElevatedButton(text="=", on_click = resultado, col={"sm": 1.5})
    
    txtresultado = ft.TextField(label='Resultado', col={"sm": 12})
    
    page.add(
       ft.ResponsiveRow([
            
            valor1,
            operacion,
            valor2,
            igual,
             
        ]),
       
       ft.ResponsiveRow([
           
           txtresultado
            
       ])
    )
    page.update()
   

ft.app(target=main)