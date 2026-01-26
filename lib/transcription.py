import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(audio_file_path: str):
  config = aai.TranscriptionConfig(speech_models=["universal"])
  transcript = aai.Transcriber(config=config).transcribe(audio_file)

  if transcript.status == "error":
    raise RuntimeError(f"Transcription failed: {transcript.error}")

  return transcript