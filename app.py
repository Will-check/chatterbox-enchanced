import gradio as gr
from gradio_app.ui.main_ui import build_ui


with gr.Blocks() as demo:
    build_ui(demo)
    demo.launch(mcp_server=True)
