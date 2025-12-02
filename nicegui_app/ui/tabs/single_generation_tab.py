from nicegui import ui
import os
import shutil
import base64
import time

temp_audio_files = {}

def single_generation_tab(tab_object: ui.tab):
    upload_component = None
    reference_audio_player_container = None
    upload_success_label = None

    def handle_reset():
        client_id = ui.context.client.id
        if client_id in temp_audio_files and os.path.exists(temp_audio_files[client_id]):
            os.remove(temp_audio_files[client_id])
            del temp_audio_files[client_id]

        # Reset UI components
        if reference_audio_player_container and upload_component:
            # Clear the player container
            with reference_audio_player_container:
                reference_audio_player_container.clear()
            
            # Hide player and show upload component
            reference_audio_player_container.classes(add='hidden')
            upload_component.classes(remove='hidden')
            
            ui.notify('Reference audio cleared.', type='info', timeout=1500)

    def handle_file_upload(e):
        client_id = e.client.id
        file_name = f'ref_{client_id}_{e.name}'

        # Clean up old file if it exists (simple session management)
        if client_id in temp_audio_files and os.path.exists(temp_audio_files[client_id]):
            os.remove(temp_audio_files[client_id])

        # Create a temporary file path
        temp_dir = 'temp_uploads'
        os.makedirs(temp_dir, exist_ok=True)
        temp_filepath = os.path.join(temp_dir, file_name)

        # Save the uploaded file chunk
        try:
            with open(temp_filepath, 'wb') as f:
                e.content.seek(0)
                shutil.copyfileobj(e.content, f)

            temp_audio_files[client_id] = temp_filepath
            
            # Update the audio player container content
            if reference_audio_player_container:
                with reference_audio_player_container:
                    reference_audio_player_container.clear() 
                    
                    with ui.row().classes('w-full items-center justify-between gap-2'):
                         ui.audio(temp_filepath).classes('flex-grow')
                         ui.icon('clear', size='sm').classes('text-gray-500 hover:text-red-500 cursor-pointer') \
                            .tooltip('Clear reference audio').on('click', handle_reset)

            
            ui.notify(f'Reference file uploaded: {e.name}', type='positive', timeout=2000)

            # Hide the upload component visually and show the player container
            if upload_component and reference_audio_player_container:
                upload_component.classes('hidden')
                reference_audio_player_container.classes(remove='hidden')
        
        except Exception as err:
            ui.notify(f'Error saving file: {err}', type='negative')
            # Ensure upload component is visible if saving fails
            upload_component.classes(remove='hidden')

    with ui.tab_panel(tab_object).classes('p-0 m-0 w-full'):
        with ui.row().classes('w-full p-6 gap-6 flex flex-wrap justify-start'):
            # --- Left Column
            with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-6'):
                # 1. First Border: Text Input and Language
                with ui.column().classes('w-full p-4 border border-gray-200 rounded-xl gap-6'):
                    # Text Input
                    ui.label('Text to synthesize (max: chars 300)').classes('font-semibold text-gray-700')
                    ui.textarea(placeholder='Enter text here...').props('rows=4 outlined dense') \
                        .classes('w-full h-24 resize-none')
                    
                    # Language Dropdown
                    ui.label('Language').classes('font-semibold text-gray-700')
                    ui.select(options=['Polish', 'English', 'German'], value='English', label='Select Language') \
                        .classes('w-full').props('outlined dense')

                # 2. Second Border: Voice Profile, Reference Audio, and Sliders
                with ui.column().classes('w-full p-4 border border-gray-200 rounded-xl mt-4 gap-6'):
                    ui.label('Saved Voice Profiles').classes('font-semibold text-gray-700')
                    ui.select(options=['Profile 1', 'Profile 2', 'Default'], value='Default', label='Select Profile') \
                        .classes('w-full mb-4').props('outlined dense')

                    ui.label('Reference Audio').classes('font-semibold text-gray-700')
                    
                    # DYNAMIC REFERENCE AUDIO SECTION
                    with ui.column().classes('w-full relative'):
                        # 1. Upload Component (Visible initially)
                        upload_component = ui.upload(
                            on_upload=handle_file_upload,
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
                        with ui.row().classes('w-full items-center justify-between mt-4'):
                            ui.label(label_text).classes('text-sm w-3/5')
                            with ui.row().classes('w-2/5 items-center justify-end'):
                                slider = ui.slider(min=min_val, max=max_val, step=step, value=default_val).classes('flex-grow')
                                number_input = ui.number(value=default_val, min=min_val, max=max_val, step=step, format='%.1f').classes('w-16 ml-2').props('dense outlined')
                                
                                slider.bind_value_to(number_input, 'value')
                                number_input.bind_value_to(slider, 'value')

                                # Optional: Add a refresh icon for reset (not implemented for actual reset logic)
                                ui.icon('refresh', size='sm').classes('text-gray-500 hover:text-indigo-500 cursor-pointer')
                        
                    create_labeled_slider('Exaggeration (Neutral = 0.5, extreme values can be unstable)', 0.0, 1.0, 0.1, 0.5)
                    create_labeled_slider('CFG/Pace', 0.0, 1.0, 0.1, 0.5)
                    create_labeled_slider('CFG/Peace', 0.0, 1.0, 0.1, 0.5)
                    
                    with ui.row().classes('w-full items-center justify-between mt-4'):
                        ui.label('Seed (0 for random)').classes('text-sm w-3/5')
                        ui.number(value=0, min=0, step=1).classes('w-24').props('dense outlined') 

                    create_labeled_slider('Temperature', 0.0, 1.0, 0.1, 0.8)

            with ui.column().classes('w-full md:w-[calc(50%-12px)] flex-grow gap-6'):
                with ui.column().classes('w-full p-4 border border-gray-200 rounded-xl gap-6'):
                    ui.label('Output Audio').classes('font-semibold text-gray-700')
                    ui.audio('').classes('w-full')
                    ui.button('Generate', on_click=lambda: ui.notify('Starting generation...', type='info')) \
                        .classes('w-full h-12 text-white font-bold text-lg rounded-lg shadow-lg') \
                        .props('color=orange')