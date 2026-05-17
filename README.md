# 🌌 Mythos.OS // The Living Universe Engine

### 🎭 A Stateful, Multimodal Multi-Agent Collaborative Storytelling Engine
Built for the **AI Agent Olympics Hackathon // Milan AI Week**.

🚀 **Live Demo:** [Explore the Living Universe on Streamlit](https://milanaiweek2026-w9ekpagqojowxceteevcjq.streamlit.app/)  
📦 **Backend Processing:** Integrated Serverless Agentic Layer  
🎙️ **Voice Technology:** Speechmatics Voice Dictation Ecosystem  

---

## 📖 Project Overview

**Mythos.OS** is an advanced, stateful simulation sandbox designed to shift AI from simple chat-based co-pilots into complex, autonomous, collaborative decision-making networks. Instead of a user simply writing a fictional story, they collaborate with a synchronized swarm of specialized AI agents that dynamically build laws, generate concept art assets, act as strict logic referees, and dynamically roleplay in-character based on user interactions.

The core technical philosophy behind Mythos.OS is **Automated State Consistency**. By utilizing real-time voice processing and foundational rule-checking pipelines, the engine prevents narrative drift, enforces logical constraints, and simulates a living, breathing systemic world.

---

## 🛠️ The Multi-Agent Swarm Architecture

The entire platform orchestrates four distinct AI agent personas built using the **Google Gemini API**, working in a synchronous execution loop to maintain the state of the story world:

| Phase | Component | Underlying Model / Tool | Autonomous Responsibility |
| :--- | :--- | :--- | :--- |
| **Ingress** | 🎙️ **Voice Capture** | `Speechmatics API` | Handles real-time, accurate audio dictation to text stream. |
| **Core 1** | 🪐 **Universe Generator** | `gemini-1.5-flash` | Establishes environmental laws, global factions, and structural world boundaries. |
| **Core 2** | 🎨 **Visual Director** | `gemini-1.5-flash` | Extracts descriptive prompts and dynamically queries Pollinations AI for concept art. |
| **Core 3** | ⚖️ **Lore Keeper (The Referee)** | `gemini-1.5-pro` | Cross-references proposals against world rules. Emits structural `APPROVED` or `REJECTED` flags. |
| **Core 4** | 🎭 **Character Persona (Jack)** | `gemini-1.5-flash` | Processes downstream timeline updates and responds with active, in-character localized roleplay. |

---

### 🤖 Agent Roles & Internal Prompts

#### 1. The Universe Generator Agent
*   **Model:** `gemini-1.5-flash` (Optimized for speed and high-throughput initialization)
*   **Role:** The World Builder. When given a master aesthetic or high-level concept, this agent establishes the systemic boundaries, strict physical or magical laws, primary governing factions, and geographical parameters.

#### 2. The Visual Director Agent
*   **Model:** `gemini-1.5-flash`
*   **Role:** The Art Director. It programmatically reads the structural lore database emitted by the Universe Generator, extracts complex descriptive tags, and engineers visual prompt hooks to dynamically inject high-fidelity concept backgrounds directly into the client user interface.

#### 3. The Lore Keeper Agent
*   **Model:** `gemini-1.5-pro` (Utilized for heavy context cross-referencing and logic validation)
*   **Role:** The System Referee. When a user proposes a story action via voice dictation, the Lore Keeper cross-references the event proposal against the established world guidelines and the entire historical chronological ledger. It explicitly approves the timeline addition or rejects it with an explicit technical explanation if a logical contradiction is introduced.

#### 4. The Character Persona Agent ("Jack the Whisper Merchant")
*   **Model:** `gemini-1.5-flash`
*   **Role:** The Grassroots Perspective. Operating down-funnel from the Lore Keeper, this agent maintains its own localized state. If an event is approved, it reads the delta change to the universe and generates a targeted 1-3 sentence in-character contextual response showing how the event alters the black-market trade index or civilian lifestyle.

---

## ✨ Key Features & Technical Workflows

*   🎙️ **Voice-Driven Event Injection:** Users dictate continuous narrative adjustments completely hands-free utilizing the **Speechmatics API**, enabling rapid simulation iteration without reliance on manual typing interfaces.
*   ⚖️ **Autonomous Compliance Checks:** The system logic includes a dual-state verification loop. Illegal timeline modifications are caught instantly by the reasoning engine, showcasing edge-case handling without human intervention.
*   🎨 **Dynamic Glassmorphic Interface:** Custom UI styling featuring blurred containers, high-contrast typography shadows, and dynamic full-screen image streaming designed for maximum aesthetic fidelity during presentation panels.
*   📜 **Persistent Chronological Ledger:** Maintains a structured state timeline displaying historical entries side-by-side with localized roleplay outputs.

---

## 💻 Tech Stack & Ecosystem Integrations

*   **Frontend & Layout Framework:** Streamlit (Configured with Custom Injected Document Object Model CSS injections)
*   **Core Orchestration Engine:** Python 3.10+
*   **Reasoning LLMs:** Google Gemini API / Google AI Studio (`gemini-1.5-flash` & `gemini-1.5-pro`)
*   **Speech Processing Pipelines:** Speechmatics Batch/Streaming API
*   **Asset Synthesis Engine:** Pollinations AI 

---

 # 🚀 Local Installation & Deployment Guide

To run this platform locally on your machine for engineering evaluation, execute the following steps:

---

## 1. Clone the Repository

```bash
git clone https://github.com/rupikap009/milanAIWeek2026.git
cd milanAIWeek2026
```

---

## 2. Configure Environment Keys

Create a local secure configuration or configure your system environment variables with your active provider tokens.

### Unix/macOS Environment Injection

```bash
export GEMINI_API_KEY="your_google_studio_key_here"
export SPEECHMATICS_API_KEY="your_speechmatics_token_here"
```

### Windows PowerShell

```powershell
setx GEMINI_API_KEY "your_google_studio_key_here"
setx SPEECHMATICS_API_KEY "your_speechmatics_token_here"
```

---

## 3. Install Module Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Boot Up the Application Engine

Depending on your exact repository structure, launch using one of the following commands:

### If Running from the Root Workspace Directory

```bash
streamlit run app.py
```

### If the Application File is Inside the `frontend` Directory

```bash
streamlit run frontend/app.py
```

---

# 🔬 Test Case Scenarios

To verify the cross-agent coordination and state compliance loops under evaluation, test using the following pathways.

---

## 🧪 Test Case A — Automated Lore Validation Failure Loop

### Step 1 — Initialize Universe Concept

Provide the following prompt:

```text
A cyber-dystopian subterranean metropolis lit by magma where human emotions are legally prohibited by bio-scanners.
```

### Step 2 — Submit a Contradictory Action

```text
Suddenly, a magical portal opens and a medieval dragon flies through the city, prompting all the citizens to throw a happy celebration party without setting off any sensors.
```

### ✅ Expected Output

- The system detects the emotional and high-fantasy anomaly.
- The Lore Keeper triggers a `REJECTED` warning banner.
- The action is refused from being appended to the public history ledger.

---

## 🧪 Test Case B — Downstream Multi-Agent Context Adaptation Loop

### Step 1 — Initialize Universe Concept

Use the same magma city universe description above.

### Step 2 — Submit a Compliant Action

```text
Jack successfully updates his ocular cyberware firmware, allowing his eyes to mask his emotional fluctuations from the city surveillance grid.
```

### ✅ Expected Output

- The Lore Keeper flags the action as `APPROVED`.
- The event appends to the public history ledger.
- Jack the Whisper Merchant dynamically reacts to the successful system override event.

---

# 📝 Comprehensive Example Run 

## 1. User Voice/Text Input (System Trigger)

```text
A strike team of Apathy Enforcers raids the Lower Strata to seize forbidden historical diaries.
```

---

## 2. System Response (Multi-Agent Swarm Execution)

### ⚖️ Lore Keeper Agent — `[STATUS: APPROVED]`

> "The action is logical. The presence of Apathy Enforcers and the hunting of emotional artifacts matches the initialized corporate-dystopian laws of this universe."

---

### 🎭 Jack the Whisper Merchant


> # 📄 License

This project was developed for the **AI Agent Olympics Hackathon — Milan AI Week 2026**.
