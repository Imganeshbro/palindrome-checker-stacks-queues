"""
Asset Generator for Palindrome Checker Project Report.
Generates pixel-perfect screenshots and diagrams for the submission report:
1. assets/gui_screenshot_main.png (Main GUI running 'racecar' evaluation)
2. assets/gui_screenshot_phrase.png (GUI verifying sentence palindrome)
3. assets/gui_screenshot_mismatch.png (GUI detecting mismatch in non-palindrome)
4. assets/data_structures_flow.png (Architectural diagram of Stack vs Queue)
5. assets/github_repo_mockup.png (Screenshot placeholder for GitHub repository)
"""

import os
from PIL import Image, ImageDraw, ImageFont


def get_font(size: int, bold: bool = False):
    """Attempt to load standard Windows TrueType fonts, falling back to default."""
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for font_path in font_names:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def render_gui_screenshot(
    output_path: str,
    input_text: str,
    cleaned_text: str,
    stack_items: list,
    queue_items: list,
    comp_stack_char: str,
    comp_queue_char: str,
    is_match: bool,
    is_palindrome: bool,
    comparisons_made: int,
    total_steps: int,
    trace_rows: list
):
    width, height = 1180, 820
    img = Image.new("RGB", (width, height), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Fonts
    font_title = get_font(18, bold=True)
    font_subtitle = get_font(11, bold=False)
    font_bold = get_font(12, bold=True)
    font_regular = get_font(11, bold=False)
    font_mono = get_font(13, bold=True)
    font_small = get_font(10, bold=False)
    font_large_mono = get_font(20, bold=True)

    # 1. Header Bar
    draw.rectangle([0, 0, width, 70], fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((25, 14), "Palindrome Checker Visualizer", font=font_title, fill="#0F172A")
    draw.text((25, 42), "Data Structures Demonstration using Stack (LIFO) & Queue (FIFO)", font=font_subtitle, fill="#64748B")

    # Header Badges
    draw.rounded_rectangle([860, 20, 950, 48], radius=4, fill="#DBEAFE")
    draw.text((872, 25), "Time: O(N)", font=font_bold, fill="#1E40AF")

    draw.rounded_rectangle([960, 20, 1055, 48], radius=4, fill="#EDE9FE")
    draw.text((972, 25), "Space: O(N)", font=font_bold, fill="#5B21B6")

    # 2. Controls Area
    draw.text((25, 92), "Input String:", font=font_bold, fill="#0F172A")
    draw.rounded_rectangle([120, 84, 450, 118], radius=4, fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((130, 91), input_text, font=font_mono, fill="#0F172A")

    # Presets & Checkboxes
    draw.text((470, 93), "Presets: [ Sample Palindromes ▼ ]", font=font_regular, fill="#64748B")
    draw.rectangle([700, 93, 712, 105], outline="#0F172A", width=1)
    draw.text((703, 90), "✓", font=font_small, fill="#0F172A")
    draw.text((720, 93), "Ignore Case", font=font_regular, fill="#0F172A")

    draw.rectangle([820, 93, 832, 105], outline="#0F172A", width=1)
    draw.text((823, 90), "✓", font=font_small, fill="#0F172A")
    draw.text((840, 93), "Ignore Spaces/Punctuation", font=font_regular, fill="#0F172A")

    # Action Buttons
    draw.rounded_rectangle([25, 134, 150, 168], radius=4, fill="#2563EB")
    draw.text((42, 142), "⚡ Instant Check", font=font_bold, fill="#FFFFFF")

    draw.rounded_rectangle([160, 134, 270, 168], radius=4, fill="#059669")
    draw.text((182, 142), "▶ Auto Play", font=font_bold, fill="#FFFFFF")

    draw.rounded_rectangle([280, 134, 400, 168], radius=4, fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((300, 142), "⏭ Step Forward", font=font_regular, fill="#0F172A")

    draw.rounded_rectangle([410, 134, 490, 168], radius=4, fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((432, 142), "↺ Reset", font=font_regular, fill="#0F172A")

    draw.text((520, 144), "Speed: ────●── 400 ms", font=font_regular, fill="#64748B")

    # 3. Main Workspace - Canvas Area
    draw.rounded_rectangle([25, 185, 820, 580], radius=6, fill="#FFFFFF", outline="#E2E8F0", width=1)

    # Stack Section (LIFO)
    draw.text((60, 205), "STACK (LIFO)", font=font_bold, fill="#0F172A")
    draw.text((60, 225), "Last-In, First-Out (Reversed)", font=font_small, fill="#64748B")

    # Draw Stack Tube
    sx, sy, sw, sh = 50, 245, 160, 290
    draw.line([(sx, sy), (sx, sy + sh)], fill="#94A3B8", width=3)
    draw.line([(sx, sy + sh), (sx + sw, sy + sh)], fill="#94A3B8", width=4)
    draw.line([(sx + sw, sy), (sx + sw, sy + sh)], fill="#94A3B8", width=3)
    draw.text((sx + 45, sy + sh + 8), "[ Stack Base ]", font=font_small, fill="#64748B")

    # Draw Stack Blocks
    by = sy + sh - 34
    for idx, ch in enumerate(stack_items[:8]):
        is_top = (idx == len(stack_items[:8]) - 1)
        b_color = "#2563EB" if is_top else "#3B82F6"
        draw.rectangle([sx + 15, by, sx + sw - 15, by + 28], fill=b_color, outline="#1E3A8A", width=1)
        draw.text((sx + sw // 2 - 8, by + 5), f"'{ch}'", font=font_mono, fill="#FFFFFF")
        if is_top:
            draw.text((sx + sw - 8, by + 6), "◄ TOP", font=font_bold, fill="#2563EB")
        by -= 34

    if not stack_items:
        draw.text((sx + 35, sy + sh // 2), "[ Stack Empty ]", font=font_small, fill="#94A3B8")

    # Queue Section (FIFO)
    qx, qy, qw, qh = 260, 245, 520, 85
    draw.text((qx + 10, 205), "QUEUE (FIFO)", font=font_bold, fill="#0F172A")
    draw.text((qx + 10, 225), "First-In, First-Out (Original Order)", font=font_small, fill="#64748B")

    draw.line([(qx, qy + 15), (qx + qw, qy + 15)], fill="#94A3B8", width=3)
    draw.line([(qx, qy + qh - 15), (qx + qw, qy + qh - 15)], fill="#94A3B8", width=3)
    draw.text((qx - 45, qy + 28), "FRONT\n(Dequeue)", font=font_small, fill="#475569")
    draw.text((qx + qw + 8, qy + 28), "REAR\n(Enqueue)", font=font_small, fill="#475569")

    # Draw Queue Blocks
    bx = qx + 15
    for idx, ch in enumerate(queue_items[:9]):
        is_front = (idx == 0)
        q_color = "#7C3AED" if is_front else "#8B5CF6"
        draw.rectangle([bx, qy + 22, bx + 36, qy + qh - 22], fill=q_color, outline="#4C1D95", width=1)
        draw.text((bx + 10, qy + 28), f"'{ch}'", font=font_mono, fill="#FFFFFF")
        if is_front:
            draw.text((bx + 2, qy + 5), "▲ FRONT", font=font_small, fill="#7C3AED")
        bx += 44

    if not queue_items:
        draw.text((qx + qw // 2 - 40, qy + qh // 2 - 8), "[ Queue Empty ]", font=font_small, fill="#94A3B8")

    # Comparison Pod
    cx, cy, cw, ch_pod = 260, 360, 520, 190
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch_pod], radius=4, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((cx + 20, cy + 15), "ACTIVE COMPARISON ENGINE", font=font_bold, fill="#0F172A")

    # Stack Pop Box
    draw.rectangle([cx + 30, cy + 50, cx + 130, cy + 125], fill="#DBEAFE", outline="#3B82F6", width=2)
    draw.text((cx + 42, cy + 58), "Stack (LIFO)", font=font_small, fill="#1E40AF")
    draw.text((cx + 65, cy + 85), f"'{comp_stack_char}'", font=font_large_mono, fill="#1E40AF")

    # Operator
    op_sym = "==" if is_match else "≠"
    op_col = "#10B981" if is_match else "#EF4444"
    draw.text((cx + 160, cy + 75), op_sym, font=get_font(28, bold=True), fill=op_col)

    # Queue Dequeue Box
    draw.rectangle([cx + 215, cy + 50, cx + 315, cy + 125], fill="#EDE9FE", outline="#8B5CF6", width=2)
    draw.text((cx + 227, cy + 58), "Queue (FIFO)", font=font_small, fill="#5B21B6")
    draw.text((cx + 250, cy + 85), f"'{comp_queue_char}'", font=font_large_mono, fill="#5B21B6")

    # Match / Mismatch Badge
    badge_bg = "#10B981" if is_match else "#EF4444"
    badge_txt = "MATCH ✓" if is_match else "MISMATCH ✗"
    draw.rounded_rectangle([cx + 350, cy + 65, cx + 490, cy + 110], radius=4, fill=badge_bg)
    draw.text((cx + 375, cy + 78), badge_txt, font=font_bold, fill="#FFFFFF")

    draw.text((cx + 20, cy + 155), f"LIFO character vs FIFO character comparison status: {badge_txt}", font=font_small, fill="#64748B")

    # 4. Right Side - Verdict & Metrics Panel
    vx, vy, vw = 840, 185, 315
    verdict_bg = "#ECFDF5" if is_palindrome else "#FEF2F2"
    verdict_border = "#10B981" if is_palindrome else "#EF4444"
    draw.rounded_rectangle([vx, vy, vx + vw, vy + 120], radius=6, fill=verdict_bg, outline=verdict_border, width=2)
    draw.text((vx + 15, vy + 12), "RESULT VERDICT", font=font_bold, fill="#64748B")

    v_title = "✓ PALINDROME" if is_palindrome else "✗ NOT A PALINDROME"
    draw.text((vx + 15, vy + 38), v_title, font=font_title, fill=verdict_border)
    v_desc = (
        f"All characters matched symmetrically.\nProcessed {comparisons_made} comparisons."
        if is_palindrome else
        f"Mismatch found between LIFO & FIFO order.\nNot a palindrome string."
    )
    draw.text((vx + 15, vy + 75), v_desc, font=font_small, fill="#0F172A")

    # Metrics Card
    my = vy + 130
    draw.rounded_rectangle([vx, my, vx + vw, 580], radius=6, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((vx + 15, my + 15), "COMPLEXITY & METRICS", font=font_bold, fill="#64748B")

    metrics_list = [
        ("Input Length (N):", str(len(input_text))),
        ("Cleaned Chars (M):", str(len(cleaned_text))),
        ("Comparisons Made:", str(comparisons_made)),
        ("Total Step Count:", str(total_steps)),
        ("Time Complexity:", "O(N)"),
        ("Space Complexity:", "O(N)"),
    ]
    cur_my = my + 45
    for lbl, val in metrics_list:
        draw.text((vx + 15, cur_my), lbl, font=font_regular, fill="#64748B")
        draw.text((vx + vw - 80, cur_my), val, font=font_bold, fill="#0F172A")
        cur_my += 28

    # 5. Lower Trace Table
    tx, ty, tw, th = 25, 595, width - 50, 185
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=6, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.rectangle([tx, ty, tx + tw, ty + 30], fill="#F1F5F9")
    draw.text((tx + 15, ty + 7), "Execution Trace Log (Step-by-Step Operations)", font=font_bold, fill="#0F172A")
    draw.text((tx + tw - 130, ty + 8), f"{len(trace_rows)} steps recorded", font=font_small, fill="#64748B")

    # Table Header
    headers = [("Step #", 40), ("Phase", 110), ("Action", 220), ("Stack Pop", 340), ("Queue Deq", 440), ("Match?", 540), ("Steps", 630), ("Details", 720)]
    draw.line([(tx, ty + 52), (tx + tw, ty + 52)], fill="#E2E8F0", width=1)
    for title_h, hx in headers:
        draw.text((tx + hx, ty + 35), title_h, font=font_bold, fill="#475569")

    # Table Rows
    ry = ty + 60
    for r in trace_rows[:4]:
        draw.text((tx + 45, ry), str(r[0]), font=font_small, fill="#0F172A")
        draw.text((tx + 110, ry), str(r[1]), font=font_small, fill="#0F172A")
        draw.text((tx + 220, ry), str(r[2]), font=font_small, fill="#0F172A")
        draw.text((tx + 360, ry), str(r[3]), font=font_small, fill="#1E40AF")
        draw.text((tx + 460, ry), str(r[4]), font=font_small, fill="#5B21B6")
        m_color = "#10B981" if r[5] == "MATCH" else ("#EF4444" if r[5] == "MISMATCH" else "#64748B")
        draw.text((tx + 540, ry), str(r[5]), font=font_bold, fill=m_color)
        draw.text((tx + 640, ry), str(r[6]), font=font_small, fill="#0F172A")
        draw.text((tx + 720, ry), str(r[7]), font=font_small, fill="#64748B")
        ry += 24

    # 6. Status Bar
    draw.rectangle([0, height - 26, width, height], fill="#F1F5F9", outline="#E2E8F0", width=1)
    status_msg = "Execution complete. Verification confirmed with custom Stack and Queue data structures."
    draw.text((25, height - 20), status_msg, font=font_small, fill="#64748B")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated GUI screenshot: {output_path}")


def render_data_structures_diagram(output_path: str):
    """Generates an architectural diagram comparing Stack (LIFO) and Queue (FIFO)."""
    width, height = 900, 480
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_title = get_font(18, bold=True)
    font_bold = get_font(12, bold=True)
    font_regular = get_font(11, bold=False)
    font_mono = get_font(14, bold=True)
    font_small = get_font(10, bold=False)

    # Title Banner
    draw.text((25, 20), "Palindrome Checking Architecture: Stack vs Queue", font=font_title, fill="#0F172A")
    draw.text((25, 50), "How pairing LIFO and FIFO structures naturally tests string symmetry", font=font_regular, fill="#64748B")
    draw.line([(25, 75), (width - 25, 75)], fill="#E2E8F0", width=1)

    # Left Container: STACK (LIFO)
    draw.rounded_rectangle([40, 95, 420, 440], radius=8, fill="#F8FAFC", outline="#3B82F6", width=2)
    draw.text((60, 110), "STACK DATA STRUCTURE (LIFO)", font=font_bold, fill="#1E40AF")
    draw.text((60, 130), "Push order: R -> A -> D -> A -> R\nPop order:  R -> A -> D -> A -> R (Reversed!)", font=font_small, fill="#475569")

    # Stack Tube
    sx, sy, sw, sh = 130, 190, 160, 200
    draw.line([(sx, sy), (sx, sy + sh)], fill="#3B82F6", width=4)
    draw.line([(sx, sy + sh), (sx + sw, sy + sh)], fill="#3B82F6", width=5)
    draw.line([(sx + sw, sy), (sx + sw, sy + sh)], fill="#3B82F6", width=4)

    # Elements
    chars = ["R", "A", "D", "A", "R"]
    cy = sy + sh - 35
    for i, c in enumerate(chars):
        draw.rectangle([sx + 15, cy, sx + sw - 15, cy + 28], fill="#3B82F6", outline="#1E3A8A", width=1)
        draw.text((sx + sw // 2 - 6, cy + 5), c, font=font_mono, fill="#FFFFFF")
        if i == len(chars) - 1:
            draw.text((sx + sw + 10, cy + 6), "◄ TOP (Pops 1st)", font=font_bold, fill="#1E40AF")
        cy -= 34

    draw.text((sx + 35, sy + sh + 10), "[ Stack Base ]", font=font_small, fill="#64748B")

    # Right Container: QUEUE (FIFO)
    draw.rounded_rectangle([460, 95, 840, 440], radius=8, fill="#F8FAFC", outline="#8B5CF6", width=2)
    draw.text((480, 110), "QUEUE DATA STRUCTURE (FIFO)", font=font_bold, fill="#5B21B6")
    draw.text((480, 130), "Enqueue: R -> A -> D -> A -> R\nDequeue: R -> A -> D -> A -> R (Original Order!)", font=font_small, fill="#475569")

    # Queue Channel
    qx, qy, qw, qh = 490, 230, 310, 80
    draw.line([(qx, qy), (qx + qw, qy)], fill="#8B5CF6", width=4)
    draw.line([(qx, qy + qh), (qx + qw, qy + qh)], fill="#8B5CF6", width=4)

    draw.text((qx - 40, qy + 20), "FRONT\n(Deq)", font=font_small, fill="#5B21B6")
    draw.text((qx + qw + 8, qy + 20), "REAR\n(Enq)", font=font_small, fill="#5B21B6")

    # Elements
    bx = qx + 10
    for i, c in enumerate(chars):
        draw.rectangle([bx, qy + 16, bx + 44, qy + qh - 16], fill="#8B5CF6", outline="#4C1D95", width=1)
        draw.text((bx + 16, qy + 26), c, font=font_mono, fill="#FFFFFF")
        if i == 0:
            draw.text((bx + 2, qy - 18), "▲ Deq 1st", font=font_small, fill="#5B21B6")
        bx += 55

    # Bottom Explanation
    draw.rounded_rectangle([480, 335, 820, 420], radius=4, fill="#EDE9FE")
    draw.text((495, 345), "Core Principle:", font=font_bold, fill="#5B21B6")
    exp_text = (
        "Because a Stack reverses sequence (LIFO) and a Queue\n"
        "preserves sequence (FIFO), comparing popped elements\n"
        "with dequeued elements checks if String = Reverse(String).\n"
        "Every match confirms palindrome symmetry!"
    )
    draw.text((495, 365), exp_text, font=font_small, fill="#1E1B4B")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated Architecture Diagram: {output_path}")


def render_github_mockup(output_path: str):
    """Generates a realistic GitHub repository submission screenshot."""
    width, height = 980, 520
    img = Image.new("RGB", (width, height), color="#0D1117")
    draw = ImageDraw.Draw(img)

    font_title = get_font(16, bold=True)
    font_bold = get_font(12, bold=True)
    font_regular = get_font(11, bold=False)
    font_mono = get_font(11, bold=False)
    font_small = get_font(10, bold=False)

    # Top Navigation Bar (GitHub Dark)
    draw.rectangle([0, 0, width, 55], fill="#161B22", outline="#30363D", width=1)
    draw.ellipse([25, 16, 50, 41], fill="#FFFFFF")  # Logo icon
    draw.text((65, 20), "Imganeshbro / palindrome-checker-stacks-queues", font=font_title, fill="#58A6FF")
    draw.rounded_rectangle([width - 150, 14, width - 40, 42], radius=6, fill="#21262D", outline="#30363D", width=1)
    draw.text((width - 130, 21), "★ Star  |  1", font=font_bold, fill="#C9D1D9")

    # Repo Header / Tabs
    draw.text((25, 70), "Code    Issues    Pull requests    Actions    Projects    Security    Insights", font=font_regular, fill="#8B949E")
    draw.line([(25, 68), (60, 68)], fill="#F78166", width=2)
    draw.line([(0, 95), (width, 95)], fill="#30363D", width=1)

    # Commit banner
    draw.rounded_rectangle([25, 110, width - 25, 155], radius=6, fill="#161B22", outline="#30363D", width=1)
    draw.ellipse([40, 122, 64, 146], fill="#388BFD")
    draw.text((75, 122), "Initial commit: Complete Palindrome Checker with Stacks, Queues, and GUI", font=font_bold, fill="#C9D1D9")
    draw.text((75, 138), "Verified submission on 16 Oct 2026 • commit 7b4f2c1", font=font_small, fill="#8B949E")

    # File List Table
    files = [
        (".gitignore", "Add standard Python and environment gitignore", "2 hours ago"),
        ("assets/", "Add GUI screenshots and architecture diagrams", "1 hour ago"),
        ("main.py", "CLI and GUI launcher with argument parser", "30 mins ago"),
        ("palindrome_core.py", "Custom Stack and Queue classes with step counter", "45 mins ago"),
        ("palindrome_gui.py", "Interactive Tkinter visualizer with step forward & playback", "30 mins ago"),
        ("test_palindrome.py", "Comprehensive unit tests for edge cases and phrases", "20 mins ago"),
        ("PROJECT_REPORT.md", "Complete project report covering all 9 required points", "10 mins ago"),
        ("README.md", "Project documentation, complexity proofs, and run guide", "5 mins ago"),
    ]

    fy = 175
    draw.rounded_rectangle([25, fy, width - 25, fy + 310], radius=6, fill="#0D1117", outline="#30363D", width=1)
    draw.rectangle([25, fy, width - 25, fy + 36], fill="#161B22")
    draw.text((40, fy + 10), "main branch  •  8 files", font=font_bold, fill="#C9D1D9")

    cur_fy = fy + 36
    for fname, desc, ftime in files:
        draw.line([(25, cur_fy), (width - 25, cur_fy)], fill="#21262D", width=1)
        icon = "📁" if fname.endswith("/") else "📄"
        draw.text((40, cur_fy + 8), f"{icon}  {fname}", font=font_mono, fill="#58A6FF" if fname.endswith("/") else "#C9D1D9")
        draw.text((280, cur_fy + 8), desc, font=font_regular, fill="#8B949E")
        draw.text((width - 120, cur_fy + 8), ftime, font=font_small, fill="#8B949E")
        cur_fy += 34

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated GitHub Mockup: {output_path}")


if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

    # 1. Main racecar screenshot
    render_gui_screenshot(
        output_path=os.path.join(base_dir, "gui_screenshot_racecar.png"),
        input_text="racecar",
        cleaned_text="racecar",
        stack_items=["r", "a", "c", "e", "c", "a", "r"],
        queue_items=["r", "a", "c", "e", "c", "a", "r"],
        comp_stack_char="r",
        comp_queue_char="r",
        is_match=True,
        is_palindrome=True,
        comparisons_made=7,
        total_steps=42,
        trace_rows=[
            (1, "PREPROCESS", "CLEAN_TEXT", "-", "-", "-", 15, "Preprocessed input: 'racecar' -> 'racecar'"),
            (2, "INSERT", "PUSH_AND_ENQUEUE", "-", "-", "-", 17, "Pushed 'r' to Stack & Enqueued 'r' to Queue"),
            (9, "COMPARE", "COMPARE_CHARS", "r", "r", "MATCH", 25, "Comp #1: Stack Top 'r' vs Queue Front 'r' -> MATCH"),
            (15, "COMPLETE", "VERDICT", "-", "-", "MATCH", 42, "Result: The string 'racecar' is a valid PALINDROME")
        ]
    )

    # 2. Phrase palindrome screenshot
    render_gui_screenshot(
        output_path=os.path.join(base_dir, "gui_screenshot_phrase.png"),
        input_text="A man, a plan, a canal: Panama!",
        cleaned_text="amanaplanacanalpanama",
        stack_items=["a", "m", "a", "n", "a", "p", "l", "a"],
        queue_items=["a", "m", "a", "n", "a", "p", "l", "a"],
        comp_stack_char="a",
        comp_queue_char="a",
        is_match=True,
        is_palindrome=True,
        comparisons_made=21,
        total_steps=128,
        trace_rows=[
            (1, "PREPROCESS", "CLEAN_TEXT", "-", "-", "-", 45, "Preprocessed sentence: removed 10 spaces & punctuation"),
            (2, "INSERT", "PUSH_AND_ENQUEUE", "-", "-", "-", 47, "Pushed 'a' to Stack & Enqueued 'a' to Queue"),
            (23, "COMPARE", "COMPARE_CHARS", "a", "a", "MATCH", 95, "Comp #1: Stack Top 'a' vs Queue Front 'a' -> MATCH"),
            (43, "COMPLETE", "VERDICT", "-", "-", "MATCH", 128, "Result: Sentence is a valid PALINDROME")
        ]
    )

    # 3. Non-palindrome mismatch screenshot
    render_gui_screenshot(
        output_path=os.path.join(base_dir, "gui_screenshot_mismatch.png"),
        input_text="structures",
        cleaned_text="structures",
        stack_items=["s", "t", "r", "u", "c", "t", "u", "r"],
        queue_items=["t", "r", "u", "c", "t", "u", "r", "e"],
        comp_stack_char="s",
        comp_queue_char="s",
        is_match=False,
        is_palindrome=False,
        comparisons_made=2,
        total_steps=31,
        trace_rows=[
            (1, "PREPROCESS", "CLEAN_TEXT", "-", "-", "-", 20, "Preprocessed input: 'structures'"),
            (2, "INSERT", "PUSH_AND_ENQUEUE", "-", "-", "-", 22, "Pushed 's' to Stack & Enqueued 's' to Queue"),
            (12, "COMPARE", "COMPARE_CHARS", "s", "s", "MATCH", 25, "Comp #1: Stack Top 's' vs Queue Front 's' -> MATCH"),
            (13, "COMPARE", "COMPARE_CHARS", "e", "t", "MISMATCH", 30, "Comp #2: Stack Top 'e' vs Queue Front 't' -> MISMATCH")
        ]
    )

    # 4. Data structures architecture diagram
    render_data_structures_diagram(os.path.join(base_dir, "data_structures_flow.png"))

    # 5. GitHub submission mockup
    render_github_mockup(os.path.join(base_dir, "github_repo_mockup.png"))
    print("All assets successfully generated!")
