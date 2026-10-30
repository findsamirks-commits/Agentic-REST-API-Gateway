"""Pydantic data schemas for Agentic REST API Gateway."""

from typing import Literal
from pydantic import BaseModel, Field


class ReviewPayload(BaseModel):
    """Incoming request payload containing unstructured customer feedback."""

    review_text: str = Field(
        ...,
        description="Raw unstructured customer review or operational grievance text",
        examples=["The Amul butter arrived completely melted and the milk pack was punctured."],
    )
    customer_id: str = Field(
        ...,
        description="Unique customer identifier",
        examples=["CUST-99214"],
    )


class DefectResponse(BaseModel):
    """Structured operational response produced by the VoC Triage Agent."""

    defect_category: Literal[
        "Temperature Abuse",
        "Packaging Integrity",
        "Missing Items",
        "Perishable Spoilage",
        "Late Delivery SLA Breach",
        "Catalog Discrepancy",
        "General Inquiry",
    ] = Field(
        ...,
        description="Categorized primary operational failure mode",
    )
    severity: int = Field(
        ...,
        ge=1,
        le=5,
        description="Severity rating from 1 (minor inconvenience) to 5 (severe food safety hazard or regulatory breach)",
    )
    routing_department: Literal[
        "Dark Store Ops",
        "Category Managers",
        "Supply Chain & Logistics",
        "Customer Experience / Support",
        "Quality Assurance",
    ] = Field(
        ...,
        description="Internal functional team responsible for immediate remediation",
    )
    rationale: str = Field(
        ...,
        description="Concise commercial and operational reasoning explaining the triage decision and urgency",
    )
