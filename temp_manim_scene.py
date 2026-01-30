from manim import *

class PythonFunctionExplained(Scene):
    def construct(self):
        # ============== INTRO ==============
        title = Text("🐍 Python Function Explained", font_size=44)
        title.set_color_by_gradient(BLUE, GREEN)
        subtitle = Text("Step by Step Animation", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # ============== STEP 1: DEF KEYWORD ==============
        step1 = Text("Step 1: The 'def' Keyword", font_size=32, color=YELLOW)
        step1.to_edge(UP)
        self.play(Write(step1))
        
        def_keyword = Text("def", font_size=48, color=BLUE)
        def_box = SurroundingRectangle(def_keyword, color=BLUE, buff=0.2)
        
        explanation1 = Text(
            "'def' tells Python we're creating a function",
            font_size=24,
            color=WHITE
        ).next_to(def_keyword, DOWN, buff=1)
        
        self.play(Write(def_keyword))
        self.play(Create(def_box))
        self.play(FadeIn(explanation1, shift=UP))
        self.wait(2)
        
        # Move def to the left
        self.play(
            FadeOut(def_box),
            FadeOut(explanation1),
            FadeOut(step1),
            def_keyword.animate.scale(0.7).to_edge(LEFT).shift(UP * 2 + RIGHT)
        )
        
        # ============== STEP 2: FUNCTION NAME ==============
        step2 = Text("Step 2: Function Name", font_size=32, color=YELLOW)
        step2.to_edge(UP)
        self.play(Write(step2))
        
        func_name = Text("calculate_sum", font_size=34, color=GREEN)
        func_name.next_to(def_keyword, RIGHT, buff=0.3)
        
        explanation2 = Text(
            "Give your function a descriptive name!",
            font_size=24,
            color=WHITE
        ).shift(DOWN * 1.5)
        
        name_box = SurroundingRectangle(func_name, color=GREEN, buff=0.15)
        
        self.play(Write(func_name))
        self.play(Create(name_box))
        self.play(FadeIn(explanation2))
        self.wait(2)
        self.play(FadeOut(name_box), FadeOut(explanation2), FadeOut(step2))
        
        # ============== STEP 3: PARAMETERS ==============
        step3 = Text("Step 3: Parameters (Inputs)", font_size=32, color=YELLOW)
        step3.to_edge(UP)
        self.play(Write(step3))
        
        params = Text("(a, b)", font_size=34, color=ORANGE)
        params.next_to(func_name, RIGHT, buff=0.1)
        
        # Highlight each parameter
        param_a = Text("a", font_size=34, color=RED)
        param_b = Text("b", font_size=34, color=PURPLE)
        
        explanation3 = VGroup(
            Text("Parameters are inputs to your function", font_size=22),
            Text("• 'a' → First number", font_size=20, color=RED),
            Text("• 'b' → Second number", font_size=20, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT).shift(DOWN * 1.5)
        
        self.play(Write(params))
        self.play(FadeIn(explanation3, shift=UP))
        
        # Animate arrows pointing to parameters
        arrow_a = Arrow(start=DOWN, end=UP, color=RED).scale(0.5)
        arrow_b = Arrow(start=DOWN, end=UP, color=PURPLE).scale(0.5)
        
        self.wait(2)
        self.play(FadeOut(explanation3), FadeOut(step3))
        
        # ============== STEP 4: COLON ==============
        step4 = Text("Step 4: The Colon ':'", font_size=32, color=YELLOW)
        step4.to_edge(UP)
        self.play(Write(step4))
        
        colon = Text(":", font_size=34, color=WHITE)
        colon.next_to(params, RIGHT, buff=0.05)
        
        explanation4 = Text(
            "Colon indicates the start of function body",
            font_size=24
        ).shift(DOWN * 1.5)
        
        self.play(Write(colon), Flash(colon, color=YELLOW, flash_radius=0.5))
        self.play(FadeIn(explanation4))
        self.wait(1.5)
        self.play(FadeOut(explanation4), FadeOut(step4))
        
        # ============== STEP 5: DOCSTRING ==============
        step5 = Text("Step 5: Docstring (Documentation)", font_size=32, color=YELLOW)
        step5.to_edge(UP)
        self.play(Write(step5))
        
        # Function line so far
        line1 = VGroup(def_keyword, func_name, params, colon)
        
        docstring = Text('    """Adds two numbers together"""', font_size=26, color=GRAY)
        docstring.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.3)
        
        doc_box = SurroundingRectangle(docstring, color=GRAY, buff=0.1)
        
        explanation5 = Text(
            "Docstrings explain what your function does!",
            font_size=24,
            color=GRAY_A
        ).shift(DOWN * 2)
        
        self.play(Write(docstring))
        self.play(Create(doc_box))
        self.play(FadeIn(explanation5))
        self.wait(2)
        self.play(FadeOut(doc_box), FadeOut(explanation5), FadeOut(step5))
        
        # ============== STEP 6: FUNCTION BODY ==============
        step6 = Text("Step 6: Function Body (The Logic)", font_size=32, color=YELLOW)
        step6.to_edge(UP)
        self.play(Write(step6))
        
        body_line = Text("    result = a + b", font_size=30, color=TEAL)
        body_line.next_to(docstring, DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Animate the logic
        explanation6 = VGroup(
            Text("The indented code is the function body", font_size=22),
            Text("Here we add 'a' and 'b' together", font_size=22),
            Text("and store it in 'result'", font_size=22)
        ).arrange(DOWN).shift(DOWN * 2.5)
        
        self.play(Write(body_line))
        
        # Highlight the operation
        plus_sign = Text("+", font_size=40, color=YELLOW).move_to(body_line)
        self.play(FadeIn(explanation6))
        self.wait(2)
        self.play(FadeOut(explanation6), FadeOut(step6))
        
        # ============== STEP 7: RETURN STATEMENT ==============
        step7 = Text("Step 7: Return Statement", font_size=32, color=YELLOW)
        step7.to_edge(UP)
        self.play(Write(step7))
        
        return_line = Text("    return result", font_size=30, color=PINK)
        return_line.next_to(body_line, DOWN, aligned_edge=LEFT, buff=0.2)
        
        explanation7 = VGroup(
            Text("'return' sends back the output", font_size=24),
            Text("This is what the function gives back!", font_size=22, color=PINK)
        ).arrange(DOWN).shift(DOWN * 2.5)
        
        self.play(Write(return_line))
        self.play(FadeIn(explanation7))
        
        # Arrow showing return
        return_arrow = Arrow(
            return_line.get_right() + RIGHT * 0.5,
            return_line.get_right() + RIGHT * 2,
            color=PINK
        )
        return_text = Text("Output!", font_size=20, color=PINK)
        return_text.next_to(return_arrow, RIGHT)
        
        self.play(Create(return_arrow), Write(return_text))
        self.wait(2)
        self.play(
            FadeOut(return_arrow), 
            FadeOut(return_text), 
            FadeOut(explanation7), 
            FadeOut(step7)
        )
        
        # ============== SHOW COMPLETE FUNCTION ==============
        complete_title = Text("✨ Complete Function ✨", font_size=32, color=GOLD)
        complete_title.to_edge(UP)
        self.play(Write(complete_title))
        
        # Group all function parts
        complete_function = VGroup(line1, docstring, body_line, return_line)
        
        # Create a code box
        code_box = SurroundingRectangle(
            complete_function, 
            color=WHITE, 
            buff=0.3,
            corner_radius=0.1
        )
        
        self.play(Create(code_box))
        self.play(complete_function.animate.set_color(WHITE))
        self.wait(1)
        
        # Color each part again
        self.play(
            def_keyword.animate.set_color(BLUE),
            func_name.animate.set_color(GREEN),
            params.animate.set_color(ORANGE),
            docstring.animate.set_color(GRAY),
            body_line.animate.set_color(TEAL),
            return_line.animate.set_color(PINK)
        )
        self.wait(2)
        
        # ============== STEP 8: CALLING THE FUNCTION ==============
        self.play(
            FadeOut(complete_title),
            VGroup(complete_function, code_box).animate.scale(0.7).to_edge(UP).shift(DOWN * 0.5)
        )
        
        step8 = Text("Step 8: Calling the Function", font_size=32, color=YELLOW)
        step8.to_edge(DOWN).shift(UP * 3)
        self.play(Write(step8))
        
        # Show function call
        call_line = Text("answer = calculate_sum(5, 3)", font_size=32)
        call_line.next_to(step8, DOWN, buff=0.5)
        
        self.play(Write(call_line))
        self.wait(1)
        
        # ============== STEP 9: EXECUTION VISUALIZATION ==============
        self.play(FadeOut(step8))
        
        exec_title = Text("🚀 Execution Flow", font_size=28, color=YELLOW)
        exec_title.next_to(call_line, DOWN, buff=0.3)
        self.play(Write(exec_title))
        
        # Show values flowing in
        flow_box = VGroup(
            Text("a = 5", font_size=28, color=RED),
            Text("b = 3", font_size=28, color=PURPLE)
        ).arrange(RIGHT, buff=1).next_to(exec_title, DOWN, buff=0.3)
        
        self.play(FadeIn(flow_box, shift=UP))
        
        # Show calculation
        calc = Text("result = 5 + 3 = 8", font_size=28, color=TEAL)
        calc.next_to(flow_box, DOWN, buff=0.3)
        self.play(Write(calc))
        
        # Show return
        result_text = Text("Returns: 8", font_size=32, color=GOLD)
        result_text.next_to(calc, DOWN, buff=0.3)
        result_box = SurroundingRectangle(result_text, color=GOLD, buff=0.15)
        
        self.play(Write(result_text), Create(result_box))
        
        # Final answer
        final = Text("answer = 8 ✓", font_size=36, color=GREEN)
        final.next_to(result_box, DOWN, buff=0.4)
        
        self.play(
            FadeIn(final, scale=1.5),
            Flash(final, color=GREEN, flash_radius=0.8)
        )
        self.wait(2)
        
        # ============== OUTRO ==============
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Summary
        summary_title = Text("📝 Summary", font_size=40, color=YELLOW)
        summary_title.to_edge(UP)
        
        summary = VGroup(
            Text("1. def      → Defines a function", font_size=24, color=BLUE),
            Text("2. name     → Identifies the function", font_size=24, color=GREEN),
            Text("3. (params) → Accepts inputs", font_size=24, color=ORANGE),
            Text("4. :        → Starts the body", font_size=24, color=WHITE),
            Text("5. \"\"\"doc\"\"\"  → Documents the function", font_size=24, color=GRAY),
            Text("6. body     → Contains the logic", font_size=24, color=TEAL),
            Text("7. return   → Outputs the result", font_size=24, color=PINK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        
        self.play(Write(summary_title))
        
        for item in summary:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.5)
        
        self.wait(2)
        
        # Final message
        thanks = Text("Happy Coding! 🎉", font_size=48)
        thanks.set_color_by_gradient(RED, YELLOW, GREEN, BLUE, PURPLE)
        
        self.play(FadeOut(summary), FadeOut(summary_title))
        self.play(Write(thanks))
        self.play(thanks.animate.scale(1.2))
        self.wait(2)


# ============== BONUS: Code Block Style ==============
class PythonCodeBlock(Scene):
    """Alternative version with code block styling"""
    def construct(self):
        # Create a code-editor style background
        code_bg = RoundedRectangle(
            width=12, height=7,
            corner_radius=0.2,
            fill_color="#1e1e1e",
            fill_opacity=1,
            stroke_color="#333333"
        )
        
        # Window buttons
        buttons = VGroup(
            Circle(radius=0.1, fill_color=RED, fill_opacity=1, stroke_width=0),
            Circle(radius=0.1, fill_color=YELLOW, fill_opacity=1, stroke_width=0),
            Circle(radius=0.1, fill_color=GREEN, fill_opacity=1, stroke_width=0)
        ).arrange(RIGHT, buff=0.15)
        buttons.move_to(code_bg.get_top() + DOWN * 0.3 + LEFT * 4.5)
        
        title_bar = Text("function_example.py", font_size=20, color=GRAY)
        title_bar.move_to(code_bg.get_top() + DOWN * 0.3)
        
        self.play(FadeIn(code_bg), FadeIn(buttons), Write(title_bar))
        
        # Line numbers
        line_nums = VGroup(*[
            Text(str(i), font_size=20, color=GRAY_C) 
            for i in range(1, 8)
        ]).arrange(DOWN, buff=0.35, aligned_edge=RIGHT)
        line_nums.move_to(code_bg.get_left() + RIGHT * 0.8 + UP * 0.5)
        
        self.play(FadeIn(line_nums))
        
        # Code lines with syntax highlighting
        code_lines = [
            ("def ", BLUE, "calculate_sum", GREEN, "(", WHITE, "a", ORANGE, ", ", WHITE, "b", ORANGE, ")", WHITE, ":", WHITE),
        ]
        
        # Simplified version - just show the complete code
        code_text = '''def calculate_sum(a, b):
    """Add two numbers"""
    result = a + b
    return result

# Call the function
answer = calculate_sum(5, 3)'''
        
        code = Code(
            code=code_text,
            language="python",
            font_size=24,
            background="rectangle",
            background_stroke_color=WHITE,
            insert_line_no=False,
        )
        code.move_to(ORIGIN)
        
        self.play(FadeIn(code))
        self.wait(3)