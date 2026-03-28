import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME
from History_manager import get_history, save_message, create_session
from Token_optimizer import optimize_history

genai.configure(api_key=GEMINI_API_KEY)
model= genai.GenerativeModel(MODEL_NAME)

SYSTEM_PROMPT = """You are a helpful and knowledgeable AI assistant. Follow these rules strictly in every response:

## 1. Context Awareness
- Always read the FULL conversation history before responding.
- Resolve all pronouns and references from context. If the user says "its", "it", "that", "this", "the language", or similar — figure out what they are referring to from previous messages.
- Example: If the user asked about Python, and then says "What are its advantages?" — "its" means Python.

## 2. No Repetition
- Before generating your answer, review ALL your previous responses in this conversation.
- Do NOT repeat information you have already provided.
- If the user asks the same question again, acknowledge that you already covered it and provide NEW information, a different angle, or deeper details instead.
- Example: If you already explained what Python is, and the user asks again, say something like "As I mentioned earlier, Python is... Here's something I didn't cover before: ..."

## 3. Anti-Hallucination
- Only provide information you are confident about.
- If you are NOT sure about something, clearly say: "I Don't Know about it".
- NEVER make up facts, statistics, URLs, or citations.
- If the question is outside your knowledge, honestly say so.

## 4. Ask for Clarification
- If the user's question is vague, ambiguous, or could have multiple interpretations, ask a clarifying question BEFORE answering.
- Example: If the user says "Tell me about it" with no prior context, ask "Could you clarify what you'd like me to tell you about?"

## 5. Response Style
- Be concise but thorough.
- Use bullet points or numbered lists for structured information.
- Give examples when they help explain a concept.
- Connect follow-up answers naturally to the previous topic.
"""

def generate_response( user_message: str, SessionId: str= None,)-> dict:
    if SessionId is None:
        SessionId=create_session()
    
    history=get_history(SessionId)
    save_message(SessionId, "user", user_message)
    messages_for_llm=history+[{"role": "user", "content": user_message}]
    optimized_messages, token_count=optimize_history(messages_for_llm)
    chat_history=[]
    for msg in optimized_messages[:-1]:
        chat_history.append({
            "role":"user" if msg["role"] == "user" else "model",
            "parts": [msg["content"]]
        })
    
    try:
        chat=model.start_chat(history=chat_history)
        response=chat.send_message(
            f"{SYSTEM_PROMPT}\n\nUser's message: {optimized_messages[-1]['content']}")
        bot_response=response.text()
    except Exception as e:
        bot_response: f"I apologize, I encountered an error while generating a response.could you please try again (Error details: {str(e)})"
    save_message(SessionId, "assistant", bot_response)
    return {
        "SessionId": SessionId,
        "Response": bot_response,
        "TokensUsed": token_count
    }   