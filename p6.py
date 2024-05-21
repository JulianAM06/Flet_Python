import flet as ft

def main(page):
    def adicionar_tarea_click(e):
        page.add(ft.Checkbox(label=nuevaTarea.value))
        nuevaTarea.value = ""
        nuevaTarea.focus()
        nuevaTarea.update()

    nuevaTarea = ft.TextField(hint_text="Cual tarea deseas Agragar?", width=500)
    page.add(ft.Row([nuevaTarea, ft.ElevatedButton("Adicionar", on_click=adicionar_tarea_click)]))

ft.app(target=main)