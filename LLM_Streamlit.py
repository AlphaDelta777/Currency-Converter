import os
import re
import streamlit as st
import matplotlib.pyplot as plt
from openai import OpenAI

OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Available models catalog
ALL_AVAILABLE_MODELS = {
    "Google Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "OpenAI GPT-4o Mini (Copilot)": "openai/gpt-4o-mini",
    "Anthropic Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet:beta", 
    "DeepSeek V3 (Coding Specialist)": "deepseek/deepseek-chat"       
}

JUDGE_MODEL = "openai/gpt-4o-mini"

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
                "HTTP-Referer": "http://localhost:8501", 
                "X-Title": "Programming Lab Assistant Comparison",   
            }
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred with this model: {e}"

# Helper function to generate an individual transparent donut chart for a single model
def create_individual_transparent_chart(score, model_name, color):
    # Set text color to white to make it legible over dark Streamlit panels
    plt.rcParams['text.color'] = '#FFFFFF'
    plt.rcParams['axes.labelcolor'] = '#FFFFFF'
    
    fig, ax = plt.subplots(figsize=(3, 3), facecolor='none') # Invisible figure background
    ax.set_facecolor('none')                                 # Invisible axes background
    
    # Data represents: [Model's Score, Remaining points out of 100]
    sizes = [score, max(0, 100 - score)]
    colors = [color, '#333333'] # Active metric vs muted background ring
    
    wedges, texts = ax.pie(
        sizes, 
        colors=colors, 
        startangle=90, 
        wedgeprops=dict(width=0.4, edgecolor='none') # Width creates the "donut/ring" effect
    )
    
    # Add the numerical value text directly in the center of the ring
    ax.text(0, 0, f"{int(score)}/100", ha='center', va='center', fontsize=14, weight='bold')
    ax.axis('equal')
    
    return fig

st.set_page_config(page_title="Programming Lab AI Evaluator", layout="wide")

st.title("🎓 Multi-AI Peer Evaluation & Analytics Dashboard")
st.subheader("Visualizing pedagogical effectiveness with categorical breakdowns")

st.sidebar.header("1. Choose AI Models to Test")
selected_model_names = []
for model_name in ALL_AVAILABLE_MODELS.keys():
    # Dynamic checkboxes allow users to easily pick and toggle individual targets
    if st.sidebar.checkbox(model_name, value=True):
        selected_model_names.append(model_name)

st.sidebar.write("---")
st.sidebar.header("2. Teacher Settings")
lab_instructor_persona = st.sidebar.text_area(
    "System Prompt (AI Teacher Persona)",
    value=(
        "You are an encouraging and expert Python lab instructor. Your goal is to help "
        "students understand coding concepts and debug their errors. "
        "CRITICAL: Do not just give them the corrected code immediately. Point out where the "
        "logic or syntax is failing, explain why, and ask a guiding question to help them fix it."
    ),
    height=200
)

student_question = st.text_area(
    "Enter Student Question:",
    value="I'm trying to add two vectors using `v1 + v2` but my terminal says 'TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector''. How do I fix this?",
    height=100
)

if len(selected_model_names) == 0:
    st.warning("⚠️ Please select at least one AI model from the sidebar checkboxes to run the evaluation.")
else:
    if st.button("🚀 Run Comparison & Generate Analytics", type="primary"):
        if not OPENROUTER_API_KEY:
            st.error("Please set your OPENROUTER_API_KEY environment variable.")
        else:
            # Build the sub-dictionary containing only the active models chosen by the checkboxes
            ACTIVE_MODELS = {name: ALL_AVAILABLE_MODELS[name] for name in selected_model_names}
            collected_responses = {}
            
            st.write("### 🤖 Phase 1: Gathering Model Responses")
            tabs = st.tabs(list(ACTIVE_MODELS.keys()))
            
            # Step 1: Run query generation loop on checked items only
            for tab, (friendly_name, model_id) in zip(tabs, ACTIVE_MODELS.items()):
                with tab:
                    st.write(f"### {friendly_name}")
                    with st.spinner(f"Fetching response..."):
                        ai_response = ask_programming_llm(model_id, student_question, system_prompt=lab_instructor_persona)
                    collected_responses[friendly_name] = ai_response
                    st.markdown(ai_response)
            
            st.write("---")
            
            # Step 2: Meta Evaluation
            st.write("### ⚖️ Phase 2: AI Peer Review & Proportion Analytics")
            
            comparison_prompt = f"The student asked:\n'{student_question}'\n\n"
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
                "\n".join([f"{name}: [score]" for name in ACTIVE_MODELS.keys()]) +
                "\nDATA_END"
            )
            
            with st.spinner("Analyzing performance metrics..."):
                evaluation_report = ask_programming_llm(JUDGE_MODEL, comparison_prompt, system_prompt=judge_instructions)
                
            st.info("📊 **AI Evaluation Summary Report**")
            st.markdown(evaluation_report)
            
            try:
                data_block = re.search(r"DATA_START(.*?)DATA_END", evaluation_report, re.DOTALL)
                
                if data_block:
                    raw_content = data_block.group(1).strip()
                    raw_segments = re.split(r'\n|(?=\b(?:Google|OpenAI|Anthropic|DeepSeek)\b)', raw_content)
                    
                    parsed_scores = {}
                    for segment in raw_segments:
                        if ":" in segment:
                            name, score_str = segment.split(":", 1)
                            clean_score = re.sub(r'[^\d.]', '', score_str)
                            if clean_score:
                                parsed_scores[name.strip()] = float(clean_score)
                    
                    # Display individual data visual components in a clean horizontal row
                    if parsed_scores:
                        st.write("### 📈 Visual Breakdown: Individual Model Performance Ratings")
                        
                        # Generate column layouts matching the exact number of chosen models
                        chart_cols = st.columns(len(parsed_scores))
                        chart_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
                        
                        for col, (model_name, model_score), idx in zip(chart_cols, parsed_scores.items(), range(len(parsed_scores))):
                            with col:
                                # FIXED: Used unsafe_allow_html=True instead of unsafe_value=True
                                st.markdown(f"<p style='text-align: center; font-weight: bold; color: white;'>{model_name}</p>", unsafe_allow_html=True)
                                
                                # Generate the transparent, customized donut chart figure
                                fig = create_individual_transparent_chart(
                                    score=model_score, 
                                    model_name=model_name, 
                                    color=chart_colors[idx % len(chart_colors)]
                                )
                                
                                # Render the chart with complete transparent framing configurations enabled
                                st.pyplot(fig, clear_figure=True, transparent=True)
                else:
                    st.warning("Could not automatically isolate grading block scores for visualization processing.")
                    
            except Exception as chart_error:
                st.error(f"Failed to render visualization graphics: {chart_error}")