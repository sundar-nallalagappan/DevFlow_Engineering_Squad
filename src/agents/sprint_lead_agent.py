from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search, AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor

from src.instructions.instructions import sprint_lead_instructions 
from src.tools.jira_tools import search_tickets, read_ticket, comment_on_ticket

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

import os
#from dotenv import load_dotenv
#load_dotenv()
#os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

# --- AGENT DEFINITION ---
def sprint_lead_agent():
    sprint_lead_agent = LlmAgent(
        name="Sprint_Lead",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config), # Pro is better for "Reasoning" on priority
        instruction=sprint_lead_instructions,
        tools=[search_tickets, read_ticket, comment_on_ticket],
        output_key="sprint_lead_output" 
    )

    print("✅ Sprint_Lead Agent created.")
    print("📋 Role: Scrum Master / Triage")
    print("🚀 Ready to prioritize Jira tickets.")
    return sprint_lead_agent