import google.generativeai as genai
import json
import requests

#import os
#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key="AIzaSyCX95VyuavKMnSx2NFTJggr8iscFgg7Msw")

# Use structured output config
generation_config = {
    "response_mime_type": "application/json"  # This forces pure JSON output
}

model = genai.GenerativeModel(
    'gemini-3-flash-preview',
    generation_config=generation_config
)

def risk_forecaster(project_input, uploaded_file=None):
    api_key = "d46ac50539794ee7a42821497a4ab807"
    news_query = "AI infrastructure OR data center OR TPU OR power shortage OR vendor delay OR gigawatt compute"  # Tailored to 2026 challenges
    url = f"https://newsapi.org/v2/everything?q={news_query}&sortBy=publishedAt&language=en&pageSize=5&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        articles = response.json().get('articles', [])
        news_snippets = "\n".join([f"{a['title']} - {a['description']} (Source: {a['source']['name']}, Published: {a['publishedAt']})" for a in articles])
        if not news_snippets:
            news_snippets = "No relevant recent news found."
    except Exception as e:
        news_snippets = f"No recent news available (API error: {str(e)})."
    prompt = f"""
    You are a versatile Risk Forecaster Agent for Google-scale technical programs in January 2026.
    Handle both software/ML (model training, launches, tech debt, safety, scaling) and infrastructure (data centers, power, vendors, TPU clusters).
    Input: {project_input}
    Recent market news: {news_snippets}
    If an uploaded file is provided, analyze it (e.g., extract timelines from PDF, dependencies from image) to inform risks.
    Detect program type and focus on relevant risks (e.g., training delays for software; grid delays for infra).
    Predict top 3-5 risks with probability, impact, and explanation.
    Output ONLY valid JSON: {{"risks": [{{"risk": "...", "probability": "XX%", "impact": "High/Medium/Low", "explanation": "..."}}]}}
    """
    
    # Handle multimodal
    content = [prompt]
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        mime_type = uploaded_file.type
        content.append({"mime_type": mime_type, "data": file_bytes})
    
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
    Generate professional communication artifacts...
    
    Generate:
    1. Email draft to stakeholders (e.g., Engineering + Finance leads): Subject + Greeting + Body (highlight key risks/trade-offs) + Closing.
    2. 3-4 bullet talking points for an exec update meeting.
    3. Simple 1-slide outline (title + 3 key bullets) for a risk review.
    
    Output ONLY valid JSON with this exact structure (no extra text, no markdown):
    {{
        "email_draft": {{ "subject": "Subject line", "greeting": "Greeting,", "body": "Full body text.", "closing": "Best,\nYour Name" }},
        "talking_points": ["Bullet 1", "Bullet 2", "Bullet 3"],
        "slide_outline": {{ "title": "Slide title", "bullets": ["Bullet 1", "Bullet 2", "Bullet 3"] }}
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

def orchestrator(project_input, uploaded_file=None):
    risks = risk_forecaster(project_input, uploaded_file)
    if "error" in risks:
        return risks

    ethics = ethics_checker(project_input, risks)
    if "error" in ethics:
        return ethics  # Or handle gracefully if you want
    
    tradeoffs = trade_off_optimizer(risks)
    if "error" in tradeoffs:
        return tradeoffs
    
    comms = comms_influencer(risks, tradeoffs)
    if "error" in comms:
        return comms  # Or handle gracefully if you want
    
    talent = talent_risk_simulator(project_input, risks)
    if "error" in talent:
        return talent  # Or handle gracefully if you want

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
    result = orchestrator(test_input)
    print(json.dumps(result, indent=2))