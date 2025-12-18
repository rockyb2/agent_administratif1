# agent_core.py
from smolagents import CodeAgent, LiteLLMModel
import os
from tools import BuildWord, BuildPDF, BuildExcelPro, SendMail
from app import RagTool

def create_agent():
    return CodeAgent(
        model=LiteLLMModel(
            model_id="mistral/mistral-large-latest",
            api_key=os.getenv("MISTRAL_API_KEY")
        ),
        tools=[
            RagTool(),
            BuildWord(),
            BuildPDF(),
            BuildExcelPro(),
            SendMail()
        ],
        max_steps=5
    )
