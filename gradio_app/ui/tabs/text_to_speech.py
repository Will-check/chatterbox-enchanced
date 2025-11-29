import gradio as gr
from gradio_app.models.tts_model import get_or_load_model
from gradio_app.logic.common import default_text_for_ui, on_language_change, generate_tts_audio, INITIAL_LANG
from gradio_app.logic.voice_lib import refresh_voice_choices, load_voice_profile_audio

def build_text_to_speech_tab(voice_library_path_state):
    with gr.Tab("🎤 Text-to-Speech", id="tts-tab") as tts_tab:
        with gr.Row():
            with gr.Column():
                text = gr.Textbox(
                    value=default_text_for_ui(INITIAL_LANG),
                    label="Text to synthesize (max chars 300)",
                    max_lines=5
                )

                language_id = gr.Dropdown(
                    choices=list(get_or_load_model().get_supported_languages().keys()),
                    value=INITIAL_LANG,
                    label="Language",
                    info="Select the language for text-to-speech synthesis"
                )

                voice_dropdown = gr.Dropdown(
                    choices=[],
                    label="Saved Voice Profiles",
                    value=None,
                    interactive=True
                )
                
                ref_audio = gr.Audio(
                    sources=["upload", "microphone"],
                    type="filepath",
                    label="Reference Audio File (Optional)",
                    value=None
                )

                gr.Markdown(
                    "💡 **Note**: Ensure that the reference clip matches the specified language tag. Otherwise, language transfer outputs may inherit the accent of the reference clip's language. To mitigate this, set the CFG weight to 0.",
                    elem_classes=["audio-note"]
                )

                exaggeration = gr.Slider(
                    0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5, extreme values can be unstable)", value=.5
                )

                cfg_weight = gr.Slider(
                    0.2, 1, step=.05, label="CFG/Pace", value=0.5
                )

                enable_trim = gr.Checkbox(
                    value=False,
                    label="Enable Silence Trimming",
                    info="Enable to cut silence and noise at the start/end of audio."
                )

                trim_db = gr.Slider(
                    minimum=10,
                    maximum=60,
                    value=30,
                    step=1,
                    interactive=True,
                    visible=False,
                    label="Silence Trim Threshold (top_db)",
                    info="Higher = less trimming, Lower = stronger trimming"
                )

                with gr.Accordion("More options", open=False):
                    seed_num = gr.Number(value=0, label="Random seed (0 for random)")
                    temp = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8)

                run_btn = gr.Button("Generate", variant="primary")

            with gr.Column():
                audio_output = gr.Audio(label="Output Audio")

        language_id.change(
            fn=on_language_change,
            inputs=[language_id, ref_audio],
            outputs=[ref_audio, text],
            show_progress=False
        )

        voice_dropdown.change(
            fn=load_voice_profile_audio,
            inputs=[voice_library_path_state, voice_dropdown],
            outputs=ref_audio,
            show_progress=False
        )

        enable_trim.change(
            fn=lambda enabled: gr.update(visible=enabled),
            inputs=enable_trim,
            outputs=trim_db
        )

        run_btn.click(
            fn=generate_tts_audio,
            inputs=[
                text,
                language_id,
                ref_audio,
                exaggeration,
                temp,
                seed_num,
                cfg_weight,
                trim_db,
                enable_trim
            ],
            outputs=[audio_output],
        )
        
    if voice_library_path_state is not None:
        tts_tab.select(
            fn=refresh_voice_choices,
            inputs=voice_library_path_state,
            outputs=voice_dropdown,
            show_progress=False
        )

    return ref_audio, voice_dropdown