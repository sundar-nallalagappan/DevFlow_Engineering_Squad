from src.mcp.mcp_client import *

def mcp_get_file(path: str):
    """
    Reads a file from the GitHub repository using MCP.
    Input: The file path (e.g., 'src/revenue_engine.py')
    """
    # The official tool name in the MCP server is usually 'get_file_contents'
    # We also need the owner/repo context if the MCP server requires it, 
    # but the official server usually defaults to the repo context or takes owner/repo args.
    # IMPORTANT: Check tool arguments. Usually: owner, repo, path.
    
    # HARDCODING REPO FOR DEMO SPEED (Replace with your details)
    owner = "your-github-username"
    repo = "sales-dashboard-demo"
    
    return run_async(mcp_wrapper.call_mcp_tool(
        "get_file_contents", 
        {"owner": owner, "repo": repo, "path": path}
    ))


def mcp_write_file(path: str, content: str):
    """
    Creates or Updates a file in GitHub using MCP.
    Input: File path and the new content.
    """
    owner = "your-github-username"
    repo = "sales-dashboard-demo"
    commit_msg = "Agent fixing bug via MCP"
    
    return run_async(mcp_wrapper.call_mcp_tool(
        "create_or_update_file", 
        {
            "owner": owner, 
            "repo": repo, 
            "path": path, 
            "content": content,
            "message": commit_msg,
            "branch": "main" # or "master"
        }
    ))

# 1. Initialize MCP (Do this once at startup)
print("⏳ Initializing MCP Connection...")
run_async(mcp_wrapper.connect())