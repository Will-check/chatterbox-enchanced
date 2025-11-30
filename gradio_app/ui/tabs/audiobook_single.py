import gradio as gr
import gradio_app.logic.audiobook_single as asl

from gradio_app.models.tts_model import get_or_load_model
from gradio_app.logic.common import DEFAULT_VOICE_LIBRARY, INITIAL_LANG, on_language_change
from gradio_app.logic.voice_lib import get_voice_choices, refresh_voice_choices

def build_audiobook_single_tab(voice_library_path_state):
    with gr.TabItem("📖 Audiobook Creation - Single Sample", id="audiobook_single") as audiobook_single_tab:
        gr.HTML("""
        <div class="audiobook-header">
            <h2>📖 Audiobook Creation Studio - Single Voice</h2>
            <p>Transform your text into professional audiobooks with one consistent voice</p>
        </div>
        """)
        
        with gr.Row(equal_height=True):
            with gr.Column(scale=2):
                # Text Input Section
                with gr.Group():
                    gr.HTML("<h3>📝 Text Content</h3>")
                    
                    with gr.Row():
                        with gr.Column(scale=3):
                            language_id = gr.Dropdown(
                                choices=list(get_or_load_model().get_supported_languages().keys()),
                                value=INITIAL_LANG,
                                label="Language",
                                info="Select the language for text-to-speech synthesis",
                                interactive=True
                            )
                             
                            audiobook_text = gr.Textbox(
                                label="Audiobook Text",
                                placeholder="Paste your text here or upload a file below...",
                                lines=12,
                                max_lines=20,
                                info="Text will be split into chunks at sentence boundaries"
                            )
                            
            
            with gr.Column(scale=1):
                # Voice Selection & Project Settings
                with gr.Group():
                    gr.HTML("<h3>🎭 Voice Configuration</h3>")
                    
                    audiobook_voice_selector = gr.Dropdown(
                        choices=get_voice_choices(DEFAULT_VOICE_LIBRARY),
                        label="Select Voice",
                        value=None,
                        info="Choose from your saved voice profiles",
                        interactive=True
                    )
                
                # Project
                with gr.Group():
                    gr.HTML("<h3>📁 Project</h3>")
                    
                    project_name = gr.Textbox(
                        label="Project Name",
                        placeholder="e.g., my_first_audiobook",
                        info="Used for naming output files (project_001.wav, project_002.wav, etc.)"
                    )

                with gr.Group():
                    gr.HTML("<h3>📁 Project Management</h3>")
                    project_dropdown = gr.Dropdown(
                        choices=asl.get_project_choices(),
                        label="Select Existing Project",
                        value=None,
                        info="Load or resume an existing project"
                    )
                   
        # Processing Section
        with gr.Group():
            gr.HTML("<h3>🚀 Audiobook Processing</h3>")
            
            # Single processing buttons (default visible)
            with gr.Group(visible=True) as single_processing_group:
                with gr.Row():
                    create_parts_btn = gr.Button(
                        "🎧 Create Audio Parts",
                        variant="secondary",
                        size="lg"
                    )

                    create_audiobook_btn = gr.Button(
                        "🎵 Create Audiobook", 
                        variant="primary",
                        size="lg",
                        interactive=False
                    )
            
            # Status and progress
            audiobook_status = gr.HTML(
                "<div class='audiobook-status'>📋 Ready to create audiobooks! Load text, select voice, and set project name.</div>"
            )
            
            
            audio_parts_state = gr.State([])
            MAX_PART_ROWS = 100

            with gr.Group(elem_id="audio-parts-table"):
                gr.HTML("""
                <style>
                    /* table wrapper */
                    #audio-parts-table {
                        margin-top: 0.5rem;
                    }

                    /* header row styling */
                    #audio-parts-table .header-row {
                        background-color: #f3f4f6; /* light gray */
                    }

                    /* header cells */
                    #audio-parts-table .parts-header-cell {
                        background-color: #f3f4f6;
                        border: 1px solid #d1d5db;
                        font-weight: 600;
                        text-align: center;
                        padding: 4px 6px;
                    }

                    /* body rows */
                    #audio-parts-table .parts-row {
                    }

                    /* body cells */
                    #audio-parts-table .parts-cell {
                        background-color: #ffffff;
                        border: 1px solid #e5e7eb;
                        padding: 4px 6px;
                    }

                    /* subtle zebra striping */
                    #audio-parts-table .parts-row:nth-child(even) .parts-cell {
                        background-color: #fcfcfc;
                    }

                    /* center index text */
                    .index-cell {
                        text-align: center;
                    }

                    /* center checkbox / play / regen content */
                    .chunk-center {
                        display: flex !important;
                        justify-content: center !important;
                        align-items: center !important;
                        height: 100%;
                    }

                    .chunk-center > * {
                        margin: 0 auto !important;
                    }
                        
                    /* cell with chunk text – smaller padding */
                    #audio-parts-table .chunk-text-cell {
                        padding: 2px 4px;
                    }
                        
                    /* textarea in chunk text cell – remove thick border/margins */
                    #audio-parts-table .chunk-text-box textarea {
                        padding: 2px 4px;
                        border: none !important;
                        box-shadow: none !important;
                        border-radius: 0 !important;
                        min-height: 2.2em;
                        font-size: 0.9rem;
                    }
                        
                    /* remove extra padding/margin around textbox wrapper */
                    #audio-parts-table .chunk-text-box {
                        padding: 0;
                        margin: 0;
                    }
                    
                    /* Remove gray background for Play / Regenerate buttons */
                    #audio-parts-table .parts-cell button {
                        background-color: transparent !important;  /* brak szarego prostokąta */
                        border: none !important;
                        box-shadow: none !important;
                        padding: 0 !important;
                        min-width: 0 !important;
                    }
                </style>
                <h4>Audio Parts</h4>
                """)

                # header row built with the same layout as data rows
                with gr.Row(elem_classes=["header-row"]):
                    with gr.Column(scale=1, min_width=60, elem_classes=["parts-header-cell"]):
                        gr.HTML("Index")
                    with gr.Column(scale=1, min_width=70, elem_classes=["parts-header-cell"]):
                        gr.HTML("Exclude")
                    with gr.Column(scale=1, min_width=70, elem_classes=["parts-header-cell"]):
                        gr.HTML("Play")
                    with gr.Column(scale=1, min_width=90, elem_classes=["parts-header-cell"]):
                        gr.HTML("Regenerate")
                    with gr.Column(scale=16, min_width=400, elem_classes=["parts-header-cell"]):
                        gr.HTML("Chunk text")

                part_rows = []

                # Pre-create rows for audio parts (max 100) and hide them initially
                for row_index in range(MAX_PART_ROWS):
                    with gr.Row(
                        visible=False,
                        elem_id=f"chunk-row-{row_index}",
                        elem_classes=["parts-row"],
                    ) as row:
                        # Index (visible HTML + hidden Number for callbacks)
                        with gr.Column(scale=1, min_width=60, elem_classes=["parts-cell"]):
                            idx_display = gr.HTML(
                                value="",
                                elem_id=f"chunk-idx-display-{row_index}",
                                elem_classes=["index-cell"],
                            )
                            idx_comp = gr.Number(
                                label="",
                                interactive=False,
                                precision=0,
                                show_label=False,
                                visible=False,
                                elem_id=f"chunk-idx-{row_index}",
                            )
                        # Exclude
                        with gr.Column(scale=1, min_width=70, elem_classes=["parts-cell"]):
                            exclude_comp = gr.Checkbox(
                                label="",
                                value=False,
                                show_label=False,
                                elem_id=f"chunk-exclude-{row_index}",
                                elem_classes=["chunk-center"],
                            )
                        # Play
                        with gr.Column(scale=1, min_width=70, elem_classes=["parts-cell"]):
                            play_btn = gr.Button(
                                "▶️",
                                variant="secondary",
                                elem_id=f"chunk-play-{row_index}",
                                elem_classes=["chunk-center"],
                            )
                        # Regenerate
                        with gr.Column(scale=1, min_width=90, elem_classes=["parts-cell"]):
                            regen_btn = gr.Button(
                                "♻️",
                                variant="secondary",
                                elem_id=f"chunk-regen-{row_index}",
                                elem_classes=["chunk-center"],
                            )
                        # Chunk text
                        with gr.Column(
                            scale=16,
                            min_width=400,
                            elem_classes=["parts-cell", "chunk-text-cell"],
                        ):
                            text_comp = gr.Textbox(
                                label="",
                                lines=2,
                                interactive=False,
                                show_label=False,
                                elem_id=f"chunk-text-{row_index}",
                                elem_classes=["chunk-text-box"],
                            )

                    part_rows.append(
                        {
                            "row": row,
                            "idx_display": idx_display,
                            "idx": idx_comp,
                            "exclude": exclude_comp,
                            "play": play_btn,
                            "regen": regen_btn,
                            "text": text_comp,
                        }
                    )

            # Preview/Output area
            audiobook_output = gr.Audio(
                label="Generated Audiobook (Preview - Full files saved to project folder)",
                visible=False
            )
        
        # Instructions
        gr.HTML("""
        <div class="instruction-box">
            <h4>📋 How to Create Single-Voice Audiobooks:</h4>
            <ol>
                <li><strong>Add Text:</strong> Paste text</li>
                <li><strong>Select Voice:</strong> Choose from your saved voice profiles</li>
                <li><strong>Set Project Name:</strong> This will be used for output file naming</li>
                <li><strong>Validate:</strong> Check that everything is ready</li>
                <li><strong>Create:</strong> Generate your audiobook(s) with smart chunking!</li>
            </ol>
            <p><strong>🎯 Smart Chunking:</strong> Text is automatically split in sentences. Safety boundary is set at 50 words for optimal processing.</p>
            <p><strong>📁 File Output:</strong> Individual chunks saved as project_001.wav, project_002.wav, etc.</p>

        </div>
        """)

        def update_parts_rows(parts_state):
            updates = []
            max_rows = len(part_rows)

            for i in range(max_rows):
                if i < len(parts_state):
                    part = parts_state[i]
                    updates.extend(
                        [
                            gr.update(visible=True),                         # row
                            gr.update(value=str(part["index"]), visible=True),  # idx_display (HTML)
                            gr.update(value=part["index"], visible=False),   # idx (hidden Number)
                            gr.update(value=part["exclude"], visible=True),  # exclude
                            gr.update(visible=True),                         # play button
                            gr.update(visible=True),                         # regen button
                            gr.update(value=part["text"], visible=True),     # text
                        ]
                    )
                else:
                    updates.extend(
                        [
                            gr.update(visible=False),              # row
                            gr.update(value="", visible=False),    # idx_display
                            gr.update(value=None, visible=False),  # idx
                            gr.update(value=False, visible=False), # exclude
                            gr.update(visible=False),              # play
                            gr.update(visible=False),              # regen
                            gr.update(value="", visible=False),    # text
                        ]
                    )

            return updates

    
    # Prepare list of components (in correct order) for outputs
    row_outputs = []
    for pr in part_rows:
        row_outputs.extend(
            [
                pr["row"],
                pr["idx_display"],
                pr["idx"],
                pr["exclude"],
                pr["play"],
                pr["regen"],
                pr["text"],
            ]
        )
    
    project_dropdown.change(
        fn=asl.load_project_name,
        inputs=project_dropdown,
        outputs=project_name
    )

    create_parts_btn.click(
        fn=asl.create_audio_parts,
        inputs=[
            audiobook_text,
            language_id,
            voice_library_path_state,
            audiobook_voice_selector,
            project_name
        ],
        outputs=[audio_parts_state, audiobook_status]
    ).then(
        fn=update_parts_rows,
        inputs=audio_parts_state,
        outputs=row_outputs
    )

    create_audiobook_btn.click(
        fn=asl.create_audiobook,
        inputs=[audiobook_text, language_id, voice_library_path_state, audiobook_voice_selector,  project_name],
        outputs=[audiobook_output, audiobook_status]
    ).then(
        fn=asl.refresh_project_dropdown,
        inputs=[],
        outputs=[project_dropdown]
    )

    for pr in part_rows:
        pr["play"].click(
            fn=asl.play_audio_part_by_index,
            inputs=[pr["idx"], audio_parts_state],
            outputs=[audiobook_output]
        )

        pr["regen"].click(
            fn=asl.regen_audio_part_by_index,
            inputs=[
                pr["idx"],
                audio_parts_state,
                language_id,
                voice_library_path_state,
                audiobook_voice_selector,
                project_name,
            ],
            outputs=[audiobook_output, audiobook_status]
        )

        pr["exclude"].change(
            fn=asl.toggle_exclude_for_index,
            inputs=[pr["idx"], pr["exclude"], audio_parts_state],
            outputs=[audio_parts_state]
        )

    if voice_library_path_state is not None:
        audiobook_single_tab.select(
            fn=asl.refresh_voice_choices_without_default,
            inputs=voice_library_path_state,
            outputs=audiobook_voice_selector,
            show_progress=False
    )
            
