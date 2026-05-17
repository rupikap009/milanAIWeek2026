from fastapi import FastAPI, HTTPException
import os
import random
import urllib.parse
from fastapi import UploadFile, File
from pydantic import BaseModel
from google import genai
from google.genai import types
from speechmatics.batch import AsyncClient, TranscriptionConfig

app = FastAPI(title="Multi-Agent Storytelling API")

@app.get("/")
def home():
    return {"message": "Mythos.OS Backend is running! Go to /docs to test the agents."}

client = genai.Client()

universe_database = {
    "world_lore": "",
    "visual_url": "",
    "timeline": [],
    "characters": []
}

class UniverseInitRequest(BaseModel):
    prompt: str

class EventProposalRequest(BaseModel):
    proposed_event: str

@app.post("/initialize-universe")
def initialize_universe(request: UniverseInitRequest):
    try:
        # Agent 1: Universe Generator
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=request.prompt,
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
        # Append random seed to prevent any caching for the dynamic shift test case
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={random.randint(1, 1000000)}"
        
        universe_database["world_lore"] = response.text
        universe_database["visual_url"] = image_url
        universe_database["timeline"] = []
        universe_database["characters"] = []
        
        return {
            "message": "Universe initialized successfully",
            "lore": universe_database["world_lore"],
            "visual_url": universe_database["visual_url"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/propose-event")
def propose_event(request: EventProposalRequest):
    if not universe_database["world_lore"]:
        raise HTTPException(
            status_code=400, 
            detail="Universe has not been initialized. Call /initialize-universe first."
        )
        
    context = f"Existing World Lore:\n{universe_database['world_lore']}\n\n"
    
    context += "Current Timeline:\n"
    if not universe_database["timeline"]:
        context += "No events have occurred yet.\n"
    else:
        for idx, entry in enumerate(universe_database["timeline"], 1):
            context += f"{idx}. {entry['event']}\n"
            
    context += f"\nProposed New Event:\n{request.proposed_event}"
    
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
                f"Universe Lore:\n{universe_database['world_lore']}\n\n"
                f"Approved Event: {request.proposed_event}\n\n"
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
                "event": request.proposed_event,
                "reaction": f"**[CHANNEL_JACK_INTERNAL]:** \"{reaction}\""
            }
            universe_database["timeline"].append(timeline_entry)
            return {"status": "APPROVED", "details": decision}
            
        elif decision.startswith("REJECTED:") or "REJECTED" in decision.upper():
            return {"status": "REJECTED", "details": decision}
        else:
            return {"status": "UNKNOWN", "details": decision, "warning": "Could not determine agent decision"}
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lore checking failed: {str(e)}")

@app.get("/get-universe")
def get_universe():
    return universe_database

@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    api_key = os.environ.get("SPEECHMATICS_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, 
            detail="SPEECHMATICS_API_KEY is not set in the environment variables."
        )
    
    # Save the uploaded file to a temporary location
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
            
        # Call Speechmatics Batch API (Async)
        sm_client = AsyncClient(api_key=api_key)
        config = TranscriptionConfig(language="en")
        
        result = await sm_client.transcribe(
            audio_file=temp_file_path,
            transcription_config=config
        )
        await sm_client.close()
        
        return {"transcription": result.transcript_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
