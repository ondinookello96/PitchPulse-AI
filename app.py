import asyncio
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from agent_framework import Agent, MCPStdioTool
from agent_framework.foundry import FoundryChatClient

load_dotenv()

app = FastAPI(title="PitchPulse AI - Tactical & Philosophical Intelligence")

class SimpleApiCredential:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def get_token(self, *scopes, **kwargs):
        class Token:
            def __init__(self, token):
                self.token = token
                self.expires_on = 32503680000
        return Token(self._api_key)

class AnalysisRequest(BaseModel):
    window: str = "60-65"

async def execute_pipeline(match_window: str) -> dict:
    credential = SimpleApiCredential(os.environ["AZURE_OPENAI_API_KEY"])
    
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=credential
    )

    mcp_tool = MCPStdioTool(
        name="football_telemetry_mcp",
        command=sys.executable,
        args=["football_mcp_server.py"]
    )

    async with mcp_tool:
        state_agent = Agent(
            name="StateMonitorAgent",
            client=client,
            instructions=(
                "You are a Premier League Match Telemetry Monitor. Call get_tactical_window_metrics "
                "for the requested window. Identify statistical anomalies (e.g., Pitch Tilt above 70% "
                "or PPDA below 8.0 indicating an intense high press) and summarize the trigger in 3 bullet points."
            ),
            tools=[mcp_tool]
        )

        tactical_agent = Agent(
            name="TacticalAnalystAgent",
            client=client,
            instructions=(
                "You are a Premier League Tactical Analyst. Given a statistical anomaly trigger, "
                "call inspect_zone_events to find the spatial cause (substitutions, half-space overloads, "
                "expected threat xT spikes). Explain the tactical mechanism causing the shift."
            ),
            tools=[mcp_tool]
        )

        philosophical_agent = Agent(
            name="PhilosophicalPunditAgent",
            client=client,
            instructions=(
                "You are a football philosopher rooted in the philosophy of sport (drawing on phenomenology, "
                "social practice theory, and sports aesthetics). Analyze the tactical shift through a philosophical lens: "
                "(1) Explain the individual player's mind and kinesthetic intent behind the decisive pass/movement as an "
                "embodied phenomenological choice rather than mechanical calculation. "
                "(2) Evaluate whether the team's build-up displays true collective synergy (operating as a cohesive 'social practice') "
                "versus being a disconnected collection of high-priced individual stars[cite: 68, 119]. "
                "(3) Comment on the aesthetic and moral beauty of the tactical pattern, emphasizing creative risk over cynical obstruction[cite: 141]."
            )
        )

        narrator_agent = Agent(
            name="BroadcastNarratorAgent",
            client=client,
            instructions=(
                "You are a live Premier League Broadcast Storyteller. Synthesize the technical data and the "
                "philosophical depth into two outputs: (1) A 2-sentence live commentary callout capturing both the tactical "
                "shift and its deeper meaning, and (2) A tactical alert telling fans which zone/player to watch next."
            )
        )

        state_res = await state_agent.run(f"Analyze match window {match_window}.")
        tactical_res = await tactical_agent.run(f"Window {match_window} telemetry trigger:\n{state_res.text}\nDiagnose the spatial tactics.")
        phil_res = await philosophical_agent.run(f"Telemetry:\n{state_res.text}\nTactical Diagnosis:\n{tactical_res.text}\nProvide the philosophical, phenomenological, and aesthetic breakdown.")
        story_res = await narrator_agent.run(f"Telemetry:\n{state_res.text}\nTactical Diagnosis:\n{tactical_res.text}\nPhilosophical Depth:\n{phil_res.text}\nGenerate final broadcast story and fan alert.")

        return {
            "window": match_window,
            "state_monitor_output": state_res.text,
            "tactical_analyst_output": tactical_res.text,
            "philosophical_output": phil_res.text,
            "broadcast_story_output": story_res.text
        }

