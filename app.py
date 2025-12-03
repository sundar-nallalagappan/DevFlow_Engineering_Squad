print("sairam")

# app.py
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv

# Ensure env is loaded before importing the agent logic
load_dotenv()

# Import logic
try:
    from devops_manager_agent import devops_manager
except ImportError as e:
    print("CRITICAL IMPORT ERROR:", e)
    # This helps debug if src/ folder paths are wrong

app = FastAPI()

class UserRequest(BaseModel):
    query: str
    session_id: str = "session-01"

@app.get("/")
def health_check():
    return {"status": "running", "message": "DevOps Agent API is active"}

@app.post("/api/chat")
async def chat_endpoint(request: UserRequest):
    try:
        # Call the agent
        response_text = await devops_manager(request.query, request.session_id)
        
        return {
            "status": "success",
            "response": response_text,
            "session_id": request.session_id
        }
    except Exception as e:
        # Print error to terminal so you can see what actually happened
        print(f"SERVER ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)