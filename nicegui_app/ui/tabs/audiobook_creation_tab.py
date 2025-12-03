from nicegui import ui

# Helper function to create a speaker row for the Speakers list
def speaker_row(speaker_name: str, voice_options: list, default_voice: str):
    with ui.row().classes('w-full items-center justify-between gap-2'):
        ui.label(speaker_name).classes('font-medium text-gray-700 w-1/4 truncate')
        
        ui.select(
            options=voice_options, 
            value=default_voice, 
            label='Select Voice'
        ).classes('w-3/4').props('outlined dense color=indigo')

def audiobook_creation_tab(tab_object: ui.tab):
    voice_options = ['Voice A (M)', 'Voice B (F)', 'Voice C (Child)']
    
    initial_speakers = {
        'Narrator': 'Voice A (M)',
        'Alina': 'Voice B (F)',
        'Tomek': 'Voice A (M)',
        'Basia': 'Voice C (Child)',
    }
    
    with ui.tab_panel(tab_object).classes('p-0 m-0 w-full'):
        with ui.column().classes('w-full p-6 gap-6'):
            with ui.row().classes('w-full p-4 border border-gray-200 rounded-xl shadow-md gap-4 items-center'):
                ui.label('Project:').classes('font-semibold text-gray-700 text-lg')
                ui.input(
                    value='', 
                    label='Select folder / project name'
                ).classes('flex-grow').props('outlined dense color=indigo')

            with ui.row().classes('w-full gap-6 flex flex-wrap justify-start'):
                # --- Left Column: Text 
                with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-4'):
                    with ui.card().classes('w-full p-4 border border-gray-200 rounded-xl shadow-none'):
                        ui.label('Text to synthesize').classes('font-semibold text-gray-700')
                        ui.textarea(
                            placeholder='Enter text here...',
                        ).classes('w-full').props('rows=20 outlined dense')
                        
                # --- Right Column: Speakers & Voices 
                with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-4'):
                    with ui.card().classes('w-full p-4 border border-gray-200 rounded-xl shadow-none gap-4'):
                        with ui.row().classes('w-full gap-4'):
                            with ui.column().classes('w-1/2 flex-grow pr-4 border-r border-gray-200'):
                                ui.button('Detect Speakers', 
                                          on_click=lambda: ui.notify('Initializing speaker detection...', type='info')
                                        ).classes('w-full h-10 font-bold text-sm rounded-lg shadow-md') \
                                         .props('color=indigo')
                                
                                speaker_row('Narrator', voice_options, initial_speakers['Narrator'])
                                ui.label('Speakers list:').classes('font-semibold text-gray-700 mt-4')
                                
                                with ui.column().classes('w-full gap-2'):
                                    for speaker, default_voice in initial_speakers.items():
                                        if speaker != 'Narrator':
                                            speaker_row(speaker, voice_options, default_voice)