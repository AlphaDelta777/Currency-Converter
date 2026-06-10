import os
import re
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from LLM_search import OpenAI

app = FastAPI(
    title="Programming Lab Multi-AI Evaluation API",
    description="Backend API to query multiple LLMs and get automated evaluation reports with scores.",
    version="1.0"
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

class EvaluationRequest(BaseModel):
    student_question: str = Field(
        default="I'm trying to add two vectors using v1 + v2 but my terminal says TypeError. How do I fix this?"
    )
    system_prompt: str = Field(
        default="You are an encouraging Python lab instructor. Guide the student without giving the code away immediately."
    )
    models_to_run: List[str] = Field(
        default=["Google Gemini 2.5 Flash", "OpenAI GPT-4o Mini (Copilot)", "DeepSeek V3 (Coding Specialist)"],
        description="List of friendly names of models you want to evaluate."
    )

class EvaluationResponse(BaseModel):
    model_responses: Dict[str, str]
    judge_report: str
    parsed_scores: Dict[str, float]

# Core function to talk to OpenRouter
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
                "X-Title": "Programming Lab Assistant API",   
            }
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred with this model: {e}"

@app.post("/api/evaluate", response_model=EvaluationResponse)
async def evaluate_models(payload: EvaluationRequest):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY environment variable is not set on the server.")
    
    # 1. Filter out requested models
    active_models = {}
    for name in payload.models_to_run:
        if name in ALL_AVAILABLE_MODELS:
            active_models[name] = ALL_AVAILABLE_MODELS[name]
            
    if not active_models:
        raise HTTPException(status_code=400, detail="None of the selected models match the available models catalog.")
        
    # 2. Phase 1: Query selected models
    collected_responses = {}
    for friendly_name, model_id in active_models.items():
        ai_response = ask_programming_llm(model_id, payload.student_question, payload.system_prompt)
        collected_responses[friendly_name] = ai_response
        
    # 3. Phase 2: Build prompt for the AI Judge
    comparison_prompt = f"The student asked:\n'{payload.student_question}'\n\n"
    for name, response in collected_responses.items():
        comparison_prompt += f"=== RESPONSE FROM {name} ===\n{response}\n\n"
        
    judge_instructions = (
        "You are an educational evaluator grading computer science lab assistants. "
        "Analyze the responses and compare their teaching effectiveness.\n\n"
        "First, provide a written evaluation summarizing who won and why.\n\n"
        "Second, at the absolute end of your response, output a strict data breakdown block "
        "assigning each model a teaching quality score from 0 to 100 based on their performance. "
        "ONLY include lines for the models listed below:\n"
        "DATA_START\n" + 
        "\n".join([f"{name}: [score]" for name in active_models.keys()]) +
        "\nDATA_END"
    )
    
    evaluation_report = ask_programming_llm(JUDGE_MODEL, comparison_prompt, system_prompt=judge_instructions)

    parsed_scores = {}
    try:
        data_block = re.search(r"DATA_START(.*?)DATA_END", evaluation_report, re.DOTALL)
        if data_block:
            raw_content = data_block.group(1).strip()
            raw_segments = re.split(r'\n|(?=\b(?:Google|OpenAI|Anthropic|DeepSeek)\b)', raw_content)
            
            for segment in raw_segments:
                if ":" in segment:
                    name, score_str = segment.split(":", 1)
                    clean_score = re.sub(r'[^\d.]', '', score_str)
                    if clean_score:
                        parsed_scores[name.strip()] = float(clean_score)
    except Exception:
        pass # If parsing fails, it returns an empty dict for scores, avoiding a complete crash

    return {
        "model_responses": collected_responses,
        "judge_report": evaluation_report,
        "parsed_scores": parsed_scores
    }