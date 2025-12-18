from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_core import create_agent
from models import Message  # IMPORTANT

app = FastAPI()

# Configuration CORS pour permettre les requêtes depuis le frontend Vue.js
# En production, utilisez une variable d'environnement pour les origines autorisées
import os
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


agent = None

def get_agent():
    global agent
    if agent is None:
        print("⚙️ Initialisation de l'agent IA...")
        agent = create_agent()
    return agent

# Initialiser l'agent
# try:
#     agent = create_agent()
#     agent_ready = True
#     print("✅ Agent initialisé avec succès")
# except Exception as e:
#     print(f"⚠️ Erreur lors de l'initialisation de l'agent: {e}")
#     agent = None
#     agent_ready = False

# Endpoint racine pour vérifier que le serveur fonctionne
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Serveur MCP Agent IA fonctionnel",
        "agent_ready": agent_ready
    }

# Endpoint de santé pour la vérification de connexion
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "agent_ready": agent_ready
    }

class MCPRequest(BaseModel):
    session_id: str
    message: str
    
class MCPResponse(BaseModel):
    answer: str
    
@app.post("/mcp/chat")
def chat(req: MCPRequest):
    try:
        agent = get_agent()
        output = agent.run(req.message)
        return {"answer": output}
    except Exception as e:
        return {"answer": f"Erreur agent: {str(e)}"}



