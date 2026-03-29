from google import genai
from config import GEMINI_API_KEY, MODEL_NAME, MAX_TOKENS, MAX_HISTORY_MESSAGES

client=genai.Client(api_key=GEMINI_API_KEY)
    
def summarize_messages(messages: list)-> str:
    conversation_text=""
    for msg in messages:
        role_label="User" if msg["role"]=="user" else "Assistant"
        conversation_text= f"{role_label}: {msg['content']}\n"
    summary_prompt = f"""Summarize the following conversation in 2-3 concise sentences. 
                        Capture the key topics discussed, any important facts mentioned, and the user's main interests.
                        Do NOT include greetings or filler — only the essential information.

                    Conversation:
                    {conversation_text}
                    Summary:"""
    try:
        response=client.models.generate_content(
            model=MODEL_NAME,
            contents=summary_prompt)
        return response.text()
    except Exception:
        return conversation_text[:500]
    
def optimize_history(messages: list)-> list:
    if len(messages)<=4:
        return messages
    
    if len(messages)<=MAX_HISTORY_MESSAGES:
        return messages
    
    old_messages=messages[:-4]
    recent_messages=messages[-4:]

    summary=summarize_messages(old_messages)
    optimized=[
        {
            "role": "user",
            "content":f"[previous conversation summary: {summary}]"
        }
    ]+recent_messages
    
    return optimized