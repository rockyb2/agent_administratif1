from smolagents import CodeAgent,LiteLLMModel,Tool , DuckDuckGoSearchTool
import gradio as gr
import os
from loadindex import loadIndex
from tools import BuildWord,BuildPDF, BuildExcelPro,SendMail
from db import SessionLocal
from services.conversation_service import save_message, save_generated_file
import uuid

conversation_id = uuid.uuid4()  # à créer une fois par session
import json
import os






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
        model= LiteLLMModel(
            model_id= "mistral/mistral-large-latest",
            api_key=os.getenv("MISTRAL_API_KEY")
        ),
        tools=[RagTool(),DuckDuckGoSearchTool(),BuildWord(),BuildPDF(), BuildExcelPro(),SendMail()],
        max_steps = 5
    )
    
    return agent


agent = buildAgent()


# function for chat with agent
from db import SessionLocal
from services.conversation_service import save_message, save_generated_file
import uuid

conversation_id = uuid.uuid4()  # à créer une fois par session

def chatwithAgent(message, history):
    db = SessionLocal()

    # 1️⃣ Sauvegarde message utilisateur
    save_message(
        db,
        conversation_id,
        role="user",
        content=message
    )

    # 2️⃣ Appel agent
    output = agent.run(message)

    # 3️⃣ Fichier généré ?
    if "||" in output:
        text, file_path = output.split("||")

        save_message(
            db,
            conversation_id,
            role="assistant",
            content=text
        )

        save_generated_file(
            db,
            conversation_id,
            file_path
        )

        return text

    # 4️⃣ Réponse simple
    save_message(
        db,
        conversation_id,
        role="assistant",
        content=output
    )

    return output




gr.ChatInterface(
    fn=chatwithAgent,
    description= "Agent IA assistant qui génère (pdf,excel et word)",
    title= "agent_administratif1",
).launch()
