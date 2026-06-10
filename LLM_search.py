import os
from openai import OpenAI

OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODELS_TO_COMPARE = {
    "Google Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "OpenAI GPT-4o Mini (Copilot)": "openai/gpt-4o-mini",
    "Anthropic Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet:beta", 
    "DeepSeek V3 (Coding Specialist)": "deepseek/deepseek-chat"       
}

def ask_programming_llm(model_string: str, user_prompt: str, system_prompt: str) -> str:
    """
    Sends a query to a specific OpenRouter model.
    """
    try:
        completion = client.chat.completions.create(
            model=model_string, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1200, 
            extra_headers={
                "HTTP-Referer": "http://localhost:3000", 
                "X-Title": "Programming Lab Assistant Comparison",   
            }
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"An error occurred with this model: {e}"


if __name__ == "__main__":
    lab_instructor_persona = (
        "You are an encouraging and expert Python lab instructor. Your goal is to help "
        "students understand coding concepts and debug their errors. "
        "CRITICAL: Do not just give them the corrected code immediately. Point out where the "
        "logic or syntax is failing, explain why, and ask a guiding question to help them fix it."
    )
    
    student_question = (
        "I'm trying to add two vectors using `v1 + v2` but my terminal says "
        "'TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector''. How do I fix this?"
    )
    
    print(f"Starting comparison for {len(MODELS_TO_COMPARE)} different AI models...\n")
    print(f"Student Question: '{student_question}'\n")
    print("=" * 60)

    for friendly_name, model_id in MODELS_TO_COMPARE.items():
        print(f"\n🤖 FETCHING RESPONSE FROM: {friendly_name}...")
        
        ai_response = ask_programming_llm(model_id, student_question, system_prompt=lab_instructor_persona)
        
        print(f"\n--- {friendly_name} Response ---")
        print(ai_response)
        print("-" * 60)

    print("\nComparison finished!")