@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PitchPulse AI | Tactical & Philosophical Intelligence</title>
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --accent-green: #22c55e;
            --accent-purple: #a855f7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 {
            margin: 0;
            font-size: 1.8rem;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .controls {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        select, button {
            background-color: var(--card-bg);
            color: var(--text-main);
            border: 1px solid var(--border);
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
        }
        button {
            background-color: var(--accent);
            color: var(--bg-dark);
            font-weight: bold;
            transition: opacity 0.2s;
        }
        button:hover {
            opacity: 0.9;
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
            gap: 20px;
        }
        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            font-size: 1.2rem;
            font-weight: 600;
        }
        .card-body {
            white-space: pre-wrap;
            line-height: 1.6;
            color: var(--text-muted);
            background-color: rgba(15, 23, 42, 0.5);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
            min-height: 120px;
            max-height: 300px;
            overflow-y: auto;
        }
        .badge {
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            font-weight: bold;
        }
        .badge-telemetry { background: #0284c7; color: #fff; }
        .badge-tactical { background: #0d9488; color: #fff; }
        .badge-philosophy { background: var(--accent-purple); color: #fff; }
        .badge-broadcast { background: var(--accent-green); color: #0f172a; }
        
        #loading {
            display: none;
            text-align: center;
            padding: 40px;
            font-size: 1.2rem;
            color: var(--accent);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ PitchPulse AI <span style="font-size: 1rem; color: var(--text-muted);">| Tactical & Philosophical Engine</span></h1>
            <div class="controls">
                <label for="windowSelect">Match Window:</label>
                <select id="windowSelect">
                    <option value="60-65">60' - 65' (Arsenal vs Liverpool)</option>
                </select>
                <button id="runBtn" onclick="runPipeline()">Run Multi-Agent Pipeline</button>
            </div>
        </header>

        <div id="loading">🤖 Multi-agent team collaborating across MCP server & Azure AI Foundry... Please wait...</div>

        <div class="grid" id="resultsGrid">
            <div class="card">
                <div class="card-header">
                    <span class="badge badge-telemetry">Agent 1</span> StateMonitorAgent (Telemetry)
                </div>
                <div class="card-body" id="stateOutput">Select a window and click run to analyze match telemetry anomalies...</div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span class="badge badge-tactical">Agent 2</span> TacticalAnalystAgent (Spatial Scout)
                </div>
                <div class="card-body" id="tacticalOutput">Spatial diagnosis will appear here...</div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span class="badge badge-philosophy">Agent 3</span> PhilosophicalPunditAgent (Existential/Aesthetics)
                </div>
                <div class="card-body" id="philOutput">Phenomenological and social practice breakdown will appear here...</div>
            </div>

            <div class="card" style="grid-column: 1 / -1;">
                <div class="card-header">
                    <span class="badge badge-broadcast">Agent 4</span> BroadcastNarratorAgent (Pundit & Fan Alert)
                </div>
                <div class="card-body" id="broadcastOutput" style="color: var(--text-main); font-weight: 500;">Live broadcast commentary and fan tactical alert will appear here...</div>
            </div>
        </div>
    </div>

    <script>
        async function runPipeline() {
            const btn = document.getElementById('runBtn');
            const loading = document.getElementById('loading');
            const windowVal = document.getElementById('windowSelect').value;

            btn.disabled = true;
            loading.style.display = 'block';

            document.getElementById('stateOutput').innerText = 'Analyzing telemetry...';
            document.getElementById('tacticalOutput').innerText = 'Diagnosing spatial events...';
            document.getElementById('philOutput').innerText = 'Reflecting through philosophy of sport...';
            document.getElementById('broadcastOutput').innerText = 'Synthesizing broadcast story...';

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ window: windowVal })
                });
                const data = await response.json();

                if (response.ok) {
                    document.getElementById('stateOutput').innerText = data.state_monitor_output;
                    document.getElementById('tacticalOutput').innerText = data.tactical_analyst_output;
                    document.getElementById('philOutput').innerText = data.philosophical_output;
                    document.getElementById('broadcastOutput').innerText = data.broadcast_story_output;
                } else {
                    alert('Error running pipeline: ' + (data.detail || 'Unknown error'));
                }
            } catch (err) {
                alert('Network error: ' + err.message);
            } finally {
                btn.disabled = false;
                loading.style.display = 'none';
            }
        }
    </script>
</body>
</html>
    """

@app.post("/analyze")
async def analyze_match(req: AnalysisRequest):
    try:
        results = await execute_pipeline(req.window)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:py" if False else "app:app", host="127.0.0.1", port=8000, reload=True)