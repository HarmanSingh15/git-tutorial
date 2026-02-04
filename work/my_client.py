from dotenv import load_dotenv
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from pydantic import BaseModel, Field
from langchain.agents import create_agent 
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from pymongo import MongoClient
from datetime import datetime, timezone
import uuid

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

class AgentResponse(BaseModel):
    response : str = Field(description="the AImessage response of the llm should be in str")

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["sabudh_chatbot"]
mongo_collection = mongo_db["chat_logs"]

SESSION_ID = str(uuid.uuid4)

async def main():
    server = MultiServerMCPClient(
    {
        "custom_mcp": {
            "url":"http://127.0.0.1:8000/mcp",
            "transport": "streamable-http",
            }
    }
)
    tools = await server.get_tools()
    print("Connected MCP Tools:", tools)

    llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature = 0,
    )
    

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are Sabudh Chatbot.

You can use these tools:
- evaluate_python_code
- get_jobs

Rules:
- If user wants to evaluate code, read the file content from the file uploaded.
- If user wants jobs, ask for role, location, and count.
- Use tools when needed. the chatbot can answer general questions on its own.                                                                                            
    """), ("human", "Input: {input}"), ("placeholder", "{agent_scratchpad}")
    ])
    agent = create_agent(
    model=llm,
    tools= tools,
#     agent_type = "react",
#     prompt=prompt
)
    chain = prompt | agent
 
    print("Sabudh MCP Chatbot")
    print("Type 'exit' to quit.\n")
    print("session id", SESSION_ID, "\n")

    while True:
        user_input = input("You: ").strip()
        last_human_message = user_input
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break

        try:
            result = await chain.ainvoke({"input": user_input})
            
            if isinstance(result, dict) and "messages" in result:
                msgs = result["messages"]
                ai_msg = msgs[-1]

                if hasattr(ai_msg, "content"):
                    content = ai_msg.content
                    
                    if isinstance(content, list) and "text" in content[0]:
                        final_text = content[0]["text"]
                        print("Bot: ", final_text)
                    else:
                        final_text = content
                        print("Bot: ", final_text)

                    try:
                        mongo_collection.insert_one({
                            "session_id": SESSION_ID,
                            "HumanMessage": last_human_message,
                            "AImessage": final_text,
                            "time": datetime.now(timezone.utc)
                        })    
                    except Exception as e:
                        print("Mongo insert error:", e)    
            
            elif hasattr(result, "content"):

                if isinstance(result.content, list) and "text" in result.content[0]:
                    final_text = result.content[0]["text"]
                    print("Bot: ", final_text)
                else:
                    final_text = result.content
                    print("Bot: ", final_text)

                try: 
                    mongo_collection.insert_one({
                        "session_id": SESSION_ID,
                        "HumanMessage": last_human_message,
                        "AIMessage": final_text,
                        "time": datetime.now(timezone.utc)
                    })
                except Exception as e:
                    print("Mongo insert error :", e)        

            else:
                final_text = str(result)
                print("Bot: ", final_text)

                try:
                    mongo_collection.insert_one({
                        "session_id": SESSION_ID,
                        "HumanMessage": last_human_message,
                        "AIMessage": final_text,
                        "time": datetime.now(timezone.utc)
                    })
                
                except Exception as e:
                    print("Mongo insert error:", e)    

        except Exception as e:
            print("Bot Error:", e)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())                