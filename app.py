import streamlit as st
import json
import plotly.express as px
import pandas as pd
from agents import orchestrator

st.set_page_config(
    page_title="Shadow TPM",
    page_icon="🛡️",
    layout="wide"
)

st.sidebar.title("Shadow TPM")

# ──────────────────────────────────────────────
# Mandatory: User must enter their own Gemini API key
st.sidebar.subheader("Your Gemini API Key (Required)")
api_key_input = st.sidebar.text_input(
    "Paste your API key to run simulations",
    type="password",  # Hides the key as dots
    placeholder="AIzaSy...",
    key="api_key_input",  # Unique key to avoid conflicts
    help="This key is only used in your browser session — not stored. Create a free one at https://aistudio.google.com/app/apikey"
)

# NEW: Enter button
if st.sidebar.button("Enter", type="primary", key="enter_key_button"):
    if not api_key_input.strip():
        st.sidebar.error("Please paste a valid API key.")
        st.sidebar.markdown("Get a free key here: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)")
    else:
        st.sidebar.success("API key accepted — ready to run simulations!")
# ──────────────────────────────────────────────

st.sidebar.markdown("🛡️ Gemini-powered agentic tool for AI infrastructure risk simulation")
st.sidebar.markdown("Built with Google Gemini API • January 2026")
st.sidebar.markdown("---")
st.sidebar.info("Simulate real-world 2026 challenges: power shortages, vendor delays, gigawatt-scale compute constraints.")
st.sidebar.markdown("### Try These Example Prompts:")
st.sidebar.markdown("- **Software/ML:** Developing Gemini v3.0 model, 6-month launch, 150 engineers, dependencies on data pipeline and TPU v6.")
st.sidebar.markdown("- **Tech Debt:** Reducing technical debt in Cloud ML serving platform, 9-month program, 40% legacy code migration.")
st.sidebar.markdown("- **Compliance:** Managing EU AI Act compliance for generative AI product, 12-month timeline, external audits.")
st.sidebar.markdown("- **Infra:** Scaling 1GW TPU cluster in Texas, 9-month deadline, $500M budget, power and fiber vendors.")

st.title("Shadow TPM")
st.markdown("Proactive AI Co-Pilot for Google-scale AI Infrastructure Programs")
st.markdown("Simulate risks, trade-offs, and mitigations for data center / TPU cluster scaling in 2026.")

# Input section
project_input = st.text_area(
    "Describe your AI infrastructure program:",
    height=150,
    placeholder="Example: Scaling a new 1GW TPU cluster in Texas, 9-month deadline, $500M budget, key vendors for power infrastructure and fiber cables."
)

uploaded_file = st.file_uploader(
    "Upload roadmap or document (PDF, Word .docx, text .txt, or image)",
    type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
    help="Gemini can read PDFs, Word docs, plain text files, or images (e.g., roadmaps, whiteboard sketches) to improve risk predictions."
)

