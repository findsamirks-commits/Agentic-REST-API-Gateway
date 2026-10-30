"""FastAPI Application for Agentic REST API Gateway.

Exposes POST /triage-review to process incoming customer feedback
and route operational defect tickets asynchronously.
"""

import asyncio
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import DefectResponse, ReviewPayload
from agent import triage_review_async

# Initialize FastAPI application
app = FastAPI(
    title="Agentic REST API Gateway (VoC Triage)",
    description=(
        "Production AI Gateway wrapping an autonomous Voice of Customer (VoC) triage agent "
        "powered by LangChain and Groq's openai/gpt-oss-120b endpoint."
    ),
    version="1.0.0",
)

# Enable CORS for frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Agentic REST API Gateway",
        "status": "online",
        "model": "openai/gpt-oss-120b",
        "docs_url": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


@app.post(
    "/triage-review",
    response_model=DefectResponse,
    status_code=status.HTTP_200_OK,
    tags=["Agentic Triage"],
    summary="Triage and route unstructured grocery customer review",
)
async def triage_review_endpoint(payload: ReviewPayload) -> DefectResponse:
    """Accepts customer review text and asynchronously routes the defect ticket.

    - **review_text**: Unstructured feedback from consumer.
    - **customer_id**: User account identifier.

    Returns:
    - **defect_category**: Primary failure mode (Temperature, Packaging, Spoilage, etc.)
    - **severity**: Integer rating (1-5)
    - **routing_department**: Target operational team
    - **rationale**: Natural language justification
    """
    if not payload.review_text or not payload.review_text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="review_text cannot be empty.",
        )

    try:
        response: DefectResponse = await triage_review_async(payload.review_text)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agentic triage execution failed: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn
    print("\nStarting Agentic REST API Gateway on http://127.0.0.1:8000...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
