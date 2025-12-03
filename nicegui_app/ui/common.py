from nicegui import ui
import os


# Dictionary to manage temporary audio file paths per client session
temp_audio_files = {}


def handle_reset(upload_component, reference_audio_player_container):
    client_id = ui.context.client.id
    if client_id in temp_audio_files and os.path.exists(temp_audio_files[client_id]):
        os.remove(temp_audio_files[client_id])
        del temp_audio_files[client_id]

    # Reset UI components
    if reference_audio_player_container and upload_component:
        reference_audio_player_container.clear()
        upload_component.reset()
        reference_audio_player_container.classes(add='hidden')
        upload_component.classes(remove='hidden')

async def handle_file_upload(e, upload_component, reference_audio_player_container):
    client_id = e.client.id
    file_name = f'ref_{client_id}_{e.file.name}'

    # Clean up old file if it exists (simple session management)
    if client_id in temp_audio_files and os.path.exists(temp_audio_files[client_id]):
        os.remove(temp_audio_files[client_id])

    # Create a temporary file path
    temp_dir = 'temp_uploads'
    os.makedirs(temp_dir, exist_ok=True)
    temp_filepath = os.path.join(temp_dir, file_name)

    # Save the uploaded file chunk
    try:
        await e.file.save(temp_filepath)
        
        temp_audio_files[client_id] = temp_filepath
        
        # Update the audio player container content
        if reference_audio_player_container:
            with reference_audio_player_container:
                reference_audio_player_container.clear() 
                
                with ui.row().classes('w-full items-center justify-between gap-2'):
                        ui.audio(temp_filepath).classes('flex-grow')
                        ui.icon('clear', size='sm').classes('text-gray-500 hover:text-red-500 cursor-pointer') \
                        .tooltip('Clear reference audio').on('click', lambda: handle_reset(upload_component, reference_audio_player_container))

        ui.notify(f'Reference file uploaded: {e.file.name}', type='positive', timeout=2000)

        # Hide the upload component visually and show the player container
        if upload_component and reference_audio_player_container:
            upload_component.classes('hidden')
            reference_audio_player_container.classes(remove='hidden')
    
    except Exception as err:
        ui.notify(f'Error saving file: {err}', type='negative')
        # Ensure upload component is visible if saving fails
        upload_component.classes(remove='hidden')