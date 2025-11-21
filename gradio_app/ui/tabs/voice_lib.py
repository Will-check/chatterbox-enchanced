import gradio as gr
import gradio_app.logic.voice_lib as vl

from gradio_app.logic.common import INITIAL_LANG, DEFAULT_VOICE_LIBRARY, generate_tts_audio
from gradio_app.models.tts_model import get_or_load_model



def build_voice_library_tab(voice_library_path_state):
    with gr.Tab("📚 Voice Library", id="voice_library_tab"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("<h3>🎭 Voice Management</h3>")
                
                # Voice Library Settings
                with gr.Group():
                    gr.HTML("<h4>📁 Library Settings</h4>")
                    voice_library_path = gr.Textbox(
                        value=DEFAULT_VOICE_LIBRARY,
                        label="Voice Library Folder",
                        placeholder="Enter path to voice library folder",
                        info="This path will be remembered between sessions"
                    )
                    update_path_btn = gr.Button("💾 Save & Update Library Path", size="sm")
                    
                    # Configuration status
                    config_status = gr.HTML(
                        f"<div class='config-status'>📂 Current library: {DEFAULT_VOICE_LIBRARY}</div>"
                    )
                
                # Voice Selection
                with gr.Group():
                    gr.HTML("<h4>🎯 Select Voice</h4>")
                    voice_dropdown = gr.Dropdown(
                        choices=[],
                        label="Saved Voice Profiles",
                        value=None,
                        interactive=True
                    )
                    
                    with gr.Row():
                        refresh_btn = gr.Button("🔄 Refresh", size="sm")
                        delete_voice_btn = gr.Button("🗑️ Delete", size="sm", variant="stop")
            
            with gr.Column(scale=2):
                # Voice Testing & Saving
                gr.HTML("<h3>🎙️ Voice Testing & Configuration</h3>")
                
                with gr.Group():
                    gr.HTML("<h4>📝 Voice Details</h4>")
                    voice_name = gr.Textbox(label="Voice Name", placeholder="e.g., narrator_male_deep")
                    voice_display_name = gr.Textbox(label="Display Name", placeholder="e.g., Deep Male Narrator")
                    voice_description = gr.Textbox(
                        label="Description", 
                        placeholder="e.g., Deep, authoritative voice for main character",
                        lines=2
                    )
                
                with gr.Group():
                    gr.HTML("<h4>🎵 Voice Settings</h4>")
                    ref_audio = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Reference Audio"
                    )
                    
                    with gr.Row():
                        voice_exaggeration = gr.Slider(
                            0.25, 2, step=.05,
                            label="Exaggeration",
                            value=0.5
                        )
                        voice_cfg = gr.Slider(
                            0.2, 1, step=.05,
                            label="CFG/Pace",
                            value=0.5
                        )

                    with gr.Accordion("More options", open=False):
                        seed_num = gr.Number(value=0, label="Random seed (0 for random)")
                        voice_temp = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8)

                # Volume Normalization Section
                with gr.Group():
                    gr.HTML("<h4>🎚️ Volume Normalization</h4>")
                    
                    enable_voice_normalization = gr.Checkbox(
                        label="Enable Volume Normalization",
                        value=False,
                        info="Automatically adjust audio level to professional standards"
                    )
                    
                    with gr.Row():
                        volume_preset_dropdown = gr.Dropdown(
                            choices=[
                                ("📚 Audiobook Standard (-18 dB)", "audiobook"),
                                ("🎙️ Podcast Standard (-16 dB)", "podcast"),
                                ("📺 Broadcast Standard (-23 dB)", "broadcast"),
                                ("🎛️ Custom Level", "custom")
                            ],
                            label="Volume Preset",
                            value="audiobook",
                            interactive=True
                        )
                        
                        target_volume_level = gr.Slider(
                            -30.0, -6.0, 
                            step=0.5,
                            label="Target Level (dB RMS)",
                            value=-18.0,
                            interactive=True,
                            info="Professional audiobook: -18dB, Podcast: -16dB"
                        )
                
                # Test Voice
                with gr.Group():
                    gr.HTML("<h4>🧪 Test Voice</h4>")
                    test_text = gr.Textbox(
                        value="Hello, this is a test of the voice settings. How does this sound?",
                        label="Test Text",
                        lines=2
                    )
                    language_id = gr.Dropdown(
                        choices=list(get_or_load_model().get_supported_languages().keys()),
                        value=INITIAL_LANG,
                        label="Language",
                        info="Select the language for text-to-speech synthesis"
                    )

                    with gr.Row():
                        test_voice_btn = gr.Button("🎵 Test Voice", variant="secondary")
                        save_voice_btn = gr.Button("💾 Save Voice Profile", variant="primary")
                    
                    test_audio_output = gr.Audio(label="Test Audio Output")

                    # Status messages
                    voice_status = gr.HTML("<div class='voice-status'>Ready to test and save voices...</div>")

        update_path_btn.click(
            fn=vl.update_voice_library_path,
            inputs=voice_library_path,
            outputs=[voice_library_path_state, config_status, voice_dropdown]
        )
        
        refresh_btn.click(
            fn=vl.refresh_voice_choices,
            inputs=voice_library_path_state,
            outputs=[voice_dropdown]
        )

        voice_dropdown.change(
            fn=vl.load_voice_profile,
            inputs=[voice_library_path_state, voice_dropdown],
            outputs=[ref_audio, voice_exaggeration, voice_cfg, voice_temp, voice_name, voice_display_name, voice_description, voice_status]
        )

        test_voice_btn.click(
            fn=generate_tts_audio,
            inputs=[
                test_text,
                language_id,
                ref_audio,
                voice_exaggeration,
                voice_temp,
                seed_num,
                voice_cfg,
            ],
            outputs=[test_audio_output],
        )

        save_voice_btn.click(
            fn=lambda path, name, display, desc, audio, exag, cfg, temp, enable_norm, target_level: vl.save_voice_profile(
                path, name, display, desc, audio, exag, cfg, temp, enable_norm, target_level
            ),
            inputs=[
                voice_library_path_state, voice_name, voice_display_name, voice_description,
                ref_audio, voice_exaggeration, voice_cfg, voice_temp, 
                enable_voice_normalization, target_volume_level,

            ],
            outputs=voice_status
        ).then(
            fn=vl.refresh_voice_choices,
            inputs=voice_library_path_state,
            outputs=[voice_dropdown]
        )

        delete_voice_btn.click(
            fn= vl.delete_voice_profile,
            inputs=[voice_library_path_state, voice_dropdown],
            outputs=[voice_status, voice_dropdown]
        ).then(
            fn=vl.refresh_voice_choices,
            inputs=voice_library_path_state,
            outputs=[voice_dropdown]
        )    