from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Models import chatResponse,chatRequest, sessionresponse, MessageHistory
from Prompts import generate_response
from History_manager import get_history, clear_history,create_session

app = FastAPI(
    title="Chatbot",
    description="A chatbot with memory and context awareness, built using FastAPI and Gemini-1.5-flash.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
@app.get("/")
def root():
    return {"message": "Chatbot is Running"}

@app.post("/chat", response_model=chatResponse)
def chat(request: chatRequest):
    try:
        result = generate_response(
            user_message=request.Message,
            SessionId=request.SessionId
            )
        return chatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/new-session", response_model=sessionresponse)
def new_session():
    try:
        SessionId=create_session()
        return sessionresponse(SessionId=SessionId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/history/{SessionId}")
def get_chat_history(SessionId: str):
    try:
        history=get_history(SessionId)
        if not history:
            return {"SessionId": SessionId, "messages": [], "message": "No history found for this session."}
        return {
            "SessionId": SessionId,
            "messages": [MessageHistory(role=msg["role"], content=msg["content"]) for msg in history]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/history/{SessionId}")
def delete_chat_history(SessionId: str):
    try:
        clear_history(SessionId)
        return {"SessionId": SessionId, "message": "Chat history cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))