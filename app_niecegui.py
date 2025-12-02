from nicegui import ui
from nicegui_app.ui.tabs.single_generation_tab import single_generation_tab
from nicegui_app.ui.tabs.voice_library_tab import voice_library_tab
from nicegui_app.ui.tabs.audiobook_creation_tab import audiobook_creation_tab

with ui.column().classes('w-full px-5 gap-5'):
    
    # 1. Header Section
    with ui.row().classes('w-full bg-gray-800 justify-center py-10 shadow-lg'):
        with ui.column().classes('items-center gap-0'):
                title_html = """
                <span class="text-6xl font-extrabold" 
                    style="background-image: linear-gradient(to right, #00BFFF, #8A2BE2); 
                           -webkit-background-clip: text; 
                           -webkit-text-fill-color: transparent;">
                    AI Voice Studio
                </span>
                """
                ui.html(title_html, sanitize=False).classes('pb-2') 

                # Subtitle
                ui.label('Transforming Text into Expressive Audio').classes('text-lg text-gray-300 font-light')

    # 2. Navigation Tabs
    with ui.tabs().classes('w-full text-gray-700 border-b border-gray-300') \
            .props('active-color=orange indicator-color=orange align=left inline-label') as tabs:
        
        tab_gen = ui.tab('Single Generation', icon='mic')
        tab_lib = ui.tab('Voice Library', icon='library_books')
        tab_audio = ui.tab('Audiobook Creation', icon='menu_book')

    # 3. Content Panels
    with ui.tab_panels(tabs, value=tab_gen).classes('w-full'):
        single_generation_tab(tab_gen)
        voice_library_tab(tab_lib)
        audiobook_creation_tab(tab_audio)

ui.run(title='Text To Speech Interface')