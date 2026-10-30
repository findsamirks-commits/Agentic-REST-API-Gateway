"""Self-test script verifying FastAPI endpoint with TestClient."""

import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def run_self_test():
    print("Running Agentic REST API Gateway self-test...")

    # 1. Test Root
    res = client.get("/")
    assert res.status_code == 200
    print("[PASS] Root endpoint returned 200 OK")

    # 2. Test Temperature Abuse Review
    payload_temp = {
        "review_text": "The Amul butter and ice cream arrived completely melted and warm in the summer heat!",
        "customer_id": "CUST-10492",
    }
    res = client.post("/triage-review", json=payload_temp)
    assert res.status_code == 200
    data = res.json()
    assert data["defect_category"] == "Temperature Abuse"
    assert data["severity"] >= 3
    assert data["routing_department"] == "Supply Chain & Logistics"
    print("\n[PASS] Temperature Abuse Triage Result:")
    print(json.dumps(data, indent=2))

    # 3. Test Perishable Spoilage Review
    payload_spoil = {
        "review_text": "The Mother Dairy paneer was completely sour and smelled foul when opened.",
        "customer_id": "CUST-58311",
    }
    res = client.post("/triage-review", json=payload_spoil)
    assert res.status_code == 200
    data = res.json()
    assert data["defect_category"] == "Perishable Spoilage"
    assert data["severity"] == 5
    assert data["routing_department"] == "Category Managers"
    print("\n[PASS] Spoilage Triage Result:")
    print(json.dumps(data, indent=2))

    # 4. Test Missing Items Review
    payload_missing = {
        "review_text": "I ordered 2 bags of Aashirvaad Atta but the delivery bag only had 1 bag.",
        "customer_id": "CUST-49102",
    }
    res = client.post("/triage-review", json=payload_missing)
    assert res.status_code == 200
    data = res.json()
    assert data["defect_category"] == "Missing Items"
    assert data["routing_department"] == "Dark Store Ops"
    print("\n[PASS] Missing Items Triage Result:")
    print(json.dumps(data, indent=2))

    print("\n[ALL SELF-TESTS PASSED] Agentic REST API Gateway is fully operational!")


if __name__ == "__main__":
    run_self_test()
