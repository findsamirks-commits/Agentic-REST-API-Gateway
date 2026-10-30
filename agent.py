"""Voice of Customer (VoC) Triage Agent.

Uses ChatOpenAI configured with Groq's openai/gpt-oss-120b endpoint
and .with_structured_output(DefectResponse) for structured triage.
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas import DefectResponse

# Load environment variables from .env
load_dotenv()

# Initialize ChatOpenAI pointing to Groq's high-speed endpoint
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# System prompt defining triage rules and operational routing
SYSTEM_PROMPT = """You are an expert Voice of Customer (VoC) Quality Assurance & Operations Triage Agent for an enterprise quick-commerce grocery dark store network (Milkbasket).

Your mission is to analyze unstructured customer delivery reviews, accurately identify the primary failure mode, rate its operational severity from 1 (minor) to 5 (critical health/safety), and route the ticket to the responsible department.

Triage Guidelines:
1. Category Definitions:
   - 'Temperature Abuse': Melted butter/ice cream, warm milk, broken cold-chain during transit.
   - 'Packaging Integrity': Crushed cartons, torn bags, punctured pouches, oil leaks.
   - 'Missing Items': Items billed but omitted by dark store hub pickers.
   - 'Perishable Spoilage': Rotten vegetables, sour curd, moldy bread, expired stock.
   - 'Late Delivery SLA Breach': Delay past promised quick-commerce delivery window.

2. Routing Matrix:
   - Cold chain failures during delivery -> 'Supply Chain & Logistics'
   - In-store packing errors / picker omissions / bag tearing -> 'Dark Store Ops'
   - Vendor quality issues / rotten batches / expired stock -> 'Category Managers'
   - Minor billing questions / courtesy refunds -> 'Customer Experience / Support'

3. Severity Scale:
   - 1: Minor cosmetic/packaging crease with zero product impairment.
   - 2: Short delay (<15 mins) or minor non-perishable dent.
   - 3: Missing low-cost SKU or broken packaging requiring immediate customer refund.
   - 4: Broken cold chain / melted dairy or missing high-value staple item.
   - 5: Food contamination, rotten/sour dairy consumed, or severe biohazard risk.

Return ONLY structured JSON conforming to DefectResponse schema with clear rationale.
"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Customer Review to Triage:\n\"{review_text}\""),
    ]
)


def build_triage_chain():
    """Builds the LangChain extraction chain with structured output."""
    if GROQ_API_KEY and GROQ_API_KEY != "dummy_key":
        llm = ChatOpenAI(
            model=MODEL_NAME,
            openai_api_base=GROQ_BASE_URL,
            openai_api_key=GROQ_API_KEY,
            temperature=0.1,
            max_tokens=600,
        )
        return prompt_template | llm.with_structured_output(DefectResponse)
    return None


# Lazy chain initialization
triage_chain = build_triage_chain()


def fallback_rule_based_triage(review_text: str) -> DefectResponse:
    """Heuristic fallback classifier when API key is missing or endpoint is offline."""
    text_lower = review_text.lower()

    if any(k in text_lower for k in ["melted", "warm", "ice cream", "butter soft", "cold chain", "thawed"]):
        return DefectResponse(
            defect_category="Temperature Abuse",
            severity=4,
            routing_department="Supply Chain & Logistics",
            rationale="Cold-chain temperature excursion detected during last-mile transit resulting in melted dairy/frozen product.",
        )
    elif any(k in text_lower for k in ["punctured", "torn", "leaking", "crushed", "broken bag", "pressed"]):
        return DefectResponse(
            defect_category="Packaging Integrity",
            severity=3,
            routing_department="Dark Store Ops",
            rationale="Primary packaging physical rupture or crushing during dark store order bagging.",
        )
    elif any(k in text_lower for k in ["missing", "did not receive", "omitted", "not in the bag", "left out", "only had 1", "short delivery", "received only"]):
        return DefectResponse(
            defect_category="Missing Items",
            severity=3,
            routing_department="Dark Store Ops",
            rationale="Picker fulfillment discrepancy where billed SKU was omitted from the tote bag.",
        )
    elif any(k in text_lower for k in ["rotten", "sour", "fungus", "mold", "stale", "expired", "smell"]):
        return DefectResponse(
            defect_category="Perishable Spoilage",
            severity=5,
            routing_department="Category Managers",
            rationale="Perishable food safety hazard. Product delivered expired or spoiled; requires vendor batch quarantine.",
        )
    elif any(k in text_lower for k in ["late", "delayed", "took 2 hours", "ridiculous delay", "sla"]):
        return DefectResponse(
            defect_category="Late Delivery SLA Breach",
            severity=2,
            routing_department="Supply Chain & Logistics",
            rationale="Rider dispatch or route congestion caused order to miss the quick-commerce SLA delivery window.",
        )
    else:
        return DefectResponse(
            defect_category="General Inquiry",
            severity=1,
            routing_department="Customer Experience / Support",
            rationale="General service sentiment requiring standard customer care follow-up.",
        )


async def triage_review_async(review_text: str) -> DefectResponse:
    """Asynchronously triages a customer review string into a structured DefectResponse."""
    global triage_chain
    if triage_chain is None and os.getenv("GROQ_API_KEY"):
        triage_chain = build_triage_chain()

    if triage_chain is not None:
        try:
            result = await triage_chain.ainvoke({"review_text": review_text})
            if isinstance(result, DefectResponse):
                return result
            if isinstance(result, dict):
                return DefectResponse(**result)
        except Exception as e:
            print(f"[Warning] LLM triage invocation failed ({e}), using heuristic fallback.")

    return fallback_rule_based_triage(review_text)
