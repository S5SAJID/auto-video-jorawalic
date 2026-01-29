from lib.ai.script_writer import generate_script
from utils import get_plain_script
from lib.speech_generation import generate_speech_with_word_timings
from lib.video.video_generator import generate_video

def generate_audio_video(title: str, audio_file_path="output.mp3", video_file_path="video.mp4", video_fps=24):
  try:
    # create script
    script = generate_script(video_title=title)

    # parse the segments and create audio
    plain_script = get_plain_script(script)
    audio_file_path, audio_word_timings = generate_speech_with_word_timings(text=plain_script,audio_file_path=audio_file_path)

    # generate the video
    generate_video(
      segments=script,
      word_timings=audio_word_timings,
      filename=video_file_path,
      fps=video_fps
    )
  
  except Exception as e:
    print(e)