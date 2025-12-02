from nicegui import app
from nicegui import ui 

# A class to hold shared application state
class AppState:
    def __init__(self):
        # Add here everything that should be shared across the application
        self.model = ''

    def set_active_model(self, model_name: str | None) -> None:
        self.active_model = model_name if model_name else None
        
        ui.notify(f'Active model set to: {self.active_model}', type='info', timeout=1500)
        
# Initialize the global state instance
app.storage.general['app_state'] = AppState()

def get_state() -> AppState:
    return app.storage.general['app_state']

