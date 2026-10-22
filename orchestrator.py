import asyncio
import os
import sys
from dotenv import load_dotenv
from agent_framework import Agent, MCPStdioTool
from agent_framework.foundry import FoundryChatClient

load_dotenv()

class SimpleApiCredential:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def get_token(self, *scopes, **kwargs):
        class Token:
            def __init__(self, token):
                self.token = token
                self.expires_on = 32503680000
        return Token(self._api_key)

async def run_tactical_pipeline(match_window: str = "60-65") -> dict:
    credential = SimpleApiCredential(os.environ["AZURE_OPENAI_API_KEY"])
    
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=credential
    )

    # Connect to your local football MCP server via stdio
    mcp_tool = MCPStdioTool(
        name="football_telemetry_mcp",
        command=sys.executable,
        args=["football_mcp_server.py"]
    )

    async with mcp_tool:
        # Agent 1: Telemetry & Anomaly Detector
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

        # Agent 2: Spatial & Tactical Scout
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

        # Agent 3: Philosophical Pundit & Existential Analyst
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

        # Agent 4: Broadcast & Fan Storyteller
        narrator_agent = Agent(
            name="BroadcastNarratorAgent",
            client=client,
            instructions=(
                "You are a live Premier League Broadcast Storyteller. Synthesize the technical data and the "
                "philosophical depth into two outputs: (1) A 2-sentence live commentary callout capturing both the tactical "
                "shift and its deeper meaning, and (2) A tactical alert telling fans which zone/player to watch next."
            )
        )

        print(f"--- Running Multi-Agent Pipeline with Philosophical Layer for Window {match_window} ---\n")
        
        # Execute coordinated multi-agent steps
        state_res = await state_agent.run(f"Analyze match window {match_window}.")
        print(f"\n[1. StateMonitorAgent Output]:\n{state_res.text}")

        tactical_res = await tactical_agent.run(
            f"Window {match_window} telemetry trigger:\n{state_res.text}\nDiagnose the spatial tactics."
        )
        print(f"\n[2. TacticalAnalystAgent Output]:\n{tactical_res.text}")

        phil_res = await philosophical_agent.run(
            f"Telemetry:\n{state_res.text}\nTactical Diagnosis:\n{tactical_res.text}\n"
            "Provide the philosophical, phenomenological, and aesthetic breakdown of this passage of play."
        )
        print(f"\n[3. PhilosophicalPunditAgent Output]:\n{phil_res.text}")

        story_res = await narrator_agent.run(
            f"Telemetry:\n{state_res.text}\nTactical Diagnosis:\n{tactical_res.text}\n"
            f"Philosophical Depth:\n{phil_res.text}\nGenerate final broadcast story and fan alert."
        )
        print(f"\n[4. BroadcastNarratorAgent Output]:\n{story_res.text}")

        return {
            "window": match_window,
            "state_monitor_output": state_res.text,
            "tactical_analyst_output": tactical_res.text,
            "philosophical_output": phil_res.text,
            "broadcast_story_output": story_res.text
        }

if __name__ == "__main__":
    asyncio.run(run_tactical_pipeline("60-65"))