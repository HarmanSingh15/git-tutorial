from mcp.server.fastmcp import FastMCP
import requests
# import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from google import genai 
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
url = "http://127.0.0.1:7863"
model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")


mcp = FastMCP("Sabudh MCP Server")

# def call_llm(prompt: str) -> str:
#     response = client.models.generate_content(model="gemini-2.5-flash", contents = prompt)
#     return response.candidates[0].content.parts[0].text

@mcp.tool()
def evaluate_python_code(file_content: str) -> str:
    """
    Sends code to FASTAPI /evaluate-python endpoint
    """
    try: 
        file = {
        "file": ("code.py", file_content)
    }

        resp = requests.post(f"{url}/evaluate-python", files=file)
        return resp.text
    except Exception as e:
        return f"MCP Tool Error {e}"
   
   

@mcp.tool()
def get_jobs(role: str, location: str, n:int) -> str:
    """
    Sends data to FASTAPI /get-jobs endpoint
    """
    try:
        payload = {
        "role": role,
        "location":location,
        "n": n
    }

        resp= requests.post(f"{url}/get-jobs", json=payload)
        return resp.text
    except Exception as e:
        return f"MCP Tool Error{e}"
    

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    mcp.run(transport="streamable-http")