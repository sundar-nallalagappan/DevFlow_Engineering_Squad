print("sairam")
from devops_manager_agent import *

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/run-agent")  # Changed to GET for simplicity
async def run_agent():
    print("🚀 Triggering Agent via API...")
    # Call your function
    result = await devops_manager() 
    return {"result": result}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)