import gradio as gr
from chatterbox.mtl_tts import SUPPORTED_LANGUAGES
from gradio_app.logic.common import DEFAULT_VOICE_LIBRARY
from gradio_app.ui.tabs.text_to_speech import build_text_to_speech_tab
from gradio_app.ui.tabs.voice_lib import build_voice_library_tab
# from ui.tab_audiobook_single import build_single_tab
# from ui.tab_audiobook_multi import build_multi_tab
# from ui.tab_production import build_production_tab

def get_supported_languages_display() -> str:
    """Generate a formatted display of all supported languages."""
    language_items = []
    for code, name in sorted(SUPPORTED_LANGUAGES.items()):
        language_items.append(f"**{name}** (`{code}`)")
    
    # Split into 2 lines
    mid = len(language_items) // 2
    line1 = " • ".join(language_items[:mid])
    line2 = " • ".join(language_items[mid:])
    
    return f"""
### 🌍 Supported Languages ({len(SUPPORTED_LANGUAGES)} total)
{line1}

{line2}
"""

def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown("Chatterbox Multilingual Demo")
        gr.Markdown(get_supported_languages_display())

        voice_library_path_state = gr.State(DEFAULT_VOICE_LIBRARY)
    
        with gr.Tabs():
            build_text_to_speech_tab()
            build_voice_library_tab(voice_library_path_state)
        #     build_single_tab()
        #     build_multi_tab()
        #     build_production_tab()
        
    return demo