if st.button("Run Simulation", type="primary"):
    if not project_input.strip():
        st.error("Please enter a project description.")
    elif not api_key_input.strip():
        st.error("Please enter your Gemini API key in the sidebar to run simulations.")
    else:
        with st.spinner("Simulating program risks and trade-offs..."):
            result = orchestrator(project_input, uploaded_file, api_key_input)

        if "error" in result:
            st.error(f"Error: {result['error']}")
            if "raw" in result:
                with st.expander("Technical Debug Info"):
                    st.code(result["raw"])
        else:
            st.success("Simulation complete! 🚀 Risks & mitigations ready.")

            # Display Summary
            st.subheader("Summary")
            st.write(result["summary"])

            # Risks Section
            st.subheader("Predicted Risks")
            risks = result.get("risks", [])
            if risks:
                # Table
                df_risks = pd.DataFrame(risks)
                st.dataframe(df_risks, use_container_width=True)

                # Simple bar chart for risk probabilities
                df_prob = df_risks.copy()
                df_prob['probability_num'] = df_prob['probability'].str.rstrip('%').astype(float)
                fig_prob = px.bar(
                    df_prob,
                    x='risk',
                    y='probability_num',
                    color='impact',
                    title="Risk Probabilities (%) by Impact",
                    labels={'probability_num': 'Probability (%)', 'risk': 'Risk'},
                    height=450,
                    color_discrete_map={
                        'High': '#FF4C4C',
                        'Medium': '#FFA500',
                        'Low': '#4CAF50'
                    }
                )
                fig_prob.update_traces(hovertemplate='<b>%{x}</b><br>Probability: %{y}%')
                fig_prob.update_layout(
                    xaxis_tickangle=-45,
                    xaxis_title="",
                    yaxis_title="Probability (%)",
                    showlegend=True,
                    margin=dict(b=100)
                )
                st.plotly_chart(fig_prob, use_container_width=True)

                # Risk Heatmap
                df_pivot = df_prob.pivot_table(
                    index='risk',
                    columns='impact',
                    values='probability_num',
                    aggfunc='first'
                ).fillna(0)

                fig_heat = px.imshow(
                    df_pivot,
                    title="Risk Heatmap (Exact Probability by Impact)",
                    color_continuous_scale="Reds",
                    height=400,
                    labels=dict(x="Impact Level", y="Risk", color="Probability (%)"),
                    text_auto=True,
                    aspect="auto"
                )
                fig_heat.update_layout(
                    xaxis_title="Impact Level",
                    yaxis_title="Risk",
                    coloraxis_colorbar_title="Probability (%)",
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_heat, use_container_width=True)

                # Impact Pie Chart
                impact_counts = df_risks['impact'].value_counts()
                fig_pie = px.pie(
                    values=impact_counts.values,
                    names=impact_counts.index,
                    title="Risk Impact Distribution",
                    hole=0.3,
                    color_discrete_sequence=["#FF4C4C", "#FFA500", "#4CAF50"],
                    height=400
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No risks detected.")

            # Trade-offs Section
            st.subheader("Mitigation Trade-offs")
            tradeoffs = result.get("tradeoffs", [])
            for item in tradeoffs:
                risk = item["risk"]
                with st.expander(f"**Risk:** {risk} (Mitigation Options)"):
                    options = item.get("options", [])
                    if options:
                        df_options = pd.DataFrame(options)
                        st.table(df_options)
                    else:
                        st.info("No trade-offs generated for this risk.")

            # Key Impact Summary
            st.subheader("Key Impact Summary")
            if tradeoffs:
                max_delay_reduction = 0
                min_cost_impact = float('inf')
                max_risk_reduction = 0

                for item in tradeoffs:
                    for option in item.get("options", []):
                        time_str = option.get("time_impact", "0")
                        if "week" in time_str.lower():
                            try:
                                val = float(time_str.split()[0].replace("+", "").replace("-", ""))
                                if "-" in time_str:
                                    max_delay_reduction = max(max_delay_reduction, val)
                            except:
                                pass

                        cost_str = option.get("cost_impact", "0")
                        if "$" in cost_str:
                            try:
                                val = float(cost_str.replace("$", "").replace("M", "").replace("+", ""))
                                min_cost_impact = min(min_cost_impact, val)
                            except:
                                pass

                        risk_str = option.get("quality_risk_reduction", "0%")
                        if "%" in risk_str:
                            try:
                                val = float(risk_str.rstrip("%"))
                                max_risk_reduction = max(max_risk_reduction, val)
                            except:
                                pass

                col1, col2, col3 = st.columns(3)
                col1.metric("Max Delay Reduction", f"Up to {max_delay_reduction} weeks" if max_delay_reduction > 0 else "N/A", delta_color="normal")
                col2.metric("Min Cost Impact", f"+${min_cost_impact}M" if min_cost_impact != float('inf') else "N/A", delta_color="inverse")
                col3.metric("Max Risk Reduction", f"{max_risk_reduction}%" if max_risk_reduction > 0 else "N/A", delta_color="normal")
            else:
                st.info("No trade-off metrics available yet.")

            # Rest of your sections (Communication Artifacts, Ethics, Talent, Download) remain unchanged
            st.subheader("Communication Artifacts")
            comms = result.get("comms", {})
            if comms:
                with st.expander("Stakeholder Email Draft"):
                    email = comms.get("email_draft", {})
                    st.markdown(f"**Subject:** {email.get('subject', 'N/A')}")
                    st.markdown(f"**Greeting:** {email.get('greeting', 'N/A')}")
                    st.text_area("Body:", value=email.get('body', 'N/A'), height=200, key="email_body")
                    st.markdown(f"**Closing:** {email.get('closing', 'N/A')}")

                st.markdown("**Talking Points for Exec Meeting**")
                talking_points = comms.get("talking_points", [])
                if talking_points:
                    for point in talking_points:
                        st.markdown(f"- {point}")
                else:
                    st.info("No talking points generated.")

                with st.expander("Exec Slide Outline"):
                    slide = comms.get("slide_outline", {})
                    st.markdown(f"**Title:** {slide.get('title', 'N/A')}")
                    bullets = slide.get("bullets", [])
                    if bullets:
                        for bullet in bullets:
                            st.markdown(f"- {bullet}")
                    else:
                        st.info("No slide outline generated.")
            else:
                st.info("No communication artifacts generated (check if comms agent is enabled).")

            st.subheader("Ethics & Sustainability Review")
            ethics = result.get("ethics", {})
            if ethics:
                concerns = ethics.get("concerns", [])
                if concerns:
                    df_concerns = pd.DataFrame(concerns)
                    st.dataframe(df_concerns)
                else:
                    st.info("No major concerns flagged.")

                mitigations = ethics.get("mitigations", [])
                if mitigations:
                    st.markdown("**Suggested Mitigations**")
                    for m in mitigations:
                        st.markdown(f"- **{m['mitigation']}** → {m['benefit']}")
            else:
                st.info("Ethics check not available.")

            st.subheader("Talent & Resource Risk Simulation")
            talent = result.get("talent", {})
            if talent:
                talent_risks = talent.get("talent_risks", [])
                if talent_risks:
                    df_talent = pd.DataFrame(talent_risks)
                    st.dataframe(df_talent)

                mitigations = talent.get("mitigations", [])
                if mitigations:
                    st.markdown("**Suggested Mitigations**")
                    for m in mitigations:
                        st.markdown(f"- **{m['mitigation']}** → {m['benefit']}")
            else:
                st.info("Talent simulation not available.")

            st.download_button(
                label="Download Results as JSON",
                data=json.dumps(result, indent=2),
                file_name="shadow_tpm_simulation.json",
                mime="application/json"
            )