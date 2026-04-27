# BioHackAI: Voice-Powered Bio-Archivist 🧬🤖

BioHackAI is an intelligent, multi-container AI system designed to turn unstructured voice notes into a structured health and lifestyle dashboard. By combining high-end transcription (Whisper), large language model reasoning (Llama 3.3), and seamless cloud synchronization (Notion), it allows for frictionless personal data logging.

---

##  The Pipeline
1.  **Voice Input:** User sends a voice note to the Telegram Bot (Opus/OGG format).
2.  **Transcription:** Groq's **Whisper-large-v3** converts audio to high-accuracy text.
3.  **Data Extraction:** **Llama 3.3 70B** (via Groq API) parses the text into a structured JSON object (Energy, Mood, Diet, etc.).
4.  **Local Storage:** Data is stored in a **PostgreSQL** database for long-term analytics and privacy.
5.  **Cloud Dashboard:** The entry is synced to a **Notion Gallery** for a beautiful, human-readable UI.

---

##  Tools & Technologies Used

### **Core Infrastructure**
* **PostgreSQL:** Used as the primary relational database to maintain a permanent local archive of all voice transcripts and structured bio-data.
* **Docker & Docker Compose:** Orchestrates the multi-container environment, ensuring the Python application and database work together seamlessly.

### **AI & Reasoning**
* **Groq AI:** Leveraged for ultra-fast inference. 
    * **Whisper-large-v3:** High-fidelity speech-to-text transcription.
    * **Llama 3.3 70B:** Powerful LLM used to extract structured insights from conversational speech.
* **LangChain:** Framework used to manage the AI chains and prompt templates.

### **Integrations**
* **Telegram Bot API:** The user interface for the project, allowing for easy mobile data entry via voice notes.
* **Notion API:** Synchronizes structured data to a beautiful, customizable gallery dashboard for the user.

---

##  Skills Demonstrated
* **Artificial Intelligence:** Speech-to-Text (STT), LLM entity extraction, and prompt engineering.
* **Backend Development:** Python 3.11, asynchronous API handling with `python-telegram-bot`.
* **Data Architecture:** Relational schema design and SQL initialization.
* **DevOps:** Containerization, environment security (`.env`), and Git version control.

---

## 📦 Project Structure
```text
BioHackAI/
├── app/
│   ├── main.py         # Bot logic & API integrations
│   └── requirements.txt # Python dependencies
├── db/
│   └── init.sql        # Database schema initialization
├── docker-compose.yml  # Multi-container orchestration
└── .env                # API Keys (Protected)


| Component | Technology | Role |
| :--- | :--- | :--- |
| **Brain (Inference)** | Groq + Llama 3.3 70B | High-speed reasoning and long-term data correlation. |
| **Ears (Transcription)** | Groq + Whisper | Near-instant transcription of Telegram voice notes. |
| **Skeleton (Orchestration)** | LangChain + LangGraph | State management to maintain consistent conversational flow. |
| **Storage (Memory)** | PostgreSQL + Redis | Stores raw logs, structured data, and session states. |
| **Human Frontend** | Notion | Mirrors the DB into a searchable, aesthetic "Life Session" gallery. |
| **Infrastructure** | Docker | Ensures identical environments from local dev to AWS. |


### Local Development
The entire stack is containerized for a one-command setup:
```bash
docker-compose up --build -d