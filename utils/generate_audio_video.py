from lib.ai.script_writer import generate_script
from utils.utils import get_plain_script
from lib.speech_generation import generate_speech_with_word_timings
from lib.video.video_generator import generate_video

def generate_audio_video(title: str, audio_file_path="output.mp3", video_file_path="video.mp4", video_fps=24):
  try:
    # create script
    yield "Generating script"
    script = generate_script(video_title=title)
    yield "Script generated"

    # parse the segments and create audio
    yield "Generating audio"
    plain_script = get_plain_script(script)
    audio_file_path, audio_word_timings = generate_speech_with_word_timings(text=plain_script,audio_file_path=audio_file_path)
    yield "Audio generated"

    # generate the video
    yield "Generating video"
    generate_video(
      segments=script,
      word_timings=audio_word_timings,
      filename=video_file_path,
      fps=video_fps
    )
    yield "Video generated"
  
  except Exception as e:
    print(e)