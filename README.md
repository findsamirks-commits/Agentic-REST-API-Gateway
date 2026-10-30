# Agentic REST API Gateway 🌐⚡

An enterprise **Agentic REST API Gateway** that serves as an intelligent front-door microservice for quick-commerce and retail operations. The gateway wraps an autonomous **Voice of Customer (VoC) Triage Agent** using **FastAPI**, **LangChain**, and **Groq's OpenAI-compatible endpoint** running `openai/gpt-oss-120b`.

---

## 🏛️ System Architecture

```
  ┌─────────────────────────────────────────────────────────┐
  │         E-Commerce / Dark Store App Frontend            │
  └───────────────────────────┬─────────────────────────────┘
                              │ POST /triage-review (ReviewPayload)
                              ▼
  ┌─────────────────────────────────────────────────────────┐
  │         FastAPI Gateway (main.py, port 8000)            │
  └───────────────────────────┬─────────────────────────────┘
                              │ Async Invoke
                              ▼
  ┌─────────────────────────────────────────────────────────┐
  │            VoC Triage Agent (agent.py)                  │
  │    LangChain + Groq LLM (openai/gpt-oss-120b)           │
  │    .with_structured_output(DefectResponse)              │
  └───────────────────────────┬─────────────────────────────┘
                              │
               Structured Triage & Routing JSON
                              ▼
  ┌─────────────────────────────────────────────────────────┐
  │                  DefectResponse                         │
  │  - Defect Category: Temperature / Packaging / Spoilage  │
  │  - Severity: 1 to 5                                     │
  │  - Routing Department: Dark Store Ops / Supply Chain    │
  │  - Rationale: Contextual operational explanation        │
  └─────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
Agentic-REST-API-Gateway/
├── requirements.txt      # fastapi, uvicorn, langchain, langchain-openai, pydantic>=2.0.0
├── schemas.py             # Pydantic models: ReviewPayload, DefectResponse
├── agent.py               # ChatOpenAI (Groq gpt-oss-120b) + with_structured_output
├── main.py                # FastAPI gateway exposing POST /triage-review & GET /health
├── test_api.py            # Self-test harness verifying end-to-end endpoint execution
├── .gitignore             # Virtualenvs, caches, .env
└── README.md              # Documentation & cURL examples
```

---

## 🛠️ API Specification

### `POST /triage-review`

#### Request Body (`ReviewPayload`)
```json
{
  "review_text": "The Amul butter and ice cream arrived completely melted and warm in the summer heat!",
  "customer_id": "CUST-10492"
}
```

#### Response (`DefectResponse`)
```json
{
  "defect_category": "Temperature Abuse",
  "severity": 4,
  "routing_department": "Supply Chain & Logistics",
  "rationale": "Cold-chain temperature excursion detected during last-mile transit resulting in melted dairy/frozen product."
}
```

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/findsamirks-commits/Agentic-REST-API-Gateway.git
cd Agentic-REST-API-Gateway
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the root folder:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Run Self-Test
```bash
python test_api.py
```

### 4. Launch the FastAPI Gateway
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive Swagger API docs will be available at: `http://127.0.0.1:8000/docs`.

### 5. Launch the Streamlit Frontend
```bash
streamlit run app.py
```
Opens interactive review triage portal with live defect classification and routing tickets.

---

## 🧪 cURL Example

```bash
curl -X POST "http://127.0.0.1:8000/triage-review" \
     -H "Content-Type: application/json" \
     -d '{
       "review_text": "The Mother Dairy paneer was completely sour and smelled foul when opened.",
       "customer_id": "CUST-58311"
     }'
```

---

## 📄 License
MIT License. Built by [Samir Sandhwar](https://github.com/findsamirks-commits) — Category Head & Retail AI Engineer.
