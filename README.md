# tutorial-calc

Small FastAPI-based calculator demo.

Setup
-----

Create and activate a virtual environment, then install pinned dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run
---

Start the server locally:

```bash
python -m uvicorn calculator:app --reload --port 8000
```

Open http://127.0.0.1:8000 in your browser to use the UI.

API
---

POST JSON `{ "expression": "2+2" }` to `/api/calc` to evaluate an expression.


---

This branch adds the pinned `requirements.txt` and a `README.md` with install/run instructions to address Issue #1.
