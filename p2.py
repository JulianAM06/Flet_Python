import flet as ft


def main (page: ft.Page):
    
    t = ft.Text(value='Hola Mundo', color='green')
    page.controls.append(t)
    page.update()
    
ft.app(target=main)