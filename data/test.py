#!/usr/bin/env python3
"""
Device Mockup Video Creator using MoviePy
Recreates the exact animations from the HTML version
"""

from moviepy.editor import (
    VideoClip, ImageClip, CompositeVideoClip, ColorClip,
    AudioFileClip, concatenate_videoclips, VideoFileClip
)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import json
import os
import math
from typing import List, Dict, Tuple, Optional


class DeviceMockupVideoCreator:
    """Creates animated videos with device mockup frame, GIFs, and text animations."""
    
    def __init__(
        self,
        device_width: int = 300,
        fps: int = 30,
        font_path: Optional[str] = None
    ):
        """
        Initialize the video creator.
        
        Args:
            device_width: Width of the device mockup in pixels
            fps: Frames per second for the output video
            font_path: Path to custom font file (optional)
        """
        # Device dimensions (9:16 aspect ratio)
        self.device_width = device_width
        self.device_height = int(device_width * 16 / 9)
        self.border_size = 12
        self.screen_width = self.device_width - (self.border_size * 2)
        self.screen_height = self.device_height - (self.border_size * 2)
        self.fps = fps
        
        # Colors matching HTML CSS
        self.device_border_color = (17, 17, 17)  # #111
        self.screen_bg_color = (248, 249, 250)  # #f8f9fa
        self.text_color = (51, 51, 51)  # #333
        self.white = (255, 255, 255)
        
        # GIF container settings
        self.gif_container_size = 150
        self.gif_shadow_color = (0, 0, 0, 26)  # 0.1 opacity black
        self.gif_shadow_blur = 15
        self.gif_shadow_offset = 5
        
        # Text settings
        self.font_size = 24
        self.word_margin = 4
        self.font = self._load_font(font_path)
        
        # Animation timing (matching HTML)
        self.word_animation_duration = 0.3  # 300ms
        self.word_delay = 0.15  # 150ms between words
        self.element_scale_duration = 0.5  # 500ms for scale animation
        
    def _load_font(self, font_path: Optional[str] = None) -> ImageFont.FreeTypeFont:
        """Load the font, trying Comic Sans MS first, then fallbacks."""
        font_candidates = [
            font_path,
            "Comic Sans MS",
            "comic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Supplemental/Comic Sans MS.ttf",
            "C:\\Windows\\Fonts\\comic.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]
        
        for font in font_candidates:
            if font:
                try:
                    return ImageFont.truetype(font, self.font_size)
                except (IOError, OSError):
                    continue
        
        print("Warning: Using default font. Install Comic Sans MS for best results.")
        return ImageFont.load_default()
    
    def _ease_out_quad(self, t: float) -> float:
        """Quadratic ease-out function matching anime.js easeOutQuad."""
        return 1 - (1 - t) ** 2
    
    def _ease_out_elastic(self, t: float) -> float:
        """Elastic ease-out function matching anime.js easeOutElastic."""
        if t == 0:
            return 0
        if t == 1:
            return 1
        
        p = 0.3
        s = p / 4
        return pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1
    
    def create_device_frame(self) -> Image.Image:
        """Create the device mockup frame with border."""
        # Create the device with border
        img = Image.new('RGBA', (self.device_width, self.device_height), 
                        (*self.device_border_color, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw screen area (inner rectangle)
        screen_rect = [
            self.border_size,
            self.border_size,
            self.device_width - self.border_size,
            self.device_height - self.border_size
        ]
        draw.rectangle(screen_rect, fill=(*self.screen_bg_color, 255))
        
        return img
    
    def create_circular_container(
        self,
        content: Image.Image,
        size: int,
        add_shadow: bool = True
    ) -> Image.Image:
        """
        Create a circular container with optional shadow.
        
        Args:
            content: Image to put in the container
            size: Diameter of the circular container
            add_shadow: Whether to add drop shadow
        """
        # Resize content to fit container
        content = content.convert('RGBA')
        content = content.resize((size, size), Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, size - 1, size - 1], fill=255)
        
        # Create white background circle
        circle_bg = Image.new('RGBA', (size, size), (*self.white, 255))
        
        # Apply circular mask to content
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(circle_bg, (0, 0), mask)
        output.paste(content, (0, 0), mask)
        
        if add_shadow:
            # Create larger canvas for shadow
            shadow_expand = 30
            canvas_size = size + shadow_expand * 2
            result = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            
            # Create shadow
            shadow = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_offset = self.gif_shadow_offset
            shadow_draw.ellipse([
                shadow_expand + shadow_offset,
                shadow_expand + shadow_offset,
                shadow_expand + size + shadow_offset,
                shadow_expand + size + shadow_offset
            ], fill=(0, 0, 0, 40))
            shadow = shadow.filter(ImageFilter.GaussianBlur(self.gif_shadow_blur))
            
            # Composite shadow and content
            result = Image.alpha_composite(result, shadow)
            result.paste(output, (shadow_expand, shadow_expand), output)
            
            return result
        
        return output
    
    def load_gif_as_frames(
        self,
        gif_path: str,
        target_size: int = None
    ) -> Tuple[List[Image.Image], List[float]]:
        """
        Load a GIF file and return its frames and durations.
        
        Args:
            gif_path: Path to the GIF file
            target_size: Target size for resizing (optional)
            
        Returns:
            Tuple of (list of PIL Images, list of frame durations in seconds)
        """
        if target_size is None:
            target_size = self.gif_container_size
            
        try:
            gif = Image.open(gif_path)
            frames = []
            durations = []
            
            try:
                while True:
                    # Convert frame to RGBA
                    frame = gif.copy().convert('RGBA')
                    
                    # Create circular container with shadow
                    frame = self.create_circular_container(frame, target_size, add_shadow=True)
                    
                    frames.append(frame)
                    # GIF duration is in milliseconds
                    durations.append(gif.info.get('duration', 100) / 1000.0)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass
            
            if not frames:
                raise ValueError("No frames found in GIF")
                
            return frames, durations
            
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {e}")
            # Return placeholder
            placeholder = Image.new('RGBA', (target_size, target_size), (200, 200, 200, 255))
            placeholder = self.create_circular_container(placeholder, target_size)
            return [placeholder], [0.1]
    
    def create_text_frame(
        self,
        words: List[str],
        time: float,
        max_width: int = None
    ) -> Image.Image:
        """
        Create a text frame with word-by-word animation.
        
        Args:
            words: List of words to display
            time: Current time in the animation
            max_width: Maximum width for text area
        """
        if max_width is None:
            max_width = int(self.screen_width * 0.9)
        
        # Calculate which words are visible and their animation state
        visible_words = []
        
        for i, word in enumerate(words):
            word_start_time = i * self.word_delay
            
            if time < word_start_time:
                # Word hasn't started animating yet
                break
            
            word_time = time - word_start_time
            progress = min(word_time / self.word_animation_duration, 1.0)
            
            # Apply easeOutQuad
            eased_progress = self._ease_out_quad(progress)
            
            # Calculate opacity and Y offset
            opacity = eased_progress
            y_offset = 10 * (1 - eased_progress)  # translateY from 10 to 0
            
            visible_words.append({
                'word': word,
                'opacity': opacity,
                'y_offset': y_offset
            })
        
        # Create image for text
        img = Image.new('RGBA', (max_width, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate total text width for centering
        total_width = 0
        word_widths = []
        for word_info in visible_words:
            bbox = draw.textbbox((0, 0), word_info['word'], font=self.font)
            width = bbox[2] - bbox[0]
            word_widths.append(width)
            total_width += width + self.word_margin
        
        if total_width > 0:
            total_width -= self.word_margin  # Remove last margin
        
        # Start position for centering
        x_offset = (max_width - total_width) // 2
        base_y = 30
        
        # Draw each word
        for i, word_info in enumerate(visible_words):
            alpha = int(255 * word_info['opacity'])
            y_pos = base_y + word_info['y_offset']
            
            color = (*self.text_color, alpha)
            draw.text((x_offset, y_pos), word_info['word'], font=self.font, fill=color)
            
            x_offset += word_widths[i] + self.word_margin
        
        return img
    
    def create_gif_clip(
        self,
        gif_path: str,
        duration: float,
        position: Tuple[int, int] = None
    ) -> VideoClip:
        """
        Create a video clip from a GIF with scale-in animation.
        
        Args:
            gif_path: Path to the GIF file
            duration: Duration of the clip
            position: (x, y) position or 'center'
        """
        frames, frame_durations = self.load_gif_as_frames(gif_path)
        
        if not frames:
            return None
        
        frame_size = frames[0].size
        
        def make_frame(t):
            # Calculate which frame to show (loop the GIF)
            total_gif_duration = sum(frame_durations)
            if total_gif_duration == 0:
                return np.array(frames[0])
            
            t_mod = t % total_gif_duration
            cumulative = 0
            
            for i, d in enumerate(frame_durations):
                cumulative += d
                if t_mod < cumulative:
                    return np.array(frames[i])
            
            return np.array(frames[-1])
        
        # Create base clip
        clip = VideoClip(make_frame, duration=duration)
        
        # Apply elastic scale-in animation
        def resize_func(t):
            if t >= self.element_scale_duration:
                return 1.0
            
            progress = t / self.element_scale_duration
            eased = self._ease_out_elastic(progress)
            # Scale from 0.8 to 1.0
            return 0.8 + 0.2 * eased
        
        clip = clip.resize(resize_func)
        
        # Apply fade-in
        def opacity_func(t):
            if t >= self.element_scale_duration:
                return 1.0
            progress = t / self.element_scale_duration
            return self._ease_out_elastic(progress)
        
        clip = clip.set_opacity(opacity_func)
        
        return clip
    
    def create_icon_clip(
        self,
        icon_name: str,
        duration: float,
        size: int = 120
    ) -> VideoClip:
        """
        Create a video clip with an icon in a circular container.
        
        Args:
            icon_name: Name of the icon (Feather icon name)
            duration: Duration of the clip
            size: Size of the icon container
        """
        # Map icon names
        icon_map = {
            'warning-skull-icon': 'alert-triangle',
            'happy-face-icon': 'smile',
            'sad-face-icon': 'frown',
            'heart-icon': 'heart',
            'star-icon': 'star',
        }
        
        mapped_icon = icon_map.get(icon_name, icon_name)
        
        # Try to load icon from feather icons or create placeholder
        try:
            # You would need to have Feather icons as SVG/PNG files
            # For this example, we create a placeholder with text
            icon_img = Image.new('RGBA', (size, size), self.white)
            draw = ImageDraw.Draw(icon_img)
            
            # Draw icon placeholder (you can replace with actual icon loading)
            draw.ellipse([10, 10, size-10, size-10], outline=(0, 0, 0, 255), width=3)
            
            # Add icon text
            try:
                icon_font = ImageFont.truetype(self.font.path, 40)
            except:
                icon_font = self.font
            
            # Simple icon representations
            icon_chars = {
                'alert-triangle': '⚠',
                'smile': '😊',
                'frown': '☹',
                'heart': '♥',
                'star': '★',
            }
            
            char = icon_chars.get(mapped_icon, '?')
            bbox = draw.textbbox((0, 0), char, font=icon_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            draw.text((x, y), char, font=icon_font, fill=(0, 0, 0, 255))
            
        except Exception as e:
            print(f"Error creating icon: {e}")
            icon_img = Image.new('RGBA', (size, size), (200, 200, 200, 255))
        
        # Apply circular container with shadow
        icon_img = self.create_circular_container(icon_img, size)
        
        # Create frame function with animation
        def make_frame(t):
            return np.array(icon_img)
        
        clip = VideoClip(make_frame, duration=duration)
        
        # Apply elastic scale-in animation
        def resize_func(t):
            if t >= self.element_scale_duration:
                return 1.0
            progress = t / self.element_scale_duration
            eased = self._ease_out_elastic(progress)
            return 0.8 + 0.2 * eased
        
        clip = clip.resize(resize_func)
        
        # Apply fade-in
        def opacity_func(t):
            if t >= self.element_scale_duration:
                return 1.0
            progress = t / self.element_scale_duration
            return self._ease_out_elastic(progress)
        
        clip = clip.set_opacity(opacity_func)
        
        return clip
    
    def create_sequence_clip(self, item: Dict, index: int = 0) -> CompositeVideoClip:
        """
        Create a complete clip for a single sequence item.
        
        Args:
            item: Sequence item dictionary with duration, type, content, words
            index: Index of the item (for debugging)
        """
        duration = item['duration']
        words = item.get('words', [])
        item_type = item.get('type', 'text')
        content = item.get('content', '')
        
        clips = []
        
        # Create background
        bg = ColorClip(
            size=(self.screen_width, self.screen_height),
            color=self.screen_bg_color
        ).set_duration(duration)
        clips.append(bg)
        
        # Calculate positions
        center_y = self.screen_height // 2
        gif_y = center_y - 20  # Slightly above center
        text_y = 50  # Near top
        
        # Add GIF or icon
        if item_type == 'gif':
            if os.path.exists(content):
                gif_clip = self.create_gif_clip(content, duration)
                if gif_clip:
                    # Center the GIF
                    gif_clip = gif_clip.set_position(('center', gif_y - self.gif_container_size // 2))
                    clips.append(gif_clip)
            else:
                print(f"Warning: GIF not found: {content}")
        
        elif item_type == 'icon':
            icon_clip = self.create_icon_clip(content, duration)
            if icon_clip:
                icon_clip = icon_clip.set_position(('center', gif_y - 60))
                clips.append(icon_clip)
        
        # Add text animation
        if words:
            text_width = int(self.screen_width * 0.9)
            
            def make_text_frame(t):
                text_img = self.create_text_frame(words, t, text_width)
                return np.array(text_img)
            
            text_clip = VideoClip(make_text_frame, duration=duration)
            text_clip = text_clip.set_position(
                ((self.screen_width - text_width) // 2, text_y)
            )
            clips.append(text_clip)
        
        # Composite all clips
        composite = CompositeVideoClip(clips, size=(self.screen_width, self.screen_height))
        return composite.set_duration(duration)
    
    def create_video(
        self,
        sequence: List[Dict],
        output_path: str = 'output.mp4',
        audio_path: Optional[str] = None,
        codec: str = 'libx264',
        audio_codec: str = 'aac',
        bitrate: str = '5000k'
    ) -> str:
        """
        Create the complete video from a sequence.
        
        Args:
            sequence: List of sequence items
            output_path: Path for the output video file
            audio_path: Path to audio file (optional)
            codec: Video codec to use
            audio_codec: Audio codec to use
            bitrate: Video bitrate
            
        Returns:
            Path to the created video file
        """
        print(f"Creating video with {len(sequence)} sequences...")
        
        # Create clips for each sequence item
        sequence_clips = []
        total_duration = 0
        
        for i, item in enumerate(sequence):
            print(f"Processing sequence {i + 1}/{len(sequence)}: {item.get('type', 'unknown')}")
            clip = self.create_sequence_clip(item, i)
            sequence_clips.append(clip)
            total_duration += item['duration']
        
        # Concatenate all sequence clips
        screen_content = concatenate_videoclips(sequence_clips, method='compose')
        
        # Create device frame
        device_frame_img = self.create_device_frame()
        device_frame_clip = ImageClip(np.array(device_frame_img)).set_duration(total_duration)
        
        # Position screen content within device frame
        screen_content = screen_content.set_position((self.border_size, self.border_size))
        
        # Combine device frame and screen content
        final_video = CompositeVideoClip(
            [device_frame_clip, screen_content],
            size=(self.device_width, self.device_height)
        )
        
        # Add audio if provided
        if audio_path and os.path.exists(audio_path):
            print(f"Adding audio from: {audio_path}")
            audio = AudioFileClip(audio_path)
            
            # Trim or loop audio to match video duration
            if audio.duration > total_duration:
                audio = audio.subclip(0, total_duration)
            elif audio.duration < total_duration:
                # Loop audio if needed
                loops_needed = int(total_duration / audio.duration) + 1
                audio = concatenate_audioclips([audio] * loops_needed).subclip(0, total_duration)
            
            final_video = final_video.set_audio(audio)
        
        # Write the video
        print(f"Writing video to: {output_path}")
        final_video.write_videofile(
            output_path,
            fps=self.fps,
            codec=codec,
            audio_codec=audio_codec,
            bitrate=bitrate,
            preset='medium',
            threads=4
        )
        
        # Clean up
        final_video.close()
        for clip in sequence_clips:
            clip.close()
        
        print(f"Video created successfully: {output_path}")
        return output_path
    
    @staticmethod
    def load_sequence_from_json(json_path: str) -> List[Dict]:
        """Load sequence from a JSON file."""
        with open(json_path, 'r') as f:
            return json.load(f)


def main():
    """Example usage of the DeviceMockupVideoCreator."""
    
    # Example sequence (matching your HTML JSON)
    sequence = [
        {
            "duration": 2.401,
            "type": "gif",
            "content": "assets/gifs/teacher/math-cat-teacher-professor-wtnfBGSHG9YpXDWCvR.gif",
            "words": ["Finding", "exact", "location", "is", "easy"]
        },
        {
            "duration": 1.704,
            "type": "gif",
            "content": "assets/gifs/cool/cat-cool-5gXYzsVBmjIsw.gif",
            "words": ["No", "need", "for", "phone", "access"]
        },
        {
            "duration": 1.798,
            "type": "gif",
            "content": "assets/gifs/hacker/fun-meme-hacker-B4dt6rXq6nABilHTYM.gif",
            "words": ["Just", "use", "one", "special", "link"]
        },
        {
            "duration": 2.3,
            "type": "gif",
            "content": "assets/gifs/suspicious/sus-suspicious-meme-ewq2ZiQMWvGffIMRTz.gif",
            "words": ["Link", "steals", "GPS", "and", "info"]
        },
        {
            "duration": 2.3,
            "type": "gif",
            "content": "assets/gifs/hacker/laithalawdat-white-hacker-memes-v1dTK1LUckMv4krjFG.gif",
            "words": ["Use", "IP", "logger", "site", "now"]
        },
        {
            "duration": 2.123,
            "type": "gif",
            "content": "assets/gifs/happy/cat-sigma-jawline-15UbO1LY4O2Fxw8gnI.gif",
            "words": ["Turn", "on", "smart", "GPS", "data"]
        },
        {
            "duration": 2.146,
            "type": "gif",
            "content": "assets/gifs/suspicious/dexter-meme-show-suspicious-TR996IaHtmDi1x98zW.gif",
            "words": ["Make", "link", "look", "less", "suspicious"]
        },
        {
            "duration": 1.891,
            "type": "gif",
            "content": "assets/gifs/happy/cat-meme-wilfrosty-mr-fresh-wr7oA0rSjnWuiLJOY5.gif",
            "words": ["Add", "context", "for", "the", "bait"]
        },
        {
            "duration": 2.088,
            "type": "gif",
            "content": "assets/gifs/happy/cat-reaction-what-abdullahmk47-deSHAgmKsZXPpTUi0N.gif",
            "words": ["Refresh", "page", "for", "more", "info"]
        },
        {
            "duration": 2.8,
            "type": "gif",
            "content": "assets/gifs/cool/vankedisicoin-cat-meme-cartoon-RRN2h25MtWnaa6b55U.gif",
            "words": ["Bella", "knows", "all", "tech", "secrets"]
        }
    ]
    
    # Create the video creator
    creator = DeviceMockupVideoCreator(
        device_width=300,
        fps=30
    )
    
    # Create the video
    output_path = creator.create_video(
        sequence=sequence,
        output_path='device_mockup_video.mp4',
        audio_path='audio.mp3'  # Optional: path to your audio file
    )
    
    print(f"Video saved to: {output_path}")


if __name__ == "__main__":
    main()