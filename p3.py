import flet as ft
import time


def main(page: ft.Page):
    
    t = ft.Text(color='red')
    page.add(t)
    
    for i in range(0, 10):
        t.value = f"Segundo {i}"
        page.update()
        time.sleep(1)
        
ft.app(target=main,view=ft.AppView.WEB_BROWSER)