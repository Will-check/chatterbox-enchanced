import gradio as gr
from gradio_app.models.tts_model import get_or_load_model
from gradio_app.logic.common import default_text_for_ui, on_language_change, generate_tts_audio, INITIAL_LANG

def build_text_to_speech_tab():
    with gr.Tab("🎤 Text-to-Speech"):
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

                ref_wav = gr.Audio(
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

                with gr.Accordion("More options", open=False):
                    seed_num = gr.Number(value=0, label="Random seed (0 for random)")
                    temp = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8)

                run_btn = gr.Button("Generate", variant="primary")

            with gr.Column():
                audio_output = gr.Audio(label="Output Audio")

        language_id.change(
            fn=on_language_change,
            inputs=[language_id, ref_wav, text],
            outputs=[ref_wav, text],
            show_progress=False
        )

        run_btn.click(
            fn=generate_tts_audio,
            inputs=[
                text,
                language_id,
                ref_wav,
                exaggeration,
                temp,
                seed_num,
                cfg_weight,
            ],
            outputs=[audio_output],
        )
            
