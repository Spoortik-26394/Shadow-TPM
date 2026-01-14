# Shadow TPM 🛡️

**Proactive AI Co-Pilot for Technical Program Managers**

Shadow TPM is a Gemini-powered multi-agent simulation tool designed to help Technical Program Managers (TPMs) anticipate risks, evaluate trade-offs, generate communication artifacts, review ethics/sustainability concerns, and assess talent/resource risks in AI/ML and infrastructure programs.

Built as a showcase project to demonstrate agentic AI, prompt engineering, Streamlit UI development, and TPM domain knowledge.

## Live Demo

Try the app here:  
[https://shadow-tpm-spoorti-koujalagi.streamlit.app/]
(https://shadow-tpm-spoorti-koujalagi.streamlit.app/)

**Note**: Use your own Gemini API KEY. Create a free one at (https://aistudio.google.com/app/apikey)

## Features

- **6 specialized agents**:
  - Risk Forecaster (predicts 3–5 risks with % probability)
  - Trade-off Optimizer (mitigations + cost/time/quality trade-offs)
  - Comms/Influencer (email drafts, talking points, slide outlines)
  - Ethics & Sustainability Checker
  - Talent Risk Simulator (churn, skill gaps, burnout)
  - Orchestrator (coordinates everything)
- **Multimodal support**: Upload PDF, Word (.docx), text (.txt), PNG/JPG images (roadmaps, timelines, sketches)
- **Interactive dashboard**: Bar charts, risk heatmap, impact pie chart, metrics badges
- **User-provided API key**: Secure — no server-side keys stored

## Screenshots

Web app screenshot: https://github.com/Spoortik-26394/Shadow-TPM/blob/main/Shadow%20TPM%20Web%20app.png

## How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://https://github.com/Spoortik-26394/Shadow-TPM

2. Install dependencies: pip install -r requirements.txt
3. Run the app: streamlit run app.py
4. In the sidebar, paste your own Gemini API key (free at https://aistudio.google.com/app/apikey).
5. Enter a program description and run simulation.
