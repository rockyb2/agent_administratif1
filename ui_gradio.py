# import gradio as gr
# import requests

# def chat_ui(message, history):
#     r = requests.post(
#         "http://localhost:8000/mcp/chat",
#         json={
#             "session_id": "user1",
#             "message": message
#         }
#     )
#     return r.json()["answer"]

# gr.ChatInterface(
#     fn=chat_ui,
#     title="Agent Administratif"
# ).launch()
