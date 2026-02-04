MCP-Based Code Evaluation & Job Assistant Chatbot

Project Description

This project is an MCP (Model Context Protocol) powered AI chatbot that evaluates Python code, provides structured feedback with a score, and generates job listings. The system integrates FastAPI, LangChain tool-calling agents, Google Gemini models, MCP tools, MongoDB for chat history, and a Gradio-based user interface.

The chatbot can analyze uploaded Python files or file paths, rate the code on a scale of 0 to 10, provide short feedback, and generate job listings based on role and location.

Key Features

Python Code Evaluation

Upload Python (.py) files or provide a file path

Get a numerical score (0–10)

Receive concise, meaningful feedback

MCP Tool Integration

Tools exposed through an MCP server

LangChain agent dynamically decides when to call tools

Job Listings Generator

Generates up to 5 job postings

Includes salary estimates

Covers both companies and startups

Interactive Chatbot Interface

Built using Gradio

Supports chat-based interaction and file uploads

Chat History Storage

Stores HumanMessage and AIMessage in MongoDB

Supports session-based conversations

Asynchronous and Scalable

FastAPI async endpoints

Non-blocking Gemini API calls

System Architecture

User interacts with Gradio Chat UI
↓
LangChain Tool-Calling Agent
↓
MCP Server (Tool Layer)
↓
FastAPI Backend
↓
Google Gemini API

Technology Stack

Backend Framework: FastAPI
Frontend/UI: Gradio
LLM: Google Gemini (via LangChain)
Agent Framework: LangChain Tool Calling
Protocol: Model Context Protocol (MCP)
Database: MongoDB
Programming Language: Python 3.10+

Project Structure

api.py

FastAPI backend

Handles code evaluation and job listing APIs

server.py

MCP server

Exposes tools for code evaluation and job listings

mcp_agent.py

LangChain agent implementation

Gradio chatbot UI

MongoDB integration for chat history

.env

Stores API keys and database configuration

Environment Variables

Create a .env file in the root directory and add:

GOOGLE_API_KEY=your_google_gemini_api_key
MONGO_URI=mongodb://localhost:27017
MONGO_DB=chatbot_db
MONGO_MESSAGES_COL=messages

How to Run the Project

Step 1: Start FastAPI Backend

Run:
python api.py

The API will start at:
http://127.0.0.1:8080

Step 2: Start MCP Server

Run:
python server.py

This exposes MCP tools using streamable HTTP transport.

Step 3: Launch Chatbot UI

Run:
python mcp_agent.py

The Gradio UI will be available at:
http://127.0.0.1:7860

Example Usage

Code Evaluation:
Upload a Python file and ask:
"Evaluate this code for correctness and optimization"

Job Listings:
Ask:
"Show Python developer jobs in Bangalore"

API Endpoints

Code Evaluation:
POST /feedback/upload
POST /feedback/file_path

Job Listings:
POST /Job_lists
