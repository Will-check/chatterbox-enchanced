from nicegui import app

# A class to hold shared application state
class AppState:
    def __init__(self):
        # Add here everything that should be shared across the application
        self.model = ''

# Initialize the global state instance
app.storage.general['app_state'] = AppState()

def get_state() -> AppState:
    return app.storage.general['app_state']