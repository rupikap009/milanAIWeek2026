import streamlit as st
import os
import random
import urllib.parse
import time
import asyncio
from google import genai
from google.genai import types
from speechmatics.batch import AsyncClient, TranscriptionConfig

# Setup Page Layout
st.set_page_config(
    page_title="Mythos.OS // The Living Universe Engine",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. READ KEYS SAFELY FROM STREAMLIT SECRETS ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    SPEECHMATICS_KEY = st.secrets["SPEECHMATICS_API_KEY"]
except KeyError as e:
    st.error(f"Missing Secret: {e}. Please add it to Streamlit Secrets or local .streamlit/secrets.toml")
    st.stop()

# --- 2. INITIALIZE CLIENTS & STATE ---
client = genai.Client(api_key=GEMINI_KEY)

if "universe_database" not in st.session_state:
    st.session_state.universe_database = {
        "world_lore": "",
        "visual_url": "",
        "timeline": [],
        "characters": []
    }

# --- 3. DEFINE AGENT WORKFLOWS ---
def initialize_universe(prompt):
    try:
        # Agent 1: Universe Generator
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are the Universe Generator Agent. Your task is to establish the core world "
                    "foundations, rules, geography, and primary factions based on the user's prompt. "
                    "Provide a cohesive and engaging overview of this universe."
                )
            )
        )
        
        # Agent 2: Visual Director
        visual_prompt_response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=f"Extract visual keywords to create a gorgeous concept art background for this universe lore. Make it a detailed prompt for an AI image generator (comma separated keywords, highly detailed, vivid). No text in image.\n\nLore:\n{response.text}",
            config=types.GenerateContentConfig(
                system_instruction="You are a Visual Director Agent. Output only the comma-separated prompt for image generation, nothing else."
            )
        )
        
        encoded_prompt = urllib.parse.quote(visual_prompt_response.text.strip())
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={random.randint(1, 1000000)}"
        
        st.session_state.universe_database["world_lore"] = response.text
        st.session_state.universe_database["visual_url"] = image_url
        st.session_state.universe_database["timeline"] = []
        st.session_state.universe_database["characters"] = []
        
        return True, "Universe initialized successfully"
    except Exception as e:
        return False, str(e)

def propose_event(proposed_event_text):
    if not st.session_state.universe_database["world_lore"]:
        return "ERROR", "Universe has not been initialized."
        
    context = f"Existing World Lore:\n{st.session_state.universe_database['world_lore']}\n\n"
    
    context += "Current Timeline:\n"
    if not st.session_state.universe_database["timeline"]:
        context += "No events have occurred yet.\n"
    else:
        for idx, entry in enumerate(st.session_state.universe_database["timeline"], 1):
            context += f"{idx}. {entry['event']}\n"
            
    context += f"\nProposed New Event:\n{proposed_event_text}"
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=context,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are the Lore Keeper Agent. You receive the existing world lore, the current "
                    "timeline history, and a new proposed event. You must check the new proposed event "
                    "for any logical or chronological contradictions against the lore and timeline.\n"
                    "You must strictly prefix your response with either 'APPROVED:' or 'REJECTED:' "
                    "followed by your reasoning."
                )
            )
        )
        
        decision = response.text.strip()
        
        if decision.startswith("APPROVED:") or "APPROVED" in decision.upper():
            # Agent 3: Character Agent (Jack the Whisper Merchant Persona)
            character_prompt = (
                f"Universe Lore:\n{st.session_state.universe_database['world_lore']}\n\n"
                f"Approved Event: {proposed_event_text}\n\n"
                "React to this event in-character as Jack the Whisper Merchant. "
                "Provide a 1-3 sentence reaction showing how this event impacts your black-market network or the local populace."
            )
            try:
                char_response = client.models.generate_content(
                    model='gemini-flash-lite-latest',
                    contents=character_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a Character Agent (Jack the Whisper Merchant). React strictly in-character to the event."
                    )
                )
                reaction = char_response.text.strip()
            except Exception:
                reaction = "*Jack goes offline...*"
                
            timeline_entry = {
                "event": proposed_event_text,
                "reaction": f"**[CHANNEL_JACK_INTERNAL]:** \"{reaction}\""
            }
            st.session_state.universe_database["timeline"].append(timeline_entry)
            return "APPROVED", decision
            
        elif decision.startswith("REJECTED:") or "REJECTED" in decision.upper():
            return "REJECTED", decision
        else:
            return "UNKNOWN", decision
                
    except Exception as e:
        return "ERROR", str(e)

