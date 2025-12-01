from src.tools.developer_tools import *
from src.tools.jira_tools import read_ticket, comment_on_ticket
from src.instructions.instructions import dev_agent_instructions
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search, AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

dev_tools = [
    clone_repository,
    list_repo_files,
    read_repo_file,
    create_or_update_file,
    run_pytest,
    #ask_human_approval,
    push_changes_to_github,
    # Don't forget the Jira tool so it can read the requirements!
    read_ticket,
    comment_on_ticket 
]

import os
#from dotenv import load_dotenv
#load_dotenv()
#os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

# --- AGENT DEFINITION ---
def developer_agent():
    developer_agent = LlmAgent(
        name="Dev_expert",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config), # Pro is better for "Reasoning" on priority
        instruction=dev_agent_instructions,
        tools=dev_tools,
        output_key="dev_expert_output" 
    )

    print("✅ Developer Agent created.")
    print("📋 Role: Developer")
    print("🚀 Dev change & test completed.")
    
    return developer_agent