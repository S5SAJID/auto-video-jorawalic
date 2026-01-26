import os

VIDEO_SIZE = (int(720/2),int(1280/2))
class ManimPipelineManager:
    def __init__(self):
        # Keeps track of what objects exist and their last properties
        self.state_registry = {}

    def get_render_script(self, segment_id, content, duration):
        # Import VIDEO_SIZE from your main script or pass it in
        
        prev_state = self.state_registry.get(segment_id, None)
        
        # 1. Setup with Frame constraints
        setup_code = f"""
        # Match MoviePy dimensions
        config.pixel_width = {VIDEO_SIZE[0]}
        config.pixel_height = {VIDEO_SIZE[1]}
        config.frame_height = 8.0  # Internal coordinate height
        config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)
"""

        if prev_state:
            setup_code += f"\n        obj = {prev_state['mobject']}({prev_state['args']}).move_to({prev_state['pos']})"
        else:
            setup_code += f"\n        obj = {content['mobject']}({content.get('args', '')}).move_to({content.get('pos', 'ORIGIN')})"

        # 2. Add Anti-Overflow Logic
        # This scales the object down if it exceeds 90% of the frame width/height
        setup_code += """
        # Prevent Overflow
        max_w = config.frame_width * 0.9
        max_h = config.frame_height * 0.9
        if obj.width > max_w: obj.scale_to_fit_width(max_w)
        if obj.height > max_h: obj.scale_to_fit_height(max_h)
        self.add(obj)
"""

        # 3. Prepare Animation
        action = content.get('action', 'Create')
        anim_code = self._build_anim_string(action, content, duration)
        
        
        self._update_registry(segment_id, content)

        return f"""
from manim import *
class DynamicScene(Scene):
    def construct(self):
    {setup_code}
    {anim_code}
        self.wait(0.1)
"""


    def _build_anim_string(self, action, content, duration):
        # Chainable animations using Manim's .animate syntax
        if action == "Create":
            return f"    self.play(Create(obj), run_time={duration})"
        
        elif action == "Transform":
            target = f"{content['target_mobject']}({content.get('target_args', '')})"
            return f"    self.play(Transform(obj, {target}.move_to(obj.get_center())), run_time={duration})"
        
        elif action == "Modify":
            # Powerful: Chain multiple property changes
            # Content example: {"action": "Modify", "move_to": "UP*2", "rotate": "PI/4", "scale": 1.5}
            mods = []
            if "move_to" in content: mods.append(f"move_to({content['move_to']})")
            if "rotate" in content: mods.append(f"rotate({content['rotate']})")
            if "scale" in content: mods.append(f"scale({content['scale']})")
            if "set_color" in content: mods.append(f"set_color({content['set_color']})")
            
            chain = ".".join(mods)
            return f"    self.play(obj.animate.{chain}, run_time={duration})"
        
        return f"    self.wait({duration})"

    def _update_registry(self, segment_id, content):
        # Maintain the object type and position for the next clip
        current = self.state_registry.get(segment_id, {})
        current['mobject'] = content.get('target_mobject', content.get('mobject', current.get('mobject')))
        current['args'] = content.get('target_args', content.get('args', current.get('args', '')))
        current['pos'] = content.get('move_to', content.get('pos', current.get('pos', 'ORIGIN')))
        self.state_registry[segment_id] = current
