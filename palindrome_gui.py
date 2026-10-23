"""
Interactive GUI for Palindrome Checker using Stacks and Queues.
Built with Python Tkinter and Canvas.

Features:
- Visual representation of Stack (LIFO) and Queue (FIFO)
- Step-by-step interactive animation with variable playback speed
- Manual step forward and auto-play controls
- Real-time comparison indicator (Stack Pop vs Queue Dequeue)
- Trace log table with step counts and operation details
- Pre-loaded sample strings (Classic, phrases, numbers, non-palindromes)
- Complexity and performance metrics dashboard
- Screenshot export functionality
"""

import sys
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, List

from palindrome_core import PalindromeChecker, PalindromeResult, StepEvent


# UI Color Palette (Modern Slate & Emerald/Crimson Theme)
BG_MAIN = "#F8FAFC"
BG_CARD = "#FFFFFF"
BG_SIDEBAR = "#F1F5F9"
ACCENT_PRIMARY = "#2563EB"     # Royal Blue
ACCENT_SECONDARY = "#4F46E5"   # Indigo
ACCENT_SUCCESS = "#10B981"     # Emerald Green
ACCENT_ERROR = "#EF4444"       # Crimson Red
ACCENT_WARNING = "#F59E0B"     # Amber
TEXT_DARK = "#0F172A"          # Slate 900
TEXT_MUTED = "#64748B"         # Slate 500
BORDER_COLOR = "#E2E8F0"       # Slate 200

STACK_COLOR = "#3B82F6"        # Blue
QUEUE_COLOR = "#8B5CF6"        # Purple
MATCH_COLOR = "#10B981"        # Green
MISMATCH_COLOR = "#EF4444"     # Red
HIGHLIGHT_COLOR = "#FBBF24"    # Yellow/Gold


class PalindromeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Palindrome Checker - Stack (LIFO) & Queue (FIFO) Visualizer")
        self.root.geometry("1180x820")
        self.root.minsize(1000, 720)
        self.root.configure(bg=BG_MAIN)

        # Algorithm Controller
        self.checker = PalindromeChecker()
        self.current_result: Optional[PalindromeResult] = None
        self.current_step_idx: int = -1
        self.is_playing: bool = False
        self.animation_speed_ms: int = 400

        # Build UI
        self._setup_styles()
        self._build_header()
        self._build_controls()
        self._build_main_workspace()
        self._build_status_bar()

        # Load initial example
        self.entry_var.set("racecar")
        self.on_check_instant()

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", background=BG_MAIN)
        style.configure("Card.TFrame", background=BG_CARD, relief="flat")
        style.configure("TLabel", background=BG_MAIN, foreground=TEXT_DARK, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=BG_MAIN, foreground=TEXT_DARK, font=("Segoe UI", 18, "bold"))
        style.configure("SubHeader.TLabel", background=BG_MAIN, foreground=TEXT_MUTED, font=("Segoe UI", 10))
        style.configure("CardHeader.TLabel", background=BG_CARD, foreground=TEXT_DARK, font=("Segoe UI", 11, "bold"))

        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Control.TButton", font=("Segoe UI", 9), padding=4)

        # Treeview styling
        style.configure(
            "Treeview",
            background=BG_CARD,
            foreground=TEXT_DARK,
            rowheight=24,
            fieldbackground=BG_CARD,
            font=("Segoe UI", 9)
        )
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", ACCENT_PRIMARY)], foreground=[("selected", "#FFFFFF")])

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=BG_CARD, height=70, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        inner = tk.Frame(header_frame, bg=BG_CARD)
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Title & Subtitle
        title_box = tk.Frame(inner, bg=BG_CARD)
        title_box.pack(side=tk.LEFT, fill=tk.Y)

        title = tk.Label(title_box, text="Palindrome Checker Visualizer", font=("Segoe UI", 16, "bold"), bg=BG_CARD, fg=TEXT_DARK)
        title.pack(anchor="w")

        subtitle = tk.Label(title_box, text="Data Structures Demonstration using Stack (LIFO) & Queue (FIFO)", font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MUTED)
        subtitle.pack(anchor="w")

        # Badges on Right
        badge_box = tk.Frame(inner, bg=BG_CARD)
        badge_box.pack(side=tk.RIGHT, fill=tk.Y, pady=4)

        b1 = tk.Label(badge_box, text="Time: O(N)", font=("Segoe UI", 9, "bold"), bg="#DBEAFE", fg="#1E40AF", padx=8, pady=3)
        b1.pack(side=tk.LEFT, padx=4)

        b2 = tk.Label(badge_box, text="Space: O(N)", font=("Segoe UI", 9, "bold"), bg="#EDE9FE", fg="#5B21B6", padx=8, pady=3)
        b2.pack(side=tk.LEFT, padx=4)

        btn_screenshot = tk.Button(
            badge_box,
            text="📷 Save Screenshot",
            command=self.save_screenshot,
            font=("Segoe UI", 9, "bold"),
            bg="#0F172A",
            fg="#FFFFFF",
            relief="flat",
            padx=10,
            pady=3,
            cursor="hand2"
        )
        btn_screenshot.pack(side=tk.LEFT, padx=8)

    def _build_controls(self):
        ctrl_frame = tk.Frame(self.root, bg=BG_MAIN, pady=10, padx=20)
        ctrl_frame.pack(fill=tk.X, side=tk.TOP)

        # Row 1: Input string and quick presets
        row1 = tk.Frame(ctrl_frame, bg=BG_MAIN)
        row1.pack(fill=tk.X, pady=2)

        tk.Label(row1, text="Input String:", font=("Segoe UI", 10, "bold"), bg=BG_MAIN, fg=TEXT_DARK).pack(side=tk.LEFT, padx=(0, 8))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            row1,
            textvariable=self.entry_var,
            font=("Consolas", 12),
            bg=BG_CARD,
            fg=TEXT_DARK,
            relief="solid",
            bd=1,
            width=36
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 12), ipady=3)
        self.entry.bind("<Return>", lambda e: self.on_check_instant())

        # Sample Presets Combobox
        tk.Label(row1, text="Presets:", font=("Segoe UI", 9), bg=BG_MAIN, fg=TEXT_MUTED).pack(side=tk.LEFT, padx=(6, 4))
        self.preset_var = tk.StringVar(value="Choose Sample...")
        presets = [
            "racecar",
            "radar",
            "level",
            "noon",
            "12321",
            "A man, a plan, a canal: Panama",
            "Was it a car or a cat I saw?",
            "Step on no pets",
            "hello",
            "structures",
            "algorithm"
        ]
        self.preset_dropdown = ttk.Combobox(row1, textvariable=self.preset_var, values=presets, state="readonly", width=22)
        self.preset_dropdown.pack(side=tk.LEFT, padx=(0, 15))
        self.preset_dropdown.bind("<<ComboboxSelected>>", self.on_preset_selected)

        # Checkbox Options
        self.ignore_case_var = tk.BooleanVar(value=True)
        self.ignore_punct_var = tk.BooleanVar(value=True)

        chk_case = tk.Checkbutton(
            row1,
            text="Ignore Case",
            variable=self.ignore_case_var,
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 9),
            command=self.on_options_changed
        )
        chk_case.pack(side=tk.LEFT, padx=6)

        chk_punct = tk.Checkbutton(
            row1,
            text="Ignore Spaces/Punctuation",
            variable=self.ignore_punct_var,
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 9),
            command=self.on_options_changed
        )
        chk_punct.pack(side=tk.LEFT, padx=6)

        # Row 2: Action Buttons & Animation Controls
        row2 = tk.Frame(ctrl_frame, bg=BG_MAIN)
        row2.pack(fill=tk.X, pady=(8, 0))

        # Main Action Buttons
        btn_check = tk.Button(
            row2,
            text="⚡ Instant Check",
            command=self.on_check_instant,
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_PRIMARY,
            fg="#FFFFFF",
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2"
        )
        btn_check.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_play = tk.Button(
            row2,
            text="▶ Auto Play",
            command=self.toggle_play,
            font=("Segoe UI", 9, "bold"),
            bg="#059669",
            fg="#FFFFFF",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        )
        self.btn_play.pack(side=tk.LEFT, padx=6)

        self.btn_step = tk.Button(
            row2,
            text="⏭ Step Forward",
            command=self.step_forward,
            font=("Segoe UI", 9),
            bg=BG_CARD,
            fg=TEXT_DARK,
            relief="solid",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2"
        )
        self.btn_step.pack(side=tk.LEFT, padx=6)

        btn_reset = tk.Button(
            row2,
            text="↺ Reset",
            command=self.reset_all,
            font=("Segoe UI", 9),
            bg=BG_CARD,
            fg=TEXT_DARK,
            relief="solid",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2"
        )
        btn_reset.pack(side=tk.LEFT, padx=6)

        # Speed Control Slider
        tk.Label(row2, text="Speed:", font=("Segoe UI", 9), bg=BG_MAIN, fg=TEXT_MUTED).pack(side=tk.LEFT, padx=(18, 4))
        self.speed_slider = tk.Scale(
            row2,
            from_=100,
            to=1000,
            orient=tk.HORIZONTAL,
            showvalue=0,
            bg=BG_MAIN,
            highlightthickness=0,
            length=110,
            command=self.on_speed_changed
        )
        self.speed_slider.set(400)
        self.speed_slider.pack(side=tk.LEFT, padx=(0, 6))

        self.speed_label = tk.Label(row2, text="400 ms", font=("Segoe UI", 8), bg=BG_MAIN, fg=TEXT_MUTED)
        self.speed_label.pack(side=tk.LEFT)

    def _build_main_workspace(self):
        workspace = tk.Frame(self.root, bg=BG_MAIN, padx=20, pady=5)
        workspace.pack(fill=tk.BOTH, expand=True)

        # Upper Area: Visualization Canvas & Summary Cards
        upper_frame = tk.Frame(workspace, bg=BG_MAIN)
        upper_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=(0, 10))

        # Canvas for graphical Stack, Queue, and Comparison Pod
        canvas_card = tk.Frame(upper_frame, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR)
        canvas_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.canvas = tk.Canvas(canvas_card, bg=BG_CARD, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.redraw())

        # Right Side: Metric Cards & Verdict Banner
        stats_panel = tk.Frame(upper_frame, bg=BG_MAIN, width=320)
        stats_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        stats_panel.pack_propagate(False)

        # Verdict Card
        self.verdict_card = tk.Frame(stats_panel, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=15, pady=12)
        self.verdict_card.pack(fill=tk.X, pady=(0, 8))

        tk.Label(self.verdict_card, text="RESULT VERDICT", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        self.verdict_text = tk.Label(self.verdict_card, text="READY", font=("Segoe UI", 16, "bold"), bg=BG_CARD, fg=TEXT_MUTED)
        self.verdict_text.pack(anchor="w", pady=(2, 4))
        self.verdict_detail = tk.Label(self.verdict_card, text="Enter a string to test", font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_MUTED, wraplength=280, justify="left")
        self.verdict_detail.pack(anchor="w")

        # Metrics Card
        metrics_card = tk.Frame(stats_panel, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=15, pady=12)
        metrics_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(metrics_card, text="COMPLEXITY & METRICS", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 8))

        self.stat_input_len = self._create_metric_row(metrics_card, "Input Length (N):", "0")
        self.stat_cleaned_len = self._create_metric_row(metrics_card, "Cleaned Chars (M):", "0")
        self.stat_comparisons = self._create_metric_row(metrics_card, "Comparisons Made:", "0")
        self.stat_total_steps = self._create_metric_row(metrics_card, "Total Step Count:", "0")
        self.stat_time_complexity = self._create_metric_row(metrics_card, "Time Complexity:", "O(N)")
        self.stat_space_complexity = self._create_metric_row(metrics_card, "Space Complexity:", "O(N)")

        # Lower Area: Trace Log Table
        lower_frame = tk.Frame(workspace, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR, height=180)
        lower_frame.pack(fill=tk.BOTH, expand=False, side=tk.BOTTOM)
        lower_frame.pack_propagate(False)

        table_header = tk.Frame(lower_frame, bg=BG_SIDEBAR, padx=10, pady=4)
        table_header.pack(fill=tk.X)
        tk.Label(table_header, text="Execution Trace Log (Step-by-Step Operations)", font=("Segoe UI", 9, "bold"), bg=BG_SIDEBAR, fg=TEXT_DARK).pack(side=tk.LEFT)
        self.log_count_label = tk.Label(table_header, text="0 steps recorded", font=("Segoe UI", 8), bg=BG_SIDEBAR, fg=TEXT_MUTED)
        self.log_count_label.pack(side=tk.RIGHT)

        columns = ("step", "phase", "action", "stack_char", "queue_char", "comparison", "running_steps", "details")
        self.tree = ttk.Treeview(lower_frame, columns=columns, show="headings", height=6)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        self.tree.heading("step", text="Step #")
        self.tree.heading("phase", text="Phase")
        self.tree.heading("action", text="Action")
        self.tree.heading("stack_char", text="Stack (Pop)")
        self.tree.heading("queue_char", text="Queue (Deq)")
        self.tree.heading("comparison", text="Match?")
        self.tree.heading("running_steps", text="Cumul. Steps")
        self.tree.heading("details", text="Description")

        self.tree.column("step", width=60, anchor="center")
        self.tree.column("phase", width=95, anchor="center")
        self.tree.column("action", width=120, anchor="center")
        self.tree.column("stack_char", width=80, anchor="center")
        self.tree.column("queue_char", width=80, anchor="center")
        self.tree.column("comparison", width=80, anchor="center")
        self.tree.column("running_steps", width=90, anchor="center")
        self.tree.column("details", width=340, anchor="w")

        scrollbar = ttk.Scrollbar(lower_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def _create_metric_row(self, parent: tk.Widget, label_text: str, default_val: str) -> tk.Label:
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill=tk.X, pady=3)
        tk.Label(row, text=label_text, font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MUTED).pack(side=tk.LEFT)
        val_label = tk.Label(row, text=default_val, font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_DARK)
        val_label.pack(side=tk.RIGHT)
        return val_label

    def _build_status_bar(self):
        status_bar = tk.Frame(self.root, bg=BG_SIDEBAR, height=26, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)

        self.status_label = tk.Label(
            status_bar,
            text="Ready. Use Instant Check or Auto Play to visualize the Palindrome checking process.",
            font=("Segoe UI", 8),
            bg=BG_SIDEBAR,
            fg=TEXT_MUTED
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=3)

    # Event Handlers
    def on_preset_selected(self, event=None):
        preset = self.preset_var.get()
        if preset and preset != "Choose Sample...":
            self.entry_var.set(preset)
            self.on_check_instant()

    def on_options_changed(self):
        self.checker.ignore_case = self.ignore_case_var.get()
        self.checker.ignore_spaces_and_punct = self.ignore_punct_var.get()
        self.on_check_instant()

    def on_speed_changed(self, val):
        self.animation_speed_ms = int(val)
        self.speed_label.config(text=f"{self.animation_speed_ms} ms")

    def reset_all(self):
        self.is_playing = False
        self.btn_play.config(text="▶ Auto Play", bg="#059669")
        self.current_step_idx = -1
        self.current_result = None
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.verdict_text.config(text="RESET", fg=TEXT_MUTED)
        self.verdict_detail.config(text="Workspace cleared. Enter new string.")
        self.stat_input_len.config(text="0")
        self.stat_cleaned_len.config(text="0")
        self.stat_comparisons.config(text="0")
        self.stat_total_steps.config(text="0")
        self.status_label.config(text="Reset complete.")
        self.redraw()

    def on_check_instant(self):
        self.is_playing = False
        self.btn_play.config(text="▶ Auto Play", bg="#059669")
        text = self.entry_var.get()

        self.current_result = self.checker.check(text)
        self._populate_trace_table(self.current_result.steps)
        self._update_metrics(self.current_result)

        # Set step to final completed step
        self.current_step_idx = len(self.current_result.steps) - 1
        self.redraw()
        self.status_label.config(text=f"Instant check completed: {self.current_result.total_step_count} steps evaluated.")

    def toggle_play(self):
        if self.is_playing:
            self.is_playing = False
            self.btn_play.config(text="▶ Auto Play", bg="#059669")
            self.status_label.config(text="Animation paused.")
        else:
            text = self.entry_var.get()
            if not self.current_result or self.current_step_idx >= len(self.current_result.steps) - 1:
                self.current_result = self.checker.check(text)
                self._populate_trace_table(self.current_result.steps)
                self.current_step_idx = -1

            self.is_playing = True
            self.btn_play.config(text="⏸ Pause", bg=ACCENT_WARNING)
            self.status_label.config(text="Auto-playing step-by-step animation...")
            self._run_animation_tick()

    def _run_animation_tick(self):
        if not self.is_playing or not self.current_result:
            return

        if self.current_step_idx < len(self.current_result.steps) - 1:
            self.current_step_idx += 1
            self._select_tree_row(self.current_step_idx)
            self.redraw()
            self.root.after(self.animation_speed_ms, self._run_animation_tick)
        else:
            self.is_playing = False
            self.btn_play.config(text="▶ Auto Play", bg="#059669")
            self._update_metrics(self.current_result)
            self.status_label.config(text="Animation finished. Final verdict reached.")

    def step_forward(self):
        self.is_playing = False
        self.btn_play.config(text="▶ Auto Play", bg="#059669")

        text = self.entry_var.get()
        if not self.current_result:
            self.current_result = self.checker.check(text)
            self._populate_trace_table(self.current_result.steps)
            self.current_step_idx = -1

        if self.current_step_idx < len(self.current_result.steps) - 1:
            self.current_step_idx += 1
            self._select_tree_row(self.current_step_idx)
            self.redraw()
            self.status_label.config(text=f"Stepped to #{self.current_step_idx + 1} of {len(self.current_result.steps)}")
        else:
            self.status_label.config(text="Already at final step.")

    def _select_tree_row(self, idx: int):
        children = self.tree.get_children()
        if 0 <= idx < len(children):
            target_id = children[idx]
            self.tree.selection_set(target_id)
            self.tree.see(target_id)

    def _populate_trace_table(self, steps: List[StepEvent]):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for s in steps:
            comp_str = ""
            if s.is_match is not None and s.phase == "COMPARE":
                comp_str = "MATCH" if s.is_match else "MISMATCH"

            self.tree.insert("", "end", values=(
                s.step_number,
                s.phase,
                s.action,
                s.stack_char or "-",
                s.queue_char or "-",
                comp_str or "-",
                s.total_steps_so_far,
                s.description
            ))

        self.log_count_label.config(text=f"{len(steps)} steps recorded")

    def _update_metrics(self, res: PalindromeResult):
        self.stat_input_len.config(text=str(len(res.original_text)))
        self.stat_cleaned_len.config(text=str(len(res.cleaned_text)))
        self.stat_comparisons.config(text=str(res.comparisons_made))
        self.stat_total_steps.config(text=str(res.total_step_count))
        self.stat_time_complexity.config(text=res.time_complexity)
        self.stat_space_complexity.config(text=res.space_complexity)

        if res.is_palindrome:
            self.verdict_text.config(text="✓ PALINDROME", fg=ACCENT_SUCCESS)
            self.verdict_card.config(highlightbackground=ACCENT_SUCCESS, highlightthickness=2)
            self.verdict_detail.config(
                text=f"All {res.comparisons_made} characters matched between Stack (reverse) and Queue (forward).",
                fg=TEXT_DARK
            )
        else:
            self.verdict_text.config(text="✗ NOT A PALINDROME", fg=ACCENT_ERROR)
            self.verdict_card.config(highlightbackground=ACCENT_ERROR, highlightthickness=2)
            self.verdict_detail.config(
                text=res.mismatch_details or "Characters failed to match during Stack/Queue verification.",
                fg=TEXT_DARK
            )

    # Canvas Drawing Engine
    def redraw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100 or h < 100:
            return

        # Determine current state to render
        stack_items: List[str] = []
        queue_items: List[str] = []
        current_step: Optional[StepEvent] = None
        phase_text = "READY"
        action_text = "Idle"

        if self.current_result and 0 <= self.current_step_idx < len(self.current_result.steps):
            current_step = self.current_result.steps[self.current_step_idx]
            stack_items = current_step.stack_state
            queue_items = current_step.queue_state
            phase_text = current_step.phase
            action_text = current_step.action

        # Background grid or guide
        self.canvas.create_text(
            15, 15,
            anchor="nw",
            text=f"Phase: {phase_text} | Action: {action_text}",
            font=("Segoe UI", 11, "bold"),
            fill=ACCENT_PRIMARY
        )

        # Draw Section 1: STACK (Left Column, Vertical)
        stack_x1, stack_y1 = 40, 60
        stack_w = 180
        stack_h = max(260, h - 90)
        self._draw_stack(stack_x1, stack_y1, stack_w, stack_h, stack_items, current_step)

        # Draw Section 2: QUEUE (Right Area, Horizontal)
        queue_x1 = stack_x1 + stack_w + 60
        queue_y1 = 70
        queue_w = max(380, w - queue_x1 - 40)
        queue_h = 100
        self._draw_queue(queue_x1, queue_y1, queue_w, queue_h, queue_items, current_step)

        # Draw Section 3: COMPARISON POD (Middle Center)
        comp_x1 = queue_x1
        comp_y1 = queue_y1 + queue_h + 35
        comp_w = queue_w
        comp_h = max(130, h - comp_y1 - 25)
        self._draw_comparison_pod(comp_x1, comp_y1, comp_w, comp_h, current_step)

    def _draw_stack(self, x: int, y: int, width: int, height: int, items: List[str], current_step: Optional[StepEvent]):
        # Header
        self.canvas.create_text(x + width // 2, y - 18, text="STACK (LIFO)", font=("Segoe UI", 11, "bold"), fill=TEXT_DARK)
        self.canvas.create_text(x + width // 2, y - 4, text="Last-In, First-Out (Reversed)", font=("Segoe UI", 8), fill=TEXT_MUTED)

        # Container outline (open top, solid walls)
        wall_color = "#94A3B8"
        self.canvas.create_line(x, y + 10, x, y + height, fill=wall_color, width=3)
        self.canvas.create_line(x, y + height, x + width, y + height, fill=wall_color, width=4)
        self.canvas.create_line(x + width, y + 10, x + width, y + height, fill=wall_color, width=3)

        # Base label
        self.canvas.create_text(x + width // 2, y + height + 14, text="[ Stack Base ]", font=("Segoe UI", 8), fill=TEXT_MUTED)

        # Draw Elements
        max_visible = 8
        displayed_items = items[-max_visible:] if len(items) > max_visible else items
        block_h = 28
        block_w = width - 24

        curr_y = y + height - 8 - block_h
        for idx, ch in enumerate(displayed_items):
            bx1 = x + 12
            bx2 = bx1 + block_w
            by1 = curr_y
            by2 = by1 + block_h

            is_top = (idx == len(displayed_items) - 1)
            fill_color = STACK_COLOR if not is_top else "#2563EB"

            # Draw block
            self.canvas.create_rectangle(bx1, by1, bx2, by2, fill=fill_color, outline="#1E3A8A", width=1)
            self.canvas.create_text((bx1 + bx2) // 2, (by1 + by2) // 2, text=f"'{ch}'", font=("Consolas", 12, "bold"), fill="#FFFFFF")

            # TOP pointer indicator
            if is_top:
                self.canvas.create_text(bx2 + 8, (by1 + by2) // 2, anchor="w", text="◄ TOP", font=("Segoe UI", 9, "bold"), fill=ACCENT_PRIMARY)

            curr_y -= (block_h + 4)

        if len(items) == 0:
            self.canvas.create_text(x + width // 2, y + height // 2, text="[ Stack is Empty ]", font=("Segoe UI", 9, "italic"), fill=TEXT_MUTED)

    def _draw_queue(self, x: int, y: int, width: int, height: int, items: List[str], current_step: Optional[StepEvent]):
        # Header
        self.canvas.create_text(x + 120, y - 18, text="QUEUE (FIFO)", font=("Segoe UI", 11, "bold"), fill=TEXT_DARK)
        self.canvas.create_text(x + 120, y - 4, text="First-In, First-Out (Original Order)", font=("Segoe UI", 8), fill=TEXT_MUTED)

        # Conveyor channel lines (top and bottom horizontal rails)
        rail_color = "#94A3B8"
        self.canvas.create_line(x, y + 15, x + width, y + 15, fill=rail_color, width=3)
        self.canvas.create_line(x, y + height - 15, x + width, y + height - 15, fill=rail_color, width=3)

        # Labels for FRONT and REAR
        self.canvas.create_text(x + 15, y + height // 2, anchor="e", text="FRONT\n(Dequeue)", font=("Segoe UI", 8, "bold"), fill="#475569", justify="center")
        self.canvas.create_text(x + width - 10, y + height // 2, anchor="w", text="REAR\n(Enqueue)", font=("Segoe UI", 8, "bold"), fill="#475569", justify="center")

        # Draw Queue elements
        max_visible = 10
        displayed_items = items[:max_visible]
        block_w = 34
        block_h = height - 44

        curr_x = x + 35
        for idx, ch in enumerate(displayed_items):
            bx1 = curr_x
            bx2 = bx1 + block_w
            by1 = y + 22
            by2 = by1 + block_h

            is_front = (idx == 0)
            fill_color = QUEUE_COLOR if not is_front else "#7C3AED"

            self.canvas.create_rectangle(bx1, by1, bx2, by2, fill=fill_color, outline="#4C1D95", width=1)
            self.canvas.create_text((bx1 + bx2) // 2, (by1 + by2) // 2, text=f"'{ch}'", font=("Consolas", 11, "bold"), fill="#FFFFFF")

            # FRONT / REAR pointers
            if is_front:
                self.canvas.create_text((bx1 + bx2) // 2, by1 - 8, text="▲ FRONT", font=("Segoe UI", 7, "bold"), fill=ACCENT_SECONDARY)

            curr_x += (block_w + 6)

        if len(items) == 0:
            self.canvas.create_text(x + width // 2, y + height // 2, text="[ Queue is Empty ]", font=("Segoe UI", 9, "italic"), fill=TEXT_MUTED)

    def _draw_comparison_pod(self, x: int, y: int, width: int, height: int, current_step: Optional[StepEvent]):
        # Background box for comparison pod
        self.canvas.create_rectangle(x, y, x + width, y + height, fill="#F8FAFC", outline=BORDER_COLOR, width=1)

        self.canvas.create_text(x + 20, y + 18, anchor="w", text="ACTIVE COMPARISON ENGINE", font=("Segoe UI", 10, "bold"), fill=TEXT_DARK)

        if not current_step or current_step.phase != "COMPARE":
            # Idle / Insert phase message
            info_msg = (
                "Waiting for character comparison phase...\n\n"
                "In comparison phase: Characters will be simultaneously Popped from Stack (LIFO) "
                "and Dequeued from Queue (FIFO) to check for symmetry."
            )
            self.canvas.create_text(x + 20, y + 55, anchor="nw", text=info_msg, font=("Segoe UI", 9), fill=TEXT_MUTED)
            return

        # We are actively comparing!
        s_char = current_step.stack_char or "?"
        q_char = current_step.queue_char or "?"
        is_match = current_step.is_match

        # Box 1: Stack Pop Character
        b1_x = x + 40
        b1_y = y + 40
        self.canvas.create_rectangle(b1_x, b1_y, b1_x + 90, b1_y + 60, fill="#DBEAFE", outline="#3B82F6", width=2)
        self.canvas.create_text(b1_x + 45, b1_y + 16, text="Stack (LIFO)", font=("Segoe UI", 8, "bold"), fill="#1E40AF")
        self.canvas.create_text(b1_x + 45, b1_y + 42, text=f"'{s_char}'", font=("Consolas", 18, "bold"), fill="#1E40AF")

        # Operator: == or !=
        op_x = b1_x + 125
        op_y = b1_y + 30
        op_symbol = "==" if is_match else "≠"
        op_color = ACCENT_SUCCESS if is_match else ACCENT_ERROR
        self.canvas.create_text(op_x, op_y, text=op_symbol, font=("Segoe UI", 24, "bold"), fill=op_color)

        # Box 2: Queue Dequeue Character
        b2_x = op_x + 35
        b2_y = b1_y
        self.canvas.create_rectangle(b2_x, b2_y, b2_x + 90, b2_y + 60, fill="#EDE9FE", outline="#8B5CF6", width=2)
        self.canvas.create_text(b2_x + 45, b2_y + 16, text="Queue (FIFO)", font=("Segoe UI", 8, "bold"), fill="#5B21B6")
        self.canvas.create_text(b2_x + 45, b2_y + 42, text=f"'{q_char}'", font=("Consolas", 18, "bold"), fill="#5B21B6")

        # Verdict Badge for this step
        v_x = b2_x + 120
        v_y = b1_y + 10
        badge_color = ACCENT_SUCCESS if is_match else ACCENT_ERROR
        status_text = "MATCH ✓" if is_match else "MISMATCH ✗"
        self.canvas.create_rectangle(v_x, v_y, v_x + 140, v_y + 40, fill=badge_color, outline="")
        self.canvas.create_text(v_x + 70, v_y + 20, text=status_text, font=("Segoe UI", 11, "bold"), fill="#FFFFFF")

        step_info = f"Step #{current_step.step_number}: Comparison check {s_char} vs {q_char}"
        self.canvas.create_text(x + 20, y + height - 15, anchor="w", text=step_info, font=("Segoe UI", 8, "italic"), fill=TEXT_MUTED)

    def save_screenshot(self):
        """
        Saves screenshot of the canvas/application.
        """
        default_filename = "gui_screenshot.png"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            initialfile=default_filename
        )
        if not filepath:
            return

        try:
            # First attempt PIL ImageGrab
            from PIL import ImageGrab
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            img.save(filepath)
            messagebox.showinfo("Screenshot Saved", f"Successfully saved screenshot to:\n{filepath}")
        except Exception as e:
            # Fallback: Postscript export from canvas
            try:
                ps_path = filepath.replace(".png", ".ps")
                self.canvas.postscript(file=ps_path, colormode="color")
                messagebox.showinfo("Exported PostScript", f"Saved canvas vector capture to:\n{ps_path}")
            except Exception as e2:
                messagebox.showerror("Error", f"Failed to save screenshot:\n{e}\n{e2}")


def run_gui():
    root = tk.Tk()
    app = PalindromeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
