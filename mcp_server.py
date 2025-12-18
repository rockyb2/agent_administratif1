from fastapi import FastAPI
from pydantic import BaseModel
from agent_core import create_agent

app = FastAPI()
agent = create_agent()

class MCPRequest(BaseModel):
    session_id: str
    message: str
    
class MCPResponse(BaseModel):
    answer: str
    
@app.post("/mcp/chat")
def chat(req: MCPRequest):
    conversation_id = req.session_id
    output = agent.run(req.message)

    # save_message(...)
    return {"answer": output}


