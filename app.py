"""Streamlit Frontend for Agentic REST API Gateway (VoC Triage).

Interactive UI to submit mock customer reviews, trigger the FastAPI
backend, and visualize structured defect classification and operational routing.
"""

import json
import requests
import streamlit as st

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agentic REST API Gateway | VoC Triage",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .badge-dept {
        background-color: #EEF2FF;
        color: #4338CA;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">⚡ Agentic REST API Gateway</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">'
    "Autonomous Voice of Customer (VoC) Triage & Defect Routing Gateway. "
    "Powered by <b>FastAPI</b>, <b>LangChain</b>, and Groq (<code>openai/gpt-oss-120b</code>)."
    "</div>",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Sidebar Configuration & Presets
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Gateway Settings")
    api_url = st.text_input(
        "FastAPI Endpoint",
        value="http://127.0.0.1:8000/triage-review",
        help="Backend REST endpoint receiving ReviewPayload",
    )

    st.markdown("---")
    st.subheader("💡 Sample Review Presets")
    st.caption("Click any preset to auto-fill the review text:")

    preset_cold = st.button("🧊 Melted Dairy / Cold-Chain Failure", use_container_width=True)
    preset_pack = st.button("📦 Crushed Carton / Oil Leak", use_container_width=True)
    preset_miss = st.button("🛒 Billed Item Omitted in Tote", use_container_width=True)
    preset_spoil = st.button("⚠️ Rotten / Sour Perishable Stock", use_container_width=True)
    preset_delay = st.button("⏱️ Quick-Commerce SLA Breach", use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Triage Severity Matrix")
    st.markdown(
        """
        - ⭐ **Level 1:** Minor cosmetic imperfection
        - ⭐⭐ **Level 2:** Short delivery delay (<15 mins)
        - ⭐⭐⭐ **Level 3:** Missing low-cost SKU / torn bag
        - ⭐⭐⭐⭐ **Level 4:** Cold-chain failure / melted items
        - ⭐⭐⭐⭐⭐ **Level 5:** Food safety contamination / spoiled stock
        """
    )

    st.markdown("---")
    st.markdown("### 👨‍💻 Developer & Architect")
    st.markdown("**Samir Sandhwar** | Category Head & AI Engineer")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-findsamirks--commits-black?style=flat&logo=github)](https://github.com/findsamirks-commits/Agentic-REST-API-Gateway)")
    st.markdown("[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-findsamirks-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/findsamirks)")
    st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-samirsandhwar-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/samirsandhwar)")

# -----------------------------------------------------------------------------
# Preset Selection Handling
# -----------------------------------------------------------------------------
default_review = "The Amul butter and ice cream arrived completely melted and warm in the summer heat!"
default_cust = "CUST-99214"

if preset_cold:
    default_review = "The Amul butter and Cornetto ice cream arrived completely melted and warm in the summer heat!"
    default_cust = "CUST-10492"
elif preset_pack:
    default_review = "The Fortune mustard oil pouch was punctured and leaked all over the vegetables in the tote bag."
    default_cust = "CUST-38104"
elif preset_miss:
    default_review = "I was billed for 2 bags of Aashirvaad Whole Wheat Atta 5kg, but the delivery bag only had 1 bag."
    default_cust = "CUST-49102"
elif preset_spoil:
    default_review = "The Mother Dairy paneer was sour and covered in green mold when opened today. Very bad!"
    default_cust = "CUST-58311"
elif preset_delay:
    default_review = "My 10-minute grocery order took over 45 minutes to arrive with no updates from the dark store."
    default_cust = "CUST-77291"

# -----------------------------------------------------------------------------
# Main Form Input
# -----------------------------------------------------------------------------
col_input, col_meta = st.columns([0.7, 0.3])

with col_input:
    review_input = st.text_area(
        "📝 Customer Feedback / Grievance Text",
        value=default_review,
        height=140,
        help="Paste unstructured customer feedback from review stream or customer support tickets.",
    )

with col_meta:
    customer_id_input = st.text_input(
        "👤 Customer Identifier",
        value=default_cust,
        help="Unique customer account ID associated with the order.",
    )
    st.write("")
    st.write("")
    triage_btn = st.button("🚀 Triage Review", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# API Request & Response Display
# -----------------------------------------------------------------------------
if triage_btn:
    if not review_input.strip():
        st.error("⚠️ Please enter a customer review before submitting.")
        st.stop()

    payload = {
        "review_text": review_input.strip(),
        "customer_id": customer_id_input.strip() if customer_id_input else "CUST-ANONYMOUS",
    }

    with st.spinner("🤖 Agentic Gateway triaging review via LangChain & Groq (openai/gpt-oss-120b)..."):
        try:
            response = requests.post(api_url, json=payload, timeout=30)
            if response.status_code != 200:
                st.error(f"❌ Gateway Error ({response.status_code}): {response.text}")
                st.stop()
            data = response.json()
        except requests.exceptions.ConnectionError:
            st.error(
                "❌ **Could not connect to FastAPI server at `http://127.0.0.1:8000`**.\n\n"
                "Please ensure the backend gateway is running in your terminal:\n"
                "```bash\nuvicorn main:app --host 127.0.0.1 --port 8000 --reload\n```"
            )
            st.stop()
        except Exception as e:
            st.error(f"❌ Request failed: {str(e)}")
            st.stop()

    # Parse DefectResponse fields
    category = data.get("defect_category", "Unknown")
    severity = int(data.get("severity", 1))
    dept = data.get("routing_department", "Customer Support")
    rationale = data.get("rationale", "")

    st.markdown("---")
    st.subheader("🎯 Triage & Operational Routing Resolution")

    # Metrics Display
    m1, m2, m3 = st.columns(3)

    star_rating = "⭐" * severity
    severity_labels = {
        1: "1 / 5 (Minor Inconvenience)",
        2: "2 / 5 (Operational Delay)",
        3: "3 / 5 (Moderate Discrepancy)",
        4: "4 / 5 (Cold-Chain / Severe Impairment)",
        5: "5 / 5 (Critical Food Safety Risk)",
    }
    sev_text = severity_labels.get(severity, f"{severity}/5")

    m1.metric("Defect Category", category)
    m2.metric("Severity Rating", f"{star_rating} ({severity}/5)", help=sev_text)
    m3.metric("Assigned Route", dept)

    # Highlighted Callout based on Severity
    st.markdown("### 📋 Executive Remediation Ticket")

    ticket_text = (
        f"**Target Department:** <span class='badge-dept'>{dept}</span>\n\n"
        f"**Failure Mode:** `{category}` | **Severity Score:** `{severity}/5`\n\n"
        f"**Agent Rationale:**\n> *\"{rationale}\"*"
    )

    if severity >= 4:
        st.error(f"🚨 **HIGH PRIORITY ESCALATION (SEVERITY {severity})**\n\n{ticket_text}", icon="🚨")
    elif severity == 3:
        st.warning(f"⚠️ **STANDARD OPERATIONAL TICKET (SEVERITY 3)**\n\n{ticket_text}", icon="⚠️")
    else:
        st.success(f"✅ **LOW-IMPACT / COURTESY RESOLUTION (SEVERITY {severity})**\n\n{ticket_text}", icon="✅")

    # Raw JSON expander for audit inspection
    with st.expander("🔍 View Raw DefectResponse JSON Payload", expanded=False):
        st.json(data)

else:
    st.info(
        "👈 **Select a sample review preset from the sidebar or type a review above, then click 'Triage Review'.**"
    )
