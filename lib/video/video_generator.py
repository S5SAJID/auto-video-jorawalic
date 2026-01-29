from moviepy import TextClip, ColorClip, CompositeVideoClip, AudioFileClip, VideoFileClip, ImageClip
from utils.calculate.calculate_segment_durations import calculate_segment_durations
import subprocess
from lib.video.manim.manim_pipeline_manager.index import ManimPipelineManager
from lib.config import VID_GEN_CONFIG
import os
from lib.images_finder import find_images
from lib.rag.chromadb.search_gif_collection import search_gif_collection

VIDEO_SIZE = VID_GEN_CONFIG["VIDEO_SIZE"]
FONT_PATH = "data\\assets\\fonts\\BricolageGrotesque-SemiBold.ttf"


def generate_video(segments: list, word_timings: list, filename="video.mp4", fps=25, audio_file='output.mp3'):
  manim_manager = ManimPipelineManager()
  process_segments = calculate_segment_durations(segments=segments, word_timings=word_timings, include_se=True)
  
  bg = ColorClip(size=VIDEO_SIZE, color=(255,255,255), duration=word_timings[-1]["end"])

  audio_clip = AudioFileClip(filename=audio_file)
  txt_clips = []
  gif_clips = []
  img_clips = []
  manim_clips = []
  
  for sg_i, sg in enumerate(process_segments):
    txt = TextClip(
        text=" ".join(sg['words']), 
        font_size=28, 
        color=(10,10,10), 
        font=FONT_PATH,
        method='caption', 
        text_align="center",
        size=((int(VIDEO_SIZE[0]/1.5), int(VIDEO_SIZE[1]/2)))
      ).with_position(('center', 0 if sg['type'] != 'text' else 0.2), relative=True)\
        .with_start(sg["start_time"])\
        .with_end(sg['end_time'])\
        .with_duration(sg['duration'])
      
    if sg['type'] == 'gif':
      gif_path = search_gif_collection(sg['content'])
      gif_clip = VideoFileClip(gif_path).with_position(('center','center'))\
        .with_start(sg["start_time"])\
        .with_end(sg['end_time'])\
        .with_duration(sg['duration'])
      gif_clips.append(gif_clip)

    if sg['type'] == 'img':
      image_downloaded = find_images(sg['content'])

      img_clip = ImageClip(image_downloaded).resized(width=VIDEO_SIZE[0]/1.4)\
        .with_position(('center', .35), relative=True)\
        .with_start(sg["start_time"])\
        .with_end(sg['end_time'])\
        .with_duration(sg['duration'])
      img_clips.append(img_clip)

    if sg['type'] == 'manim':
      # 1. Generate Script
      script_path = "temp_manim_scene.py"
      script_content = manim_manager.get_render_script(sg['id'], sg['content'], sg['duration'])
      with open(script_path, "w") as f:
          f.write(script_content)

      # 2. Execute Manim
      # --transparent and --format=mov ensures you can overlay it in MoviePy
      subprocess.run([
          "manim", "-ql", "--transparent", "--format=mov", 
          script_path, "DynamicScene"
      ], check=True)

      # 3. Import back to MoviePy
      # Manim 2026 default path: media/videos/temp_manim_scene/480p15/DynamicScene.mov
      video_path = os.path.join("media", "videos", "temp_manim_scene", "480p15", "DynamicScene.mov")
      
      if os.path.exists(video_path):
          m_clip = VideoFileClip(video_path, has_mask=True)\
              .with_start(sg["start_time"])\
              .with_duration(sg['duration'])\
              .with_position(('center', 'center'))
          manim_clips.append(m_clip)

    txt_clips.append(txt)

  video = CompositeVideoClip([bg, *txt_clips, *gif_clips, *img_clips, *manim_clips]).with_audio(audioclip=audio_clip)
  video.write_videofile(filename=filename, fps=fps, 
    audio=True, # No audio as not needed
    codec="libx264", # libx264 is the default codec for H.264 video encoding
    preset="ultrafast",  # Key for maximum encoding speed
    threads=4            # Utilizes multi-core processing
  )