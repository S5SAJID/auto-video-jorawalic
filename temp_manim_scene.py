
from manim import *
class DynamicScene(Scene):
    def construct(self):
    
        # Match MoviePy dimensions
        config.pixel_width = 360
        config.pixel_height = 640
        config.frame_height = 8.0  # Internal coordinate height
        config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)

        obj = Tex(y = wx + b).move_to(UP * 2)
        # Prevent Overflow
        max_w = config.frame_width * 0.9
        max_h = config.frame_height * 0.9
        if obj.width > max_w: obj.scale_to_fit_width(max_w)
        if obj.height > max_h: obj.scale_to_fit_height(max_h)
        self.add(obj)

        self.play(Create(obj), run_time=1.997)
        self.wait(0.1)
