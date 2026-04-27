# Bio-Hack AI: The Autonomous Health & Performance OS

**Bio-Hack AI** is a production-grade agentic system designed to bridge the gap between "dumb" biometric data (steps, heart rate, sleep) and "subjective" human context (stress, diet, physical pain). 

While wearables track physiological spikes, they often lack the "why." Bio-Hack AI captures the missing middle—contextualizing data like a high heart rate during a stressful meeting versus a caffeine-induced spike—via low-friction voice input and structuring it for long-term physiological optimization.

---

## 🏗️ System Architecture & Tech Stack

The project utilizes a **Modular Agentic Architecture** powered by the **Model Context Protocol (MCP)**. This allows the AI to dynamically "plug in" to various data sources and specialized tools instead of relying on a static script.

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Brain (Inference)** | Groq + Llama 3.3 70B | High-speed reasoning and long-term data correlation. |
| **Ears (Transcription)** | Groq + Whisper | Near-instant transcription of Telegram voice notes. |
| **Skeleton (Orchestration)** | LangChain + LangGraph | State management to maintain consistent conversational flow. |
| **Storage (Memory)** | PostgreSQL + Redis | Stores raw logs, structured data, and session states. |
| **Human Frontend** | Notion | Mirrors the DB into a searchable, aesthetic "Life Session" gallery. |
| **Infrastructure** | Docker | Ensures identical environments from local dev to AWS. |

---

## ⚙️ The Functional Pipeline

### Phase A: The Event Trigger (Real-Time Polling)
The system runs a background worker that polls health APIs (e.g., Google Fit or specialized MCP servers). 
* **Detection:** The system notices a specific event, such as a "Deep Sleep" session ending or a "High Intensity" activity being logged.
* **Action:** It triggers the Telegram Bot to initiate a "Context Retrieval" sequence.

### Phase B: Subjective Capture (Telegram + Whisper)
The bot pings the user: *"I see a 45-minute HIIT session. Your recovery score is low today. Any specific reason?"*
1. **Voice Reply:** The user replies with a quick, natural voice note.
2. **Transcription:** Groq Whisper converts the audio to text instantaneously.
3. **Structuring:** Llama 3.3 "shreds" that text into a structured JSON object, identifying energy levels, soreness locations, and dietary notes.

### Phase C: The Correlation Engine (MCP + PostgreSQL)
Using MCP servers, the agent queries the PostgreSQL database to find longitudinal patterns.
* **Example Query:** *"Identify correlations between 'fasted training' and 'lower back' soreness over the last 30 days."*
* The agent writes the SQL, executes it via the DB-Server, and returns a natural language summary of the findings.

---

## 📊 Database Schema & Data Flow

To ensure the system is more than just a chatbot, the PostgreSQL backend uses a relational model to track progress and health trends.

| Table | Purpose |
| :--- | :--- |
| `raw_metrics` | Heart rate, calories, and sleep stages (from Health APIs). |
| `voice_logs` | Transcriptions and AI-extracted sentiments/tags. |
| `correlations` | AI-generated insights (e.g., "Lack of sleep leads to 20% lower workout volume"). |

---

## 💡 Why This Architecture Matters

* **Zero Friction:** You never have to open a spreadsheet. You simply talk to your "Archivist" while walking, driving, or cooling down from a workout.
* **Contextual Intelligence:** By using Llama 3.3 70B, the system interprets data rather than just storing it. If you mention "knee pain," it doesn't just save the text; it flags it as an **"Injury Risk"** in your Notion dashboard.
* **Infinite Extensibility:** Because of the MCP integration, you can easily add a "Weather MCP" to see if environment affects mood, or a "Spotify MCP" to see which music leads to peak performance.

---

## 🚀 Deployment 

### Local Development
The entire stack is containerized for a one-command setup:
```bash
docker-compose up