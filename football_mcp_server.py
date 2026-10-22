import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PremierLeagueTacticalMCP")

# Synthetic rolling match snapshots keyed by match minute window
MATCH_WINDOWS = {
    "60-65": {
        "score": "Arsenal 1 - 1 Liverpool",
        "possession_pct": {"Arsenal": 64, "Liverpool": 36},
        "pitch_tilt_final_third": {"Arsenal": 78.5, "Liverpool": 21.5},
        "ppda_pressing_index": {"Arsenal": 6.2, "Liverpool": 14.8},
        "key_events": [
            {"min": 61, "type": "substitution", "team": "Arsenal", "detail": "Inverted LB introduced; #8 pushed into right half-space"},
            {"min": 63, "type": "progressive_pass_cluster", "team": "Arsenal", "zone": "Right Half-Space (Zone 14)", "count": 7, "xT_added": 0.42},
            {"min": 64, "type": "high_turnover", "team": "Arsenal", "zone": "Opponent Defensive Third", "shots_generated": 2}
        ]
    }
}

@mcp.tool()
def get_tactical_window_metrics(window: str = "60-65") -> str:
    """Fetch aggregated tactical metrics (Pitch Tilt, PPDA press intensity, possession) for a 5-minute match window."""
    data = MATCH_WINDOWS.get(window, MATCH_WINDOWS["60-65"])
    return json.dumps({
        "window": window,
        "score": data["score"],
        "possession_pct": data["possession_pct"],
        "pitch_tilt_final_third": data["pitch_tilt_final_third"],
        "ppda_pressing_index": data["ppda_pressing_index"]
    })

@mcp.tool()
def inspect_zone_events(window: str = "60-65") -> str:
    """Fetch granular spatial events (substitutions, progressive pass clusters, expected threat xT, turnovers) for a match window."""
    data = MATCH_WINDOWS.get(window, MATCH_WINDOWS["60-65"])
    return json.dumps({"window": window, "events": data["key_events"]})

if __name__ == "__main__":
    mcp.run(transport="stdio")