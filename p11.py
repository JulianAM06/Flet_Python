import flet as ft

def main (page):
    
    btn = ft.ElevatedButton('Click')
    
    page.add(btn)
    
ft.app(target=main)