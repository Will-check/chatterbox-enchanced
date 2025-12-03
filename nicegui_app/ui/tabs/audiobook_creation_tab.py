from nicegui import ui
import re

def detect_speakers(textarea_ref: ui.textarea, speaker_list_container: ui.column, results_container: ui.column, voice_options: list):
    script = textarea_ref.value
    # Regex to find text inside brackets at the start of a line, e.g., [SpeakerName]
    speaker_tags = set(re.findall(r'^\s*\[([A-Za-z0-9\s]+)\]', script, re.MULTILINE))
    
    new_speakers = {}
    
    for tag in sorted(list(speaker_tags)):
        normalized_tag = tag.capitalize() 
        new_speakers[normalized_tag] = ''

    speaker_list_container.clear()
    
    if new_speakers:
        results_container.set_visibility(True)
        with speaker_list_container:
            for speaker, default_voice in new_speakers.items():
                speaker_row(speaker, voice_options, default_voice)
    else:
        results_container.set_visibility(False)
    
    results_container.update()
    speaker_list_container.update()
    ui.notify(f'Detected {len(new_speakers)} speakers.', type='positive')

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
    voice_options = ['','Voice A (M)', 'Voice B (F)', 'Voice C (Child)']
    
    initial_speakers = {}

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
                        text_input = ui.textarea(
                            value='[Narrator] In a dark forest, full of mysteries, stood a small house.\n \
[Alice] Is this where the forest sprite lives?\n \
[Boris] I don\'t think so. Let\'s ask.\n \
[NARRATOR] Suddenly, a quiet rustle was heard\n. \
[Alice] Who is there?\n \
[Alice2] Is this where the forest sprite lives?\n \
[Boris2] I don\'t think so. Let\'s ask.\n \
[NARRATOR2] Suddenly, a quiet rustle was heard\n. \
[Alice2] Who is there?',  
                            placeholder='Enter text here...',
                        ).classes('w-full').props('rows=20 outlined dense')
                        
                # --- Right Column: Speakers & Voices 
                with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-4'):
                    with ui.card().classes('w-full p-4 border border-gray-200 rounded-xl shadow-none gap-4'):
                        ui.button('Detect Speakers', 
                                    on_click=lambda: detect_speakers(text_input, speaker_list_container, results_container, voice_options)
                                ).classes('w-full h-10 font-bold text-sm rounded-lg shadow-md') \
                                    .props('color=indigo')
                        
                        speaker_row('Single voice', voice_options, '')

                        results_container = ui.column().classes('w-full gap-2')
                        results_container.clear()
                        results_container.set_visibility(False)
                        
                        with results_container:
                            ui.label('Speakers list:').classes('font-semibold text-gray-700 mt-4')
                            
                            with ui.scroll_area().classes('w-full h-64 border border-gray-200 rounded-md p-2'):
                                speaker_list_container = ui.column().classes('w-full gap-2')