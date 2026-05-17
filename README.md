# Multi-Agent Storytelling Project (Mythos.OS)

Welcome to **Mythos.OS // The Living Universe Engine**! This project is a robust, dynamic AI-driven platform that orchestrates multiple autonomous agents to create, maintain, and react to a developing story universe.

## 🏗️ Project Architecture

The project is built on a decoupled client-server architecture:

- **Backend (FastAPI)**: Acts as the central orchestrator handling all API logic, agent prompts, and state management (maintaining the universe database, timeline, and lore).
- **Frontend (Streamlit)**: A highly interactive, dark-themed user interface that dynamically updates based on the current state of the universe, featuring voice-input capabilities and dynamic background injection.

### AI Integrations
- **Google GenAI (Gemini 1.5 Flash)** for lightning-fast multi-agent reasoning, generation, and character roleplay.
- **Speechmatics API** for asynchronous, high-accuracy audio transcription of dictated story events.
- **Pollinations AI** for real-time, dynamic concept art generation.

## 🤖 The Multi-Agent Ecosystem

The platform utilizes four distinct AI agents, each with specialized system instructions, collaborating seamlessly:

1. **The Universe Generator Agent** (The World-Builder): Establishes core foundations, rules, geography, and primary factions.
2. **The Visual Director Agent** (The Art Director): Extracts visual keywords and generates immersive concept art backgrounds via Pollinations AI.
3. **The Lore Keeper Agent** (The Referee): Cross-references proposed events against lore and timeline, approving or rejecting with reasoning to avoid contradictions.
4. **The Character Persona Agent** ("Jack the Whisper Merchant"): Reacts strictly in-character to approved events, showing local impact.

## ✨ Key Features & User Flow

- **Master Universe Initialization**: Spin up an entirely new world from a simple text prompt.
- **Voice-Dictated Storytelling**: Use audio input to dictate proposed timeline events (via Speechmatics).
- **Chronological Ledger**: Persistent history of all approved events alongside in-character reactions.
- **Dynamic Theming & Glassmorphism**: Custom injected CSS for a premium, immersive aesthetic with frosted-glass containers and dynamic world map backgrounds.
