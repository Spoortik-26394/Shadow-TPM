import google.generativeai as genai
import json
import requests

generation_config = {
    "response_mime_type": "application/json"
}

model = genai.GenerativeModel(
    'mgemini-3-flash-preview',  # Higher free quota than 3-flash
    generation_config=generation_config
)

def risk_forecaster(project_input, uploaded_file=None):

    prompt = f"""
    You are a versatile Risk Forecaster Agent for Google-scale technical programs in January 2026.
    Handle both software/ML (model training, launches, tech debt, safety, scaling) and infrastructure (data centers, power, vendors, TPU clusters).
    Input: {project_input}
    If an uploaded file is provided, analyze it (e.g., extract timelines from PDF, dependencies from image) to inform risks.
    Detect program type and focus on relevant risks (e.g., training delays for software; grid delays for infra).
    Predict top 3-5 risks with probability, impact, and explanation.
    Output ONLY valid JSON: {{"risks": [{{"risk": "...", "probability": "XX%", "impact": "High/Medium/Low", "explanation": "..."}}]}}
    """

    # Handle multimodal file upload
    content = [prompt]
    if uploaded_file is not None:
        try:
            file_bytes = uploaded_file.read()
            mime_type = uploaded_file.type
            
            # Safety: Gemini has ~20MB practical limit
            if len(file_bytes) > 20 * 1024 * 1024:
                return {"error": "Uploaded file is too large (over 20MB). Please use a smaller file."}
            
            # Supported file types
            supported_mimes = {
                'application/pdf': 'PDF document',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word document (.docx)',
                'text/plain': 'Plain text file (.txt / Notepad)',
                'image/png': 'PNG image',
                'image/jpeg': 'JPEG/JPG image',
                'image/jpg': 'JPG image'
            }
            
            if mime_type not in supported_mimes:
                return {"error": f"Unsupported file type ({uploaded_file.name}). Please upload PDF, Word (.docx), text (.txt), PNG, JPG/JPEG."}
            
            content.append({"mime_type": mime_type, "data": file_bytes})
        except Exception as e:
            return {"error": f"Error processing uploaded file ({uploaded_file.name}): {str(e)}. Try again or skip upload."}
    
    response = model.generate_content(content)
    try:
        parsed = json.loads(response.text)
        return parsed
    except json.JSONDecodeError as e:
        print("JSON Parse Error:", e, "\nRaw response:", response.text)
        return {"error": "Failed to parse risks", "raw": response.text}

def trade_off_optimizer(risks_data):
    prompt = f"""
    You are a Trade-Off Optimizer Agent for technical programs.
    Input risks: {json.dumps(risks_data)}
    Suggest 2-3 mitigations per risk with trade-offs:
    - For software/ML: engineering effort, time, quality/safety.
    - For infra: cost, time, risk reduction.
    Output ONLY valid JSON: {{"tradeoffs": [{{"risk": "...", "options": [{{"option": "...", "effort_impact": "...", "time_impact": "...", "quality_risk_reduction": "XX%"}}]}}]}}
    """
    response = model.generate_content(prompt)
    try:
        parsed = json.loads(response.text)
        return parsed
    except json.JSONDecodeError as e:
        print("JSON Parse Error:", e, "\nRaw response:", response.text)
        return {"error": "Failed to parse trade-offs", "raw": response.text}

def comms_influencer(risks_data, tradeoffs_data):
    prompt = f"""
    You are a senior TPM Comms/Influencer Agent at Google.
    Focus on software/ML programs: model launches, platform upgrades, compliance, cross-team coordination.
    Input risks: {json.dumps(risks_data)}
    Input trade-offs: {json.dumps(tradeoffs_data)}
    
    Generate:
    1. Email draft to stakeholders (Subject + Greeting + Body + Closing)
    2. 3-4 bullet talking points for exec update
    3. Simple 1-slide outline (title + 3 bullets)
    
    Output ONLY valid JSON: {{
        "email_draft": {{ "subject": "...", "greeting": "...", "body": "...", "closing": "..." }},
        "talking_points": ["...", "..."],
        "slide_outline": {{ "title": "...", "bullets": ["...", "..."] }}
    }}
    """
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {"error": "Failed to generate comms"}

def ethics_checker(project_input, risks_data):
    prompt = f"""
    You are an Ethics & Sustainability Agent for Google technical programs.
    Project: {project_input}
    Risks: {json.dumps(risks_data)}
    
    Flag ethical/sustainability concerns: carbon footprint, regulatory (e.g., EU AI Act), community impact, bias in decisions, safety red-teaming.
    Suggest 2-3 mitigations.
    
    Output ONLY valid JSON: {{
        "concerns": [{{"concern": "...", "severity": "High/Medium/Low", "explanation": "..."}}],
        "mitigations": [{{"mitigation": "...", "benefit": "..."}}]
    }}
    """
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {"error": "Failed to check ethics"}

def talent_risk_simulator(project_input, risks_data):
    prompt = f"""
    You are a Talent Risk Simulator Agent for technical programs.
    Project: {project_input}
    Risks: {json.dumps(risks_data)}
    
    Predict 2-3 talent/resource risks (e.g., engineer churn, skill gaps, burnout).
    Suggest mitigations (recruitment, retention strategies).
    
    Output ONLY valid JSON: {{
        "talent_risks": [{{"risk": "...", "probability": "XX%", "impact": "High/Medium/Low", "explanation": "..."}}],
        "mitigations": [{{"mitigation": "...", "benefit": "..."}}]
    }}
    """
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {"error": "Failed to simulate talent risks"}

def orchestrator(project_input, uploaded_file=None, user_api_key=""):
    # Require user-provided API key
    if not user_api_key.strip():
        return {"error": "No Gemini API key provided. Please enter your own key in the sidebar to run simulations. Get a free key at https://aistudio.google.com/app/apikey"}

    # Configure Gemini with the user-provided key
    genai.configure(api_key=user_api_key)

    risks = risk_forecaster(project_input, uploaded_file)
    if "error" in risks:
        return risks

    ethics = ethics_checker(project_input, risks)
    if "error" in ethics:
        return ethics

    tradeoffs = trade_off_optimizer(risks)
    if "error" in tradeoffs:
        return tradeoffs

    comms = comms_influencer(risks, tradeoffs)
    if "error" in comms:
        return comms

    talent = talent_risk_simulator(project_input, risks)
    if "error" in talent:
        return talent

    final_output = {
        "summary": "Simulation complete for your AI infra program.",
        "risks": risks.get("risks", []),
        "tradeoffs": tradeoffs.get("tradeoffs", []),
        "comms": comms,
        "ethics": ethics if "error" not in ethics else {},
        "talent": talent if "error" not in talent else {}
    }
    return final_output


if __name__ == "__main__":
    test_input = "Scaling a new 1GW TPU cluster in Texas, 9-month deadline, $500M budget, key vendors for power infrastructure and fiber cables."
    result = orchestrator(test_input, user_api_key="")  # No key for test — will show error
    print(json.dumps(result, indent=2))