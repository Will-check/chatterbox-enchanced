from gradio_app.ui.main_ui import build_ui


demo = build_ui()
demo.launch(mcp_server=True)
