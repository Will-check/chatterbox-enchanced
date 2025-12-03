from nicegui import ui
from nicegui_app.ui.common import handle_file_upload

def single_generation_tab(tab_object: ui.tab):
    with ui.tab_panel(tab_object).classes('p-0 m-0 w-full'):
        with ui.row().classes('w-full p-6 gap-6 flex flex-wrap justify-start'):
            # --- Left Column: Controls
            with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-6'):
                # 1. Voice Profile, Reference Audio, and Sliders
                with ui.column().classes('w-full p-4 border border-gray-200 rounded-xl gap-6'):
                    ui.label('Saved Voice Profiles').classes('font-semibold text-gray-700')
                    ui.select(options=['Profile 1', 'Profile 2', 'Default'], value='Default', label='Select Profile') \
                        .classes('w-full mb-4').props('outlined dense')

                    ui.label('Reference Audio').classes('font-semibold text-gray-700')
                    
                    # DYNAMIC REFERENCE AUDIO SECTION
                    with ui.column().classes('w-full relative'):
                        # 1. Upload Component (Visible initially)
                        upload_component = ui.upload(
                            on_upload=lambda e: handle_file_upload(e, upload_component, reference_audio_player_container),
                            on_rejected=lambda: ui.notify('Invalid file format. Supported: MP3, WAV, FLAC.', type='negative'),
                            label='Drop Audio Here or Click to Upload',
                            max_files=1,
                            auto_upload=True,
                            max_file_size=10_000_000, # 10MB limit
                        ).classes('w-full h-40 flex items-center justify-center')
                        
                        upload_component.props('hide-upload-button multiple accept=".mp3,.wav,.flac,audio/*" color=grey flat')
                        upload_component.style('border: 2px dashed #9ca3af; border-radius: 0.75rem; padding: 0.5rem;')

                        with upload_component.add_slot('default'):
                            with ui.column().classes('w-full h-full items-center justify-center text-gray-500 gap-1'):
                                ui.icon('cloud_upload', size='xl').classes('text-gray-400')
                                ui.label('Drop Audio Here').classes('text-base')
                                ui.label('— or —').classes('text-sm text-gray-400')
                                ui.label('CLICK TO UPLOAD').classes('text-sm font-semibold text-orange-500 cursor-pointer')

                        # 2. Dynamic Audio Player Container (Hidden initially)
                        reference_audio_player_container = ui.row().classes('w-full hidden mt-2 p-2 border border-gray-200 rounded-xl bg-gray-50')
                            
                    # Sliders for Generation Control
                    def create_labeled_slider(label_text, min_val, max_val, step, default_val):            
                        def reset_slider(target_slider, target_input, default_value):
                            target_slider.value = default_value
                            target_input.value = default_value

                        with ui.column().classes('w-full mt-2 p-2 bg-gray-50 rounded-lg border border-gray-100'): 
                            with ui.row().classes('w-full items-center justify-between'):
                                ui.label(label_text).classes('text-sm')
                                
                                with ui.row().classes('items-center justify-end gap-1'): 
                                    number_input = ui.number(value=default_val, min=min_val, max=max_val, step=step, format='%.1f').classes('w-14').props('dense outlined input-class=text-center')
                                    ui.icon('refresh', size='sm').classes('text-gray-500 hover:text-indigo-500 cursor-pointer') \
                                        .on('click', lambda: reset_slider(slider, number_input, default_val))
                            
                            with ui.row().classes('w-full items-center'):
                                slider = ui.slider(min=min_val, max=max_val, step=step, value=default_val).classes('w-full')
                                
                            slider.bind_value_to(number_input, 'value')
                            number_input.bind_value_to(slider, 'value')
                        
                    create_labeled_slider('Exaggeration (Neutral = 0.5, extreme values can be unstable)', 0.0, 1.0, 0.1, 0.5)
                    create_labeled_slider('CFG/Pace', 0.0, 1.0, 0.1, 0.5)
                    create_labeled_slider('CFG/Peace', 0.0, 1.0, 0.1, 0.5)                    
                    create_labeled_slider('Temperature', 0.0, 1.0, 0.1, 0.8)

                    DEFAULT_SEED_VALUE = 0
                    with ui.column().classes('w-full mt-2 p-2 bg-gray-50 rounded-lg border border-gray-100'):
                        with ui.row().classes('w-full items-center justify-between'):
                            ui.label('Seed (0 for random)').classes('text-sm') 
                        
                        seed_input = ui.number(value=DEFAULT_SEED_VALUE, min=0, step=1, label='Seed Value').classes('w-full').props('dense outlined no-spinners') 
                        


            # --- Right Column: Input and Output
            with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-6'):
                # Text Input, Language, Generate Button, Audio Output
                with ui.column().classes('w-full p-4 border border-gray-200 rounded-xl gap-6'):
                    
                    # 1. Text Input Area
                    ui.label('Text to synthesize (max: chars 300)').classes('font-semibold text-gray-700')
                    ui.textarea(placeholder='Enter text here...').props('rows=4 outlined dense') \
                        .classes('w-full h-24') 
                    
                    # 2. Language Dropdown
                    ui.label('Language').classes('font-semibold text-gray-700')
                    ui.select(options=['Polish', 'English', 'German'], value='English', label='Select Language') \
                        .classes('w-full').props('outlined dense')

                    # 3. Generate Button
                    ui.button('Generate', on_click=lambda: ui.notify('Starting generation...', type='info')) \
                        .classes('w-full h-12 text-white font-bold text-lg rounded-lg shadow-lg') \
                        .props('color=orange')
                        
                    # 4. Output Audio
                    ui.label('Output Audio').classes('font-semibold text-gray-700')
                    ui.audio('').classes('w-full')