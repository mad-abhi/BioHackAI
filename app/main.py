import os
import time
import json        # <--- This was the missing piece!
import requests
import psycopg2
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

load_dotenv()

# --- EXISTING EXTRACTION LOGIC ---
def extract_health_data(user_input):
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"), temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract health metrics. Return ONLY raw JSON. Keys: 'energy_level', 'soreness_areas', 'diet_notes', 'mood'."),
        ("user", "{text}")
    ])
    chain = prompt | llm
    try:
        response = chain.invoke({"text": user_input})
        return response.content.replace("```json", "").replace("```", "").strip()
    except Exception as e:
        print(f"❌ Extraction Error: {e}")
        return None

def save_to_journal(raw_text, structured_json):
    conn = psycopg2.connect(host="db", database="bio_archive", user="user", password="password")
    cur = conn.cursor()
    cur.execute("INSERT INTO voice_journals (raw_transcript, structured_json) VALUES (%s, %s)", (raw_text, structured_json))
    conn.commit()
    cur.close()
    conn.close()

# --- NEW: WHISPER TRANSCRIPTION ---
def transcribe_voice(file_path):
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
    
    try:
        with open(file_path, "rb") as audio_file:
            # We explicitly define the filename as .ogg and the mime type
            files = {
                "file": ("voice_note.ogg", audio_file, "audio/ogg"),
                "model": (None, "whisper-large-v3"),
            }
            response = requests.post(url, headers=headers, files=files)
            
            # Debugging: See what Groq is actually returning in the container logs
            result = response.json()
            print(f"👂 Whisper Result: {result}")
            
            return result.get("text")
    except Exception as e:
        print(f"❌ Whisper Error: {e}")
        return None
    
def save_to_notion(transcript, structured_json):
    try:
        # Now that 'json' is imported, this will work
        data = json.loads(structured_json)
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {os.getenv('NOTION_TOKEN').strip()}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Fallback for energy value
        energy_val = data.get("energy_level")
        try:
            energy_val = float(energy_val) if energy_val is not None else 0
        except:
            energy_val = 0

        payload = {
            "parent": {"database_id": os.getenv("NOTION_DATABASE_ID").strip()},
            "properties": {
                "Name": {"title": [{"text": {"content": f"Entry: {time.strftime('%Y-%m-%d %H:%M')}"}}]},
                "Transcript": {"rich_text": [{"text": {"content": transcript}}]},
                "Energy": {"number": energy_val},
                "Mood": {"rich_text": [{"text": {"content": str(data.get("mood") or "None")}}]},
                "Diet": {"rich_text": [{"text": {"content": str(data.get("diet_notes") or "None")}}]}
            }
        }
        
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            print("📖 Synced to Notion successfully!")
        else:
            print(f"❌ Notion Error ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"❌ Notion Sync Logic Error: {e}")
        
# --- NEW: TELEGRAM HANDLER ---
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    # Use a unique name for concurrent messages
    file_path = f"voice_{update.message.message_id}.ogg"
    await voice_file.download_to_drive(file_path)
    
    await update.message.reply_text("👂 Listening to your note...")
    
    transcript = transcribe_voice(file_path)
    
    # Check if we actually heard anything
    if not transcript or len(transcript.strip()) < 2:
        await update.message.reply_text("🤔 I heard a voice note, but couldn't extract any words. Try speaking a bit louder!")
        if os.path.exists(file_path):
            os.remove(file_path)
        return

    # Process the valid transcript
    structured_data = extract_health_data(transcript)
        
    if structured_data:
        save_to_journal(transcript, structured_data) # Saves to Postgres
        save_to_notion(transcript, structured_data)  # Saves to Notion
        await update.message.reply_text(f"✅ Saved & Synced to Notion!")
    else:
        await update.message.reply_text("❌ Failed to structure data.")
    
    if os.path.exists(file_path):
        os.remove(file_path)
# --- MAIN RUNNER ---
if __name__ == "__main__":
    print("🚀 Bio-Archivist Telegram Bot is starting...")
    token = os.getenv("TELEGRAM_TOKEN")
    
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    app.run_polling()