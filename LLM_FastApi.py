import os
import re
from typing import List, Dict
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(
    title="Programming Lab Multi-AI Evaluation API",
    description="A 100% Python Full-Stack App for Multi-LLM Evaluation",
    version="3.0"
)

OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

ALL_AVAILABLE_MODELS = {
    "Google Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "OpenAI GPT-4o Mini (Copilot)": "openai/gpt-4o-mini",
    "Anthropic Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet:beta", 
    "DeepSeek V3 (Coding Specialist)": "deepseek/deepseek-chat"       
}

JUDGE_MODEL = "openai/gpt-4o-mini"

# Global state to hold results purely in-memory across page reloads
UI_STATE = {
    "responses": {},
    "judge_report": "",
    "scores": {},
    "selected_models": list(ALL_AVAILABLE_MODELS.keys()),
    "student_question": "I'm trying to add two vectors using `v1 + v2` but my terminal says 'TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector''. How do I fix this?",
    "system_prompt": "You are an encouraging and expert Python lab instructor. Help students understand coding concepts and debug errors. CRITICAL: Do not just give them corrected code immediately. Point out where the logic fails, explain why, and ask a guiding question."
}

def ask_programming_llm(model_string: str, user_prompt: str, system_prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=model_string, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1200, 
            extra_headers={
                "HTTP-Referer": "http://localhost:8000", 
                "X-Title": "Programming Lab Assistant App",   
            }
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred with this model: {e}"

