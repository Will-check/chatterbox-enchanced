from nicegui import ui
from nicegui_app.ui.models.chatterbox import chatterbox_controls
from nicegui_app.logic.app_state import get_state


def single_generation_tab(tab_object: ui.tab):
    app_state = get_state()
    is_chatterbox_selected = lambda v: v == "Chatterbox"
    is_no_model_selected = lambda v: v == "No Model Selected"
    is_any_model_selected = lambda v: v != "No Model Selected"

    with ui.tab_panel(tab_object).classes("w-full p-0 m-0"):
        with ui.row().classes("flex flex-wrap justify-start w-full gap-6 p-6"):
            left_column_chatterbox = ui.column().classes(
                "w-full md:w-[calc(50%-12px)] flex-grow gap-6"
            )
            left_column_no_model = ui.column().classes(
                "w-full md:w-[calc(50%-12px)] flex-grow gap-6"
            )

            left_column_chatterbox.bind_visibility_from(
                app_state, "active_model", is_chatterbox_selected
            )

            left_column_no_model.bind_visibility_from(
                app_state, "active_model", is_no_model_selected
            )

            # --- Left Column: Empty - no model selected
            with left_column_no_model:
                with ui.column().classes(
                    "w-full p-4 border border-gray-200 rounded-xl gap-6 items-center justify-center min-h-[400px]"
                ):
                    ui.icon("info", size="2xl").classes("text-orange-500")
                    ui.label("No Model Selected").classes(
                        "font-bold text-xl text-gray-700"
                    )
                    ui.label(
                        "Please select a valid model from the dropdown menu to enable specific controls."
                    ).classes("text-center text-gray-500")

            # --- Left Column: Controls for Chatterbox
            with left_column_chatterbox:
                chatterbox_controls()

            # --- Right Column: Input and Output
            with ui.column().classes("flex-grow w-full gap-6 md:w-[calc(50%-12px)]"):
                # Text Input, Language, Generate Button, Audio Output
                with ui.column().classes(
                    "w-full p-4 border border-gray-200 rounded-xl gap-6"
                ):

                    # 1. Text Input Area
                    ui.label("Text to synthesize (max: chars 300)").classes(
                        "font-semibold text-gray-700 w-full text-center"
                    )
                    ui.textarea(placeholder="Enter text here...").props(
                        "rows=4 outlined dense"
                    ).classes("w-full h-24")

                    # 2. Language Dropdown
                    test_options = ["Polish", "English", "German"]
                    ui.label("Language").classes(
                        "font-semibold text-gray-700  w-full text-center"
                    )
                    language_dropdown = (
                        ui.select(
                            options=test_options,
                            value="English",
                            label="Select Language",
                        )
                        .classes("w-full")
                        .props("outlined dense")
                    )

                    language_dropdown.bind_enabled_from(
                        app_state, "active_model", is_any_model_selected
                    )

                    ui.label("Output Audio").classes(
                        "font-semibold text-gray-700 w-full text-center"
                    )
                    ui.audio("").classes("w-full")

                    generate_button = (
                        ui.button(
                            "Generate",
                            on_click=lambda: ui.notify(
                                "Starting generation...", type="info"
                            ),
                        )
                        .classes(
                            "w-full h-12 text-white font-bold rounded-lg shadow-lg"
                        )
                        .props("color=indigo")
                    )

                    generate_button.bind_enabled_from(
                        app_state, "active_model", is_any_model_selected
                    )
