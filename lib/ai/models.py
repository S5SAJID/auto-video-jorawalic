from typing import Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator


class ManimContent(BaseModel):
    """Nested content structure for Manim animations."""
    mobject: Optional[str] = Field(None, description="Manim mobject class name (e.g., Circle, Square, MathTex)")
    args: Optional[str] = Field(None, description="Arguments for mobject creation (e.g., 'color=BLUE, fill_opacity=0.5')")
    action: Literal["Create", "Modify", "Transform"] = Field(..., description="Animation action type")
    pos: Optional[str] = Field(None, description="Position (e.g., 'ORIGIN', 'LEFT * 3')")
    move_to: Optional[str] = Field(None, description="Move to position (for Modify action)")
    rotate: Optional[str] = Field(None, description="Rotation angle (e.g., 'PI', 'PI/2')")
    scale: Optional[float] = Field(None, description="Scale factor")
    set_color: Optional[str] = Field(None, description="Color to set (for Modify action)")
    target_mobject: Optional[str] = Field(None, description="Target mobject for Transform action")
    target_args: Optional[str] = Field(None, description="Arguments for target mobject in Transform")


class TextSegment(BaseModel):
    """Text segment with narration."""
    type: Literal["text"] = Field(default="text")
    content: str = Field(..., description="Text content to display")
    words: list[str] = Field(..., description="Words for TTS synchronization")


class GifSegment(BaseModel):
    """GIF segment with emotion-based search."""
    type: Literal["gif"] = Field(default="gif")
    content: str = Field(..., description="Search query for GIF retrieval (max 5-8 words)")
    words: list[str] = Field(..., description="Words for TTS synchronization")


class ImageSegment(BaseModel):
    """Image segment with Bing search."""
    type: Literal["img"] = Field(default="img")
    content: str = Field(..., description="Search query for image download")
    words: list[str] = Field(..., description="Words for TTS synchronization")


class ManimSegment(BaseModel):
    """Manim animation segment with nested content."""
    type: Literal["manim"] = Field(default="manim")
    id: str = Field(..., description="Unique identifier for tracking object across segments")
    content: ManimContent = Field(..., description="Manim animation properties")
    words: list[str] = Field(..., description="Words for TTS synchronization")

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Manim segment must have a non-empty id")
        return v


# Discriminated union for type-safe segment handling
Segment = Union[TextSegment, GifSegment, ImageSegment, ManimSegment]


class VideoScriptOutput(BaseModel):
    """Complete video script with multiple segments."""
    segments: list[Segment] = Field(..., description="List of video segments in sequence")

    @field_validator('segments')
    @classmethod
    def validate_segments(cls, v: list[Segment]) -> list[Segment]:
        if not v:
            raise ValueError("Video script must have at least one segment")
        return v

