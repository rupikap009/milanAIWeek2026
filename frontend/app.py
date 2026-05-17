import streamlit as st
import requests
import time
import json

# Constants
BACKEND_URL = "http://127.0.0.1:8000"

# Setup Page Layout
st.set_page_config(
    page_title="Mythos.OS // The Living Universe Engine",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to fetch the current universe state
def fetch_universe():
    try:
        response = requests.get(f"{BACKEND_URL}/get-universe", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

# Fetch current state to render main dashboard
universe_data = fetch_universe()

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
            try:
                with st.spinner("Gemini Flash is spinning up the world lore & visual prompt..."):
                    response = requests.post(
                        f"{BACKEND_URL}/initialize-universe",
                        json={"prompt": universe_concept},
                        timeout=45
                    )
                    if response.status_code != 200:
                        try:
                            error_detail = response.json().get("detail", response.text)
                        except:
                            error_detail = response.text
                        st.error(f"Backend Error: {error_detail}")
                    else:
                        st.success("Universe successfully initialized!")
                        time.sleep(1) # Brief pause so the user sees the success message
                        st.rerun()  # Refresh the page state to show the new universe
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend. Is it running?\n\nDetails: {e}")

if universe_data is None:
    st.error("⚠️ Cannot connect to the Mythos.OS backend. Ensure the FastAPI server is running at http://127.0.0.1:8000.")
    st.stop()

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
                try:
                    files = {"file": ("recording.wav", audio_value, "audio/wav")}
                    resp = requests.post(f"{BACKEND_URL}/transcribe-audio", files=files, timeout=60)
                    if resp.status_code != 200:
                        try:
                            error_detail = resp.json().get("detail", resp.text)
                        except:
                            error_detail = resp.text
                        st.error(f"Speechmatics Error: {error_detail}")
                    else:
                        st.session_state.propose_input_field = resp.json().get("transcription", "")
                        st.success("Transcription complete! You can review and edit it below.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to reach transcription endpoint: {e}")
        
        proposed_event = st.text_input("Event Text:", key="propose_input_field")
        submit_button = st.button("Submit to Lore Keeper", type="primary")
        
        if submit_button:
            if not proposed_event.strip():
                st.warning("Please enter a proposed event.")
            else:
                try:
                    with st.spinner("The Lore Keeper is analyzing..."):
                        resp = requests.post(
                            f"{BACKEND_URL}/propose-event",
                            json={"proposed_event": proposed_event},
                            timeout=30
                        )
                        if resp.status_code != 200:
                            try:
                                error_detail = resp.json().get("detail", resp.text)
                            except:
                                error_detail = resp.text
                            st.error(f"Backend Error: {error_detail}")
                        else:
                            result = resp.json()
                            status = result.get("status")
                            details = result.get("details", "")
                            
                            if status == "APPROVED":
                                st.success(f"**APPROVED:** {details}")
                                # Clear the transcription cache
                                if "propose_input_field" in st.session_state:
                                    del st.session_state["propose_input_field"]
                                time.sleep(1.5)
                                st.rerun()
                            elif status == "REJECTED":
                                st.error(f"**REJECTED:** {details}")
                            else:
                                st.warning(f"**UNKNOWN RESPONSE:** {details}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to submit event. Backend error:\n\n{e}")

        timeline = universe_data.get("timeline", []) if universe_data else []
        
        st.divider()
        st.markdown("### Chronological History")
        if not timeline:
            st.write("*No events have occurred yet.*")
        else:
            # Display like a historic ledger
            for i, entry in enumerate(timeline, 1):
                with st.container(border=True):
                    # In our new schema, timeline is a list of dicts: {"event": "...", "reaction": "..."}
                    if isinstance(entry, dict):
                        st.markdown(f"**Event {i}:** {entry.get('event', '')}")
                        if entry.get("reaction"):
                            st.markdown(f"> *{entry.get('reaction')}*")
                    else:
                        # Fallback for old schema
                        st.markdown(f"**Event {i}**<br>{entry}", unsafe_allow_html=True)
    else:
        st.write("Initialize a universe before proposing events.")
