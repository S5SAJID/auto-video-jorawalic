
from manim import *
class DynamicScene(Scene):
    def construct(self):
    
        # Match MoviePy dimensions
        config.pixel_width = 360
        config.pixel_height = 640
        config.frame_height = 8.0  # Internal coordinate height
        config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)

        obj = Star(color=GOLD, n=5, fill_opacity=0.9).move_to(ORIGIN)
        # Prevent Overflow
        max_w = config.frame_width * 0.9
        max_h = config.frame_height * 0.9
        if obj.width > max_w: obj.scale_to_fit_width(max_w)
        if obj.height > max_h: obj.scale_to_fit_height(max_h)
        self.add(obj)

        self.play(obj.animate.rotate(TAU).scale(1.5), run_time=1.568)
        self.wait(0.1)
