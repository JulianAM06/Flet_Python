import flet as ft

def main(page:ft.Page):

    def resultado(e):
        txtresultado.value = str(int(valor1.value) + int(valor2.value))
        page.update()

    valor1 = ft.TextField(width=250, label='Digita primer Numero')
    
    suma = ft.Text(value='+')

    valor2 = ft.TextField(width=250, label='Digita segundo Numero')

    igual = ft.ElevatedButton(text="=", on_click = resultado)
    
    txtresultado = ft.TextField(width=250, label='Resultado')
    
    
    
    page.add(
        ft.Row(
            [
                valor1,
                valor2,
                suma,
                igual,
                txtresultado
            ]
        )
    )
    page.update()
    
ft.app(target=main)

