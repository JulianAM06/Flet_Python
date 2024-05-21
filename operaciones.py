import flet as ft

def main(page:ft.Page):
    
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
       

    valor1 = ft.TextField(width=250, label='Digita primer Numero')

    valor2 = ft.TextField(width=250, label='Digita segundo Numero')
    
    operacion = ft.Dropdown(
        width=150,
        label='Operacion',
        options=[
            ft.dropdown.Option("+"),
            ft.dropdown.Option("-"),
            ft.dropdown.Option("*"),
            ft.dropdown.Option("/"),
            
        ],
    )

    igual = ft.ElevatedButton(text="=", on_click = resultado)
    
    txtresultado = ft.TextField(width=250, label='Resultado')
    
    
    page.add(
        ft.Row(
            [
                valor1,
                operacion,
                valor2,
                igual,
                txtresultado
         
            ]
        )
    )
    
    page.update()
    
ft.app(target=main)

