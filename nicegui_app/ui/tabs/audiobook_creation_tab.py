from nicegui import ui

def audiobook_creation_tab(tab_object: ui.tab):
    with ui.tab_panel(tab_object).classes('p-0 m-0'):
        ui.label('Audiobook Creation Content').classes('text-xl font-bold p-4')