from nicegui import ui
from nicegui_app.logic.app_state import get_state

def voice_library_tab(tab_object: ui.tab):
    app_state = get_state()

    with ui.tab_panel(tab_object).classes('p-0 m-0'):
        ui.label('Voice Library Content').classes('text-xl font-bold p-4')
        ui.label('Active Model: ') \
            .classes('text-base p-4 inline') \
            .bind_text_from(app_state, 'active_model', 
                            backward=lambda model: f'Aktywny Model: {model}')