async def transcribe_audio_async(audio_bytes):
    temp_file_path = f"temp_st_{random.randint(1000,9999)}.wav"
    try:
        with open(temp_file_path, "wb") as f:
            f.write(audio_bytes)
            
        sm_client = AsyncClient(api_key=SPEECHMATICS_KEY)
        config = TranscriptionConfig(language="en")
        
        result = await sm_client.transcribe(
            audio_file=temp_file_path,
            transcription_config=config
        )
        await sm_client.close()
        return True, result.transcript_text
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def transcribe_audio(audio_bytes):
    return asyncio.run(transcribe_audio_async(audio_bytes))

# --- 4. STREAMLIT UI CODE ---
universe_data = st.session_state.universe_database

# Dynamic Background Injection
if universe_data and universe_data.get("visual_url"):
    visual_url = universe_data["visual_url"]
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.85)), url("{visual_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Enhance text readability against dark background */
        h1, h2, h3, p, .stMarkdown, .stText {{
            color: #f0f2f6 !important;
            text-shadow: 0px 2px 4px rgba(0,0,0,0.8);
        }}
        .stContainer > div {{
            background: rgba(20, 20, 20, 0.6) !important;
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# App Headers
st.title("🌌 Mythos.OS // The Living Universe Engine")
st.caption("Powered by Gemini Flash Lite & Speechmatics")
st.markdown("---")

# Sidebar - Universe Initialization
with st.sidebar:
    st.header("🛠️ Universe Controls")
    
    universe_concept = st.text_area(
        "Master Universe Concept",
        placeholder="e.g., A cyberpunk city where emotions are strictly illegal..."
    )
    
    if st.button("Initialize Universe", type="primary"):
        if not universe_concept.strip():
            st.warning("Please provide a concept before initializing.")
        else:
            with st.spinner("Gemini Flash is spinning up the world lore & visual prompt..."):
                success, msg_or_error = initialize_universe(universe_concept)
                if not success:
                    st.error(f"Generation Error: {msg_or_error}")
                else:
                    st.success("Universe successfully initialized!")
                    time.sleep(1)
                    st.rerun()

# Main Dashboard Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🪐 Core World Lore & Laws")
    lore = universe_data.get("world_lore", "")
    
    if lore:
        with st.container(border=True):
            st.markdown(lore)
    else:
        st.info("The universe is currently an empty void. Use the sidebar to initialize a new world.")

with col2:
    st.subheader("📜 The Timeline & Event Proposer")
    
    if lore:
        st.markdown("### Propose Next Event")
        
        audio_value = st.audio_input("Dictate via Speechmatics (Batch)")
        if audio_value and st.button("Transcribe Recording"):
            with st.spinner("Transcribing with Speechmatics..."):
                audio_bytes = audio_value.getvalue()
                success, result = transcribe_audio(audio_bytes)
                if not success:
                    st.error(f"Speechmatics Error: {result}")
                else:
                    st.session_state.propose_input_field = result
                    st.success("Transcription complete! You can review and edit it below.")
        
        proposed_event = st.text_input("Event Text:", key="propose_input_field")
        submit_button = st.button("Submit to Lore Keeper", type="primary")
        
        if submit_button:
            if not proposed_event.strip():
                st.warning("Please enter a proposed event.")
            else:
                with st.spinner("The Lore Keeper is analyzing..."):
                    status, details = propose_event(proposed_event)
                    
                    if status == "APPROVED":
                        st.success(f"**APPROVED:** {details}")
                        if "propose_input_field" in st.session_state:
                            del st.session_state["propose_input_field"]
                        time.sleep(1.5)
                        st.rerun()
                    elif status == "REJECTED":
                        st.error(f"**REJECTED:** {details}")
                    elif status == "ERROR":
                        st.error(f"**ERROR:** {details}")
                    else:
                        st.warning(f"**UNKNOWN RESPONSE:** {details}")

        timeline = universe_data.get("timeline", [])
        
        st.divider()
        st.markdown("### Chronological History")
        if not timeline:
            st.write("*No events have occurred yet.*")
        else:
            # Display like a historic ledger
            for i, entry in enumerate(timeline, 1):
                with st.container(border=True):
                    if isinstance(entry, dict):
                        st.markdown(f"**Event {i}:** {entry.get('event', '')}")
                        if entry.get("reaction"):
                            st.markdown(f"> *{entry.get('reaction')}*")
                    else:
                        st.markdown(f"**Event {i}**<br>{entry}", unsafe_allow_html=True)
    else:
        st.write("Initialize a universe before proposing events.")
