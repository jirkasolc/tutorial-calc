from fastapi.testclient import TestClient
from calculator import app


def test_api_calc_basic():
    client = TestClient(app)
    resp = client.post("/api/calc", json={"expression": "2+2"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] in ("4", "4.0", "4.0")
