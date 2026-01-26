# Short Video Generator

A Python tool for generating short-form vertical videos by combining text overlays, animated GIFs, web images, and mathematical animations.

## Overview

This project generates TikTok/YouTube Shorts style videos from structured JSON input. Each video segment can contain text narration, emotion-based cat meme GIFs, web-sourced images, or Manim mathematical visualizations, all synchronized with AI-generated voiceover.

## Features

- **Text Overlays**: Synchronized captions with TTS narration
- **GIF Library**: Pre-downloaded cat memes organized by emotion (happy, sad, confused, etc.)
- **Image Search**: Automatic image downloading via Bing
- **Manim Integration**: Mathematical and scientific animations
- **Audio Generation**: ElevenLabs TTS with word-level timing
- **Video Composition**: MoviePy-based rendering at 720x1280 (vertical format)

## Requirements

- Python 3.12+
- Manim
- MoviePy
- ElevenLabs API key
- Bing Image Search credentials (optional)

## Installation

```bash
pip install -e .
```

Set up your `.env` file with:
```
ELEVENLABS_API_KEY=your_key_here
GIPHY_API_KEY=your_key_here
```

## Usage

Define your video segments in JSON format:

```python
segments = [
    {
        "type": "text",
        "content": "Your opening line",
        "words": ["Your", "opening", "line"]
    },
    {
        "type": "gif",
        "content": r"data\assets\gifs\surprised\*",
        "words": ["Mind", "blown"]
    },
    {
        "type": "img",
        "content": "search query for image",
        "words": ["supporting", "visuals"]
    },
    {
        "type": "manim",
        "id": "obj_1",
        "content": {
            "mobject": "Circle",
            "args": "color=BLUE",
            "action": "Create",
            "pos": "ORIGIN"
        },
        "words": ["animated", "circle"]
    }
]
```

Generate the video:

```python
from lib.video.video_generator import generate_video

generate_video(
    fps=10,
    segments=segments,
    word_timings=timings,
    audio_file='output.mp3'
)
```

## Project Structure

```
├── lib/
│   ├── speech_generation.py    # ElevenLabs TTS integration
│   ├── images_finder.py         # Bing image search
│   ├── gifs_finder.py           # Giphy API wrapper
│   └── video/
│       ├── video_generator.py   # Main video composition
│       └── manim/               # Manim scene generation
├── data/
│   └── assets/
│       └── gifs/                # Pre-downloaded GIF library
└── main.py                      # Example usage
```

## Content Types

### Text
Plain text overlays with synchronized narration.

### GIFs
Available emotion categories: `happy`, `angry`, `sad`, `confused`, `surprised`, `suspicious`, `dancing`, `cool`, `scared`, `sleepy`, `hungry`, `crying`, `judging`, `hacker`, `doctor`, `teacher`, `chef`, `firefighter`, `robber`.

### Images
Automatically downloaded from Bing based on search queries.

### Manim Animations
Supports geometric shapes, mathematical equations (LaTeX), and transformations. Three action types:
- **Create**: Initial object appearance
- **Modify**: Change position, rotation, color, or scale
- **Transform**: Morph into different shape

## AI-Assisted Content Generation

See `AI_VIDEO_GENERATION_PROMPT.md` for a detailed prompt to use with language models (GPT-4, Claude, Gemini) to automatically generate video scripts in the required JSON format.

## Limitations

- ElevenLabs API rate limits apply
- Manim rendering can be slow for complex animations
- GIF library is limited to pre-downloaded content
- Output quality depends on input segment timing and pacing

## License

This project is for educational and experimental purposes.

## Notes

This was built as a learning project to explore programmatic video generation. The code prioritizes simplicity over production readiness. Use at your own discretion.
