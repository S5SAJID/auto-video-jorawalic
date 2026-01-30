import json
import os
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from lib.ai.models import VideoScriptOutput

load_dotenv()
# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_BASE_URL"),
)

@lru_cache(maxsize=1)
def _load_system_prompt(pov_style: bool = False) -> str:
    """Load and cache the system prompt from markdown file."""
    with open("AI_VIDEO_GENERATION_PROMPT.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()
        system_prompt += "\n\n Important: \n - For now dont use manim. \n - Use the image search query as if you are searching on google search. \n - For explanatory videos use alot more images"
    
    if pov_style:
        system_prompt += "\n\nFor now the video should be in meme POV style"
    return system_prompt


def generate_script(
    video_title: str,
    enable_pov_style: bool = False
) -> VideoScriptOutput:
    """
    Generate a video script using AI based on the provided title.
    
    Args:
        video_title: The title/topic for the video
        enable_pov_style: Whether to enable POV meme style
        max_retries: Maximum number of retry attempts on failure
    
    Returns:
        VideoScriptOutput: Validated video script with segments
    
    Raises:
        OpenAIError: If API call fails after retries
        ValueError: If generated script is invalid
    """
    if not video_title or not video_title.strip():
        raise ValueError("Video title cannot be empty")
    
    system_prompt = _load_system_prompt(enable_pov_style)

    response = client.chat.completions.create(
        model=os.getenv("AI_MODEL"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": video_title}
        ]
    )

    gen_resp = response.choices[0].message.content.replace("```json", "").replace("```", "")
    
    # Parse and validate response
    script_data = json.loads(gen_resp)
    
    return script_data


if __name__ == "__main__":
    try:
        script = generate_script("POV: Startup founder in KPK with 0 rupees", enable_pov_style=True)
        print(f"Generated script with {len(script.segments)} segments")
        for i, segment in enumerate(script.segments, 1):
            print(f"{i}. Type: {segment.type}, Words: {' '.join(segment.words)}")
    except Exception as e:
        print(f"Script generation failed: {e}")
        raise