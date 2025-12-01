import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# CONFIGURATION
GITHUB_TOKEN = "ghp_your_token_here" 

# Define how to run the Official GitHub MCP Server
server_params = StdioServerParameters(
    command="npx", # Requires Node.js installed
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN}
)

class GitHubMCPWrapper:
    def __init__(self):
        self.session = None
        self.exit_stack = None

    async def connect(self):
        """Starts the MCP server and connects."""
        print("🔌 Starting GitHub MCP Server...")
        # We use the stdio_client context manager manually
        self.client_ctx = stdio_client(server_params)
        self.read, self.write = await self.client_ctx.__aenter__()
        self.session = ClientSession(self.read, self.write)
        await self.session.initialize()
        print("✅ Connected to GitHub MCP!")

    async def list_available_tools(self):
        """Debug helper to see what the MCP server offers."""
        if not self.session: await self.connect()
        result = await self.session.list_tools()
        return [t.name for t in result.tools]

    async def call_mcp_tool(self, tool_name, arguments):
        """Generic function to call any MCP tool."""
        if not self.session: await self.connect()
        result = await self.session.call_tool(tool_name, arguments)
        return result.content[0].text

# INSTANTIATE GLOBAL WRAPPER
mcp_wrapper = GitHubMCPWrapper()

# HELPER: Helper to run async MCP calls in sync LangChain
def run_async(coro):
    return asyncio.run(coro)