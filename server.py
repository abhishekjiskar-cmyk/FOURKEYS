from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from agents import MultiAgentSystem
from reconciliation import Reconciler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

multi_agent = MultiAgentSystem(use_api=True)
reconciler = Reconciler()

@app.get("/")
async def get_ui():
    with open("ui.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/")
async def ask_question(request: Request):
    data = await request.json()
    problem = data.get("q", "")
    
    if not problem:
        return {"answer": "No question provided.", "found": False, "mode": "multi-agent", "sources": []}

    perspectives = multi_agent.get_perspectives(problem, parallel=True)
    reconciled = reconciler.reconcile(perspectives)
    
    sources = []
    for p in perspectives:
        sources.append({
            "file": p["role_name"],
            "section": f"Weight: {p['weight']*100}%",
            "passage": p["response"]
        })

    return {
        "answer": reconciled["final_answer"],
        "found": True,
        "mode": "multi-agent",
        "sources": sources
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
