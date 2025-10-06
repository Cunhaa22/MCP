import cst_python_api as cpa
from openai import OpenAI
from agents.mcp import MCPServerStdio
import os
import gradio as gr
from dotenv import load_dotenv
import asyncio

params = {
    "command": "uv",
    "args": ["run", "-m", "cst_python_api.CST_API_SERVER"]
}

async def main():
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
        mcp_tools = await server.list_tools()
        print(mcp_tools)

if __name__ == "__main__":
    asyncio.run(main())