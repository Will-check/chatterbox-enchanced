from nicegui import ui
import re

def detect_speakers(textarea_ref: ui.textarea,
                    speaker_list_container: ui.column,
                    results_container: ui.column,
                    voice_options: list,
                    single_voice_select: ui.select):
    script = textarea_ref.value
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
                speaker_row(
                    speaker, voice_options, default_voice, 
                    list_container=speaker_list_container, 
                    single_voice_select=single_voice_select, 
                    results_container=results_container
                )
        single_voice_select.disable()
    else:
        results_container.set_visibility(False)
        single_voice_select.enable()
    
    results_container.update()
    speaker_list_container.update()
    ui.notify(f'Detected {len(new_speakers)} speakers.', type='positive')

def reset_speakers(speaker_list_container: ui.column,
                   single_voice_select: ui.select,
                   results_container: ui.column):
    speaker_list_container.clear()
    speaker_list_container.update()
    single_voice_select.enable()
    results_container.set_visibility(False)
    results_container.update()

def remove_speaker(row_to_remove: ui.row, list_container: ui.column, single_voice_select: ui.select, results_container: ui.column):
    row_to_remove.delete()
    list_container.update()
    
    if not list_container.default_slot.children:
        reset_speakers(list_container, single_voice_select, results_container)

def speaker_row(speaker_name: str,
                voice_options: list,
                default_voice: str,
                label_classes: str = '',
                list_container: ui.column = None,
                single_voice_select: ui.select = None,
                results_container: ui.column = None):
    with ui.row().classes('w-full items-center justify-between gap-2') as row_container:
        if list_container is not None:
            ui.button('X', on_click=lambda: remove_speaker(
                row_container, list_container, single_voice_select, results_container
            )).classes('h-8 w-8 p-0 flex-shrink-0').props('color=red flat round')

        default_label_classes = 'font-medium text-gray-700 w-24 truncate'
        ui.label(speaker_name).classes(default_label_classes if not label_classes else label_classes)
        
        row = ui.select(
            options=voice_options, 
            value=default_voice, 
            label='Select Voice'
        ).classes('flex-grow').props('outlined dense color=indigo')

    return row

def audiobook_creation_tab(tab_object: ui.tab):
    voice_options = ['','Voice A (M)', 'Voice B (F)', 'Voice C (Child)']
    
    initial_speakers = {}

    with ui.tab_panel(tab_object).classes('p-0 m-0 w-full'):
        with ui.column().classes('w-full p-6 gap-6'):
            with ui.row().classes('w-full p-4 border border-gray-200 rounded-xl shadow-md gap-4 items-center'):
                ui.label('Project:').classes('font-semibold text-gray-700')
                ui.input(
                    value='', 
                    label='Select folder / project name'
                ).classes('flex-grow').props('outlined dense color=indigo')

            with ui.row().classes('w-full gap-6 flex flex-wrap justify-start'):
                with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-4'):
                    with ui.card().classes('w-full h-[460px] p-4 border border-gray-200 rounded-xl shadow-none'):
                        ui.label('Text to synthesize').classes('font-semibold text-gray-700 w-full text-center')
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
                        ).classes('w-full h-full').props('rows=20 outlined dense resize-none')
                        
                with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-4'):
                    with ui.card().classes('w-full h-[460px] p-4 border border-gray-200 rounded-xl shadow-none gap-4'):
                        ui.button('Detect Speakers', 
                                    on_click=lambda: detect_speakers(text_input, speaker_list_container, results_container, voice_options, single_voice_select)
                                ).classes('w-full h-10 font-bold text-sm rounded-lg shadow-md') \
                                    .props('color=indigo')
                        
                        single_voice_select = speaker_row('Single voice', voice_options, '', 'font-semibold text-gray-700 w-26 truncate')

                        results_container = ui.column().classes('w-full gap-2')
                        results_container.clear()
                        results_container.set_visibility(False)
                        
                        with results_container:
                            ui.label('Speaker list').classes('font-semibold text-gray-700 mt-4 w-full text-center')
                            
                            with ui.scroll_area().classes('w-full h-52 border border-gray-200 rounded-md p-2'):
                                speaker_list_container = ui.column().classes('w-full gap-1')
                            ui.button('Remove speakers', 
                                on_click=lambda: reset_speakers(speaker_list_container, single_voice_select, results_container),
                            ).classes('w-full mt-2').props('color=red')

            with ui.row().classes('w-full justify-center gap-4 pt-4'):
                ui.label('Output Audio').classes('font-semibold text-gray-700')
                ui.audio('').classes('w-full')


            with ui.row().classes('w-full justify-center gap-4 pt-4'):
                ui.button('Create audio parts', on_click=lambda: ui.notify('Create audio parts - not implemented yet!')) \
                    .classes('flex-grow h-12 font-bold text-base rounded-lg shadow-md') \
                    .props('color=indigo')
                ui.button('Merge audio parts', on_click=lambda:  ui.notify('Merge audio parts - not implemented yet!')) \
                    .classes('flex-grow h-12 font-bold text-base rounded-lg shadow-md') \
                    .props('color=indigo')