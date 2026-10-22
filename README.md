# ⚡ PitchPulse AI: Real-Time Premier League Tactical & Philosophical Intelligence

> **"A football match is not just a scoreline; it is a living narrative of human agency, space, and collective spirit."**

PitchPulse AI is a multi-agent artificial intelligence system built for the **Inside the Game: Developer Hackathon**. It bridges the gap between raw match telemetry, advanced spatial tactics, and the **philosophy of sport**, transforming live football data into rigorous tactical diagnoses and existential broadcast commentary.

---

## 🏆 Project Vision & Originality

While standard sports analytics engines output cold statistics (possession percentages, shots on target), **PitchPulse AI** asks the deeper questions inspired by the philosophy of sport (e.g., Heather L. Reid, _Introduction to the Philosophy of Sport_):

1. **Kinesthetic Intent & Phenomenology:** How does an individual pass reflect an embodied, phenomenological choice rather than a mechanical calculation?
2. **Collective Intentionality:** Can we detect whether a club has truly "teamed up" as a cohesive social practice, or if they are merely a disconnected collection of high-priced individual stars?
3. **Aesthetic & Moral Beauty:** Does the build-up celebrate creative risk and human flourishing over cynical obstruction?

---

## 🏗️ System Architecture & Tech Stack

PitchPulse AI is built using a modern, robust enterprise stack:

- **AI Orchestration & LLMs:** Microsoft Azure AI Foundry (`gpt-5-mini-1`) powered by the **Microsoft Agent Framework**.
- **Data Integration:** Custom Model Context Protocol (**MCP**) server serving rolling match telemetry and spatial zone events.
- **Backend Dashboard:** FastAPI asynchronous web server.
- **Frontend:** Modern, dark-themed responsive web dashboard.

---

## 🤖 The Multi-Agent Pipeline

The core intelligence is driven by four specialized agents collaborating in a coordinated pipeline:

1. **`StateMonitorAgent` (Telemetry & Anomaly Watchdog):** Queries the MCP server to track rolling windows (e.g., Pitch Tilt, PPDA pressing intensity) and isolates statistical anomalies.
2. **`TacticalAnalystAgent` (Spatial Scout):** Pinpoints the physical causes of anomalies—such as inverted fullbacks, Zone 14 overloads, and expected threat ($xT$) spikes.
3. **`PhilosophicalPunditAgent` (Existential & Aesthetic Analyst):** Applies frameworks from the philosophy of sport to evaluate player psychology, team synergy, and aesthetic beauty.
4. **`BroadcastNarratorAgent` (Live Pundit & Storyteller):** Synthesizes technical telemetry and philosophical depth into live broadcast commentary callouts and precise fan tactical alerts.

---

## 🚀 Quickstart & Installation

### 1. Clone & Set Up Environment

```bash
git clone [https://github.com/your-username/pitchpulse-ai.git](https://github.com/your-username/pitchpulse-ai.git)
cd pitchpulse-ai
python -m venv .venv
```
