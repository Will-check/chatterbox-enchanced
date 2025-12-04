from nicegui import ui
from nicegui_app.ui.common import handle_file_upload

def chatterbox_controls():
     # 1. Voice Profile, Reference Audio, and Sliders
    with ui.column().classes('w-full p-4 border border-gray-200 rounded-xl gap-6'):
        ui.label('Saved Voice Profiles').classes('font-semibold text-gray-700 w-full text-center')
        ui.select(options=['Profile 1', 'Profile 2', 'Default'], value='Default', label='Select Profile') \
            .classes('w-full mb-4').props('outlined dense')

        ui.label('Reference Audio').classes('font-semibold text-gray-700 w-full text-center')

        with ui.column().classes('w-full relative'):
            # Grouping container to keep both UI and functional elements together.
            uploader_container = ui.element('div').classes('relative w-full h-40 group')

            # Kontener odtwarzacza audio jest tutaj tworzony, ale początkowo pozostaje ukryty.
            # Jest przekazywany do handlera, aby został pokazany po przesłaniu.
            reference_audio_player_container = ui.row().classes('w-full mt-2 p-2 border border-gray-200 rounded-xl bg-gray-50')
            reference_audio_player_container.visible = False

            with uploader_container:
                # UI layer
                with ui.column().classes(
                    'w-full h-full border-2 border-dashed border-slate-300 rounded-lg '
                    'items-center justify-center bg-slate-50 transition-colors '
                    'group-hover:bg-slate-100 group-hover:border-slate-400'
                ):
                    ui.icon('cloud_upload', size='2rem', color='slate-400').classes('mb-2 transition-transform group-hover:scale-110')
                    ui.label('Drop Audio Here').classes('text-slate-500 text-base font-medium')
                    ui.label('- or -').classes('text-slate-300 text-xs my-1')
                    ui.label('CLICK TO UPLOAD').classes('font-bold text-orange-500 text-sm')

                # Functional layer
                uploader = ui.upload(
                    auto_upload=True,
                    on_upload=lambda e: handle_file_upload(e, uploader_container, reference_audio_player_container),
                    on_rejected=lambda: ui.notify('Invalid file format. Supported: MP3, WAV, FLAC.', type='negative'),
                    max_files=1,
                    max_file_size=10_000_000, # 10MB limit
                ).props(
                    'flat no-shadow accept=".mp3,.wav,.flac,audio/*" hide-upload-btn'
                ).classes(
                    # Opacity to show the custom UI element
                    'absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10'
                )
                uploader.on('click', lambda: uploader.run_method('pickFiles'))
                
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
                    slider = ui.slider(min=min_val, max=max_val, step=step, value=default_val).classes('w-full').props('color=indigo')
                    
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
            
            ui.number(value=DEFAULT_SEED_VALUE, min=0, step=1, label='Seed Value').classes('w-full').props('dense outlined no-spinners') 
