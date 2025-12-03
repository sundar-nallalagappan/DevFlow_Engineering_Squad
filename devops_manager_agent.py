print("sairam")
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
os.environ["jira_api_token"] = os.getenv('JIRA_API_TOKEN')
os.environ["GITHUB_PAT"] = os.getenv('GITHUB_PAT')

from src.instructions.instructions import devops_manager_instruction
from src.agents.dev_expert_agent import developer_agent
from src.agents.sprint_lead_agent import sprint_lead_agent

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search, AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.memory import InMemoryMemoryService


import asyncio 

APP_NAME = "DevOps Agent"  # Application
USER_ID  = "nsundar"       # User
SESSION  = "session-1"     # Session
MODEL_NAME = "gemini-2.5-flash-lite"
session_service = InMemorySessionService()
memory_service  = (InMemoryMemoryService()) 



retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# Define helper functions that will be reused throughout the notebook
async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    # List to store the text responses
    collected_responses = [] 
    
    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
                        # ✅ CAPTURE THE RESPONSE HERE
                        collected_responses.append(event.content.parts[0].text)
    else:               
        print("No queries!")
    
        # ✅ RETURN THE CAPTURED TEXT
    if not collected_responses:
        return "No response text captured."
    
    return "\n".join(collected_responses)


print("✅ Helper functions defined.")

async def devops_manager(user_input: str, session_id: str = "default_session"):
    sprint_lead_agent_instance = sprint_lead_agent() 
    developer_agent_insatnce   = developer_agent()
    
    devops_manager_agent = LlmAgent(
        name="DevOps_Manager_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config), # Pro is better for "Reasoning" on priority
        instruction=devops_manager_instruction,
        tools=[AgentTool(sprint_lead_agent_instance), AgentTool(developer_agent_insatnce)]
    )

    print("✅ DevOps_Manager_agent created.")
    
    devops_manager_runner = Runner(agent=devops_manager_agent, 
                               app_name=APP_NAME, 
                               session_service=session_service, 
                               memory_service=memory_service)
                               #plugins=[LoggingPlugin()])

#    response = await run_session(devops_manager_runner, 
#                             "Check the Jira board for project 'SALES-Dashboard' and pick the next task.",
#                             'session-04')
    response = await run_session(devops_manager_runner, 
                            user_input,  # <--- Dynamic Input
                            session_id   # <--- Dynamic Session)
    )
    return response

if __name__ == "__main__":
    print("Firing the devops manager agent")
    user_input = "Check the Jira board for project 'SALES-Dashboard' and pick the next task."
    agent_response = asyncio.run(devops_manager(user_input=user_input))
    print('!!!!!!!!!!!*************!!!!!!!!!!!!!!')
    print("Response:", agent_response)
    
    
    