import flet as ft

def main(page:ft.Page):
    
    page.title = "Conversion Moneda"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 400
    
    def reset (e):
        
        n1.value = ""
        n2.value = ""
        resultado.value = ""
        valor.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("La Calculadora se ha Reseteado"))
        page.snack_bar.open = True
        page.update()
    
    page.floating_action_button = ft.FloatingActionButton(
        
        icon=ft.icons.RESTORE, on_click=reset
    )
    
    def cambio(e):
        
        if n1.value == "EURO" and n2.value == "DOLAR":
            resultado.value = str(int(valor.value) * 1.07)
            page.update()
            
        elif n1.value == "EURO" and n2.value == "PESO":
            resultado.value = str(int(valor.value) * 4324.27)
            page.update()
        
        elif n1.value == "DOLAR" and n2.value == "EURO":
            resultado.value = str(int(valor.value) * 0.94)
            page.update()
            
        elif n1.value == "DOLAR" and n2.value == "PESO":
            resultado.value = str(int(valor.value) * 4038.50)
            page.update()
            
        elif n1.value == "PESO" and n2.value == "EURO":
            resultado.value = str(int(valor.value) * 0.00023)
            page.update()
            
        elif n1.value == "PESO" and n2.value == "DOLAR":
            resultado.value = str(int(valor.value) * 0.00025)
            page.update() 
    
    n1 = ft.Dropdown(label="Moneda Inicial", border_color=ft.colors.TEAL, width=300, options=[
        
        ft.dropdown.Option("EURO"),
        ft.dropdown.Option("DOLAR"),
        ft.dropdown.Option("PESO"),
        
    ])
    
    valor = ft.TextField(label="Ingresa Valor", border_color=ft.colors.RED, width=300)
    
    n2 = ft.Dropdown(label="Moneda Final", border_color=ft.colors.TEAL, width=300, options=[
        
        ft.dropdown.Option("EURO"),
        ft.dropdown.Option("DOLAR"),
        ft.dropdown.Option("PESO"),
        
    ])
    
    conversion = ft.IconButton(icon=ft.icons.PRICE_CHANGE, icon_size=50, on_click=cambio)
    
    resultado = ft.TextField(label="Resultado", width=300, border_color=ft.colors.BLUE)
    
    page.add(
        n1,
        valor,
        n2,
        conversion,
        resultado
    )
    
    page.update()
    
ft.app(target=main)