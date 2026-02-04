from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI 
import uvicorn
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
# model = client.models.get("gemini-2.0-flash")
app = FastAPI(title="Sabudh MCP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    role: str
    location: str
    n: int

async def call_llm(prompt: str) -> str:
    response = await model.ainvoke([HumanMessage(content=prompt)])
    raw =response.content if isinstance(response.content, str) else str(response.content)
    return raw.strip()


# def call_llm(prompt: str) -> str:
#     response =client.models.generate_content(
#         model = "gemini-2.5-flash", contents = prompt
#     )
#     return response.candidates[0].content.parts[0].text

def evaluate_code(code: str):
    prompt = f"""
You are a strict Python code evaluator.

Read this code and:
1. Give 2-3 lines of feedback
2. Give a score from 0 to 10

Code:
{code}

Return exactly in this format:
Feedback: ...
Score: X/10
"""
    return call_llm(prompt)

def generate_jobs(role, location, n):
    prompt = f"""
You are a job assistant.

Based on general market knowledge, list {n} jobs for the role:
Role: {role}
Location: {location}

For each job, include:
- Job Title
- Company
- Location
- Average monthly salary in INR (approximate)
- Short 1 line description

Do NOT give apply links.

Return only in this format:

1. Job Title - Company - Location - Avg Salary: ₹XXXXX/month - Description
"""
    return call_llm(prompt)





@app.post("/evaluate-python")
async def evaluate_python(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        return {"error": "Only .py files allowed"}

    content = await file.read()
    code = content.decode("utf-8")

    result = await evaluate_code(code)

    return {
        "filename": file.filename,
        "result": result
    }


@app.post("/get-jobs")
async def get_jobs(data: JobRequest):
    result = await generate_jobs(data.role, data.location, data.n)
    return {"job_text": result}
    


if __name__ == "__main__":
    
    uvicorn.run("api:app",host="127.0.0.1",port=7863,reload=True )

