from smolagents import CodeAgent, LiteLLMModel, Tool, DuckDuckGoSearchTool
# import gradio as gr
import os
from loadindex import loadIndex
from tools import BuildWord, BuildPDF, BuildExcelPro, SendMail
from db import SessionLocal
from services.conversation_service import save_message, save_generated_file
import uuid
from models import Message  # IMPORTANT
conversation_id = uuid.uuid4()  # à créer une fois par session


def get_conversation_history(db, conversation_id, limit=10):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
        .all()
    )


def build_context(messages):
    context = ""
    for msg in messages:
        role = "Utilisateur" if msg.role == "user" else "Assistant"
        context += f"{role}: {msg.content}\n"
    return context



class RagTool(Tool):
    name = "RagTool"
    description = "Fait une recherche RAG sur la base de connaissance."
    inputs = {
        "query": {"type": "string", "description": "Question à poser à la base de documents"}
    }
    output_type = "string"

    def forward(self, query: str):
        # Charger l'index déjà stocké
        index = loadIndex()

        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return str(response)


def buildAgent():
    agent = CodeAgent(
        model=LiteLLMModel(
            model_id="mistral/mistral-large-latest",
            api_key=os.getenv("MISTRAL_API_KEY")
        ),
        tools=[RagTool(), DuckDuckGoSearchTool(), BuildWord(),
               BuildPDF(), BuildExcelPro(), SendMail()],
        max_steps=5
    )

    return agent


agent = buildAgent()


# function for chat with agent


conversation_id = uuid.uuid4()  # à créer une fois par session

def chatwithAgent(message, history):
    db = SessionLocal()

    try:
        # 1️⃣ Récupérer historique réel
        messages = get_conversation_history(db, conversation_id)

        context = build_context(messages)

        # 2️⃣ Construire prompt final
        final_prompt = f"""
Tu es un assistant IA professionnel.

Historique de la conversation :
{context}

Utilisateur : {message}
"""

        # 3️⃣ Appel UNIQUE à l'agent
        output = agent.run(final_prompt)

        # 4️⃣ Sauvegardes
        save_message(db, conversation_id, "user", message)
        save_message(db, conversation_id, "assistant", output)

        return output

    finally:
        db.close()




# gr.ChatInterface(
#     fn=chatwithAgent,
#     description="Agent IA assistant qui génère (pdf,excel et word)",
#     title="agent_administratif1",
# ).launch()
