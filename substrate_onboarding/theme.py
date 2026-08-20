"""Theme, color tokens, and styling for Agent Substrate Onboarding TUI.

Follows Google Material 3 (Material You) Dark Surface tokens and 4-Color Brand Palette:
- Google Blue:   #8ab4f8 / #a8c7fa / #0842a0
- Google Red:    #f28b82
- Google Yellow: #fdd663
- Google Green:  #81c995
- Dark Surfaces: #131314 (Base), #1e1f20 (Panels/Sidebar), #28292a (Cards), #333538 (Hover), #444746 (Outlines)
"""

from __future__ import annotations

from typing import List, Tuple
from rich.style import Style
from rich.text import Text

# Google Material 3 Dark Surface Color Tokens
M3_SURFACE = "#131314"
M3_SURFACE_PANEL = "#1e1f20"
M3_SURFACE_CARD = "#28292a"
M3_SURFACE_HOVER = "#333538"
M3_OUTLINE = "#444746"
M3_OUTLINE_FOCUS = "#8ab4f8"

# Google Brand Palette
M3_PRIMARY = "#a8c7fa"
M3_ON_PRIMARY = "#003062"
M3_PRIMARY_CONTAINER = "#0842a0"
M3_ON_PRIMARY_CONTAINER = "#d3e3fd"

GOOGLE_BLUE = "#8ab4f8"
GOOGLE_RED = "#f28b82"
GOOGLE_YELLOW = "#fdd663"
GOOGLE_GREEN = "#81c995"

M3_TEXT_PRIMARY = "#e3e3e3"
M3_TEXT_MUTED = "#9aa0a6"
M3_TEXT_WHITE = "#ffffff"


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert hex color string (#rrggbb) to RGB tuple."""
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def interpolate_rgb(
    c1: Tuple[int, int, int], c2: Tuple[int, int, int], factor: float
) -> Tuple[int, int, int]:
    """Linearly interpolate between two RGB colors."""
    factor = max(0.0, min(1.0, factor))
    return (
        int(c1[0] + (c2[0] - c1[0]) * factor),
        int(c1[1] + (c2[1] - c1[1]) * factor),
        int(c1[2] + (c2[2] - c1[2]) * factor),
    )


def get_gradient_color(progress: float) -> Tuple[int, int, int]:
    """Get interpolated RGB tuple across Google 4-color gradient stops."""
    stops = [
        hex_to_rgb(GOOGLE_BLUE),
        hex_to_rgb(GOOGLE_RED),
        hex_to_rgb(GOOGLE_YELLOW),
        hex_to_rgb(GOOGLE_GREEN),
        hex_to_rgb(M3_PRIMARY),
    ]
    p = max(0.0, min(1.0, progress))
    num_segments = len(stops) - 1
    segment_idx = min(int(p * num_segments), num_segments - 1)
    seg_progress = (p * num_segments) - segment_idx
    return interpolate_rgb(stops[segment_idx], stops[segment_idx + 1], seg_progress)


def apply_google_gradient(text_lines: List[str]) -> Text:
    """Apply horizontal and diagonal Google 4-color gradient to ASCII art or multi-line text."""
    rich_text = Text()
    total_lines = max(1, len(text_lines))

    for y, line in enumerate(text_lines):
        line_len = max(1, len(line))
        for x, char in enumerate(line):
            if char.isspace():
                rich_text.append(char)
                continue
            diag_pos = (x / line_len * 0.7) + (y / total_lines * 0.3)
            r, g, b = get_gradient_color(diag_pos)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            rich_text.append(char, style=Style(color=hex_color, bold=True))
        if y < total_lines - 1:
            rich_text.append("\n")
    return rich_text


apply_pastel_gradient = apply_google_gradient


APP_CSS = """
Screen {
    background: #131314;
    color: #e3e3e3;
    layers: base modal;
    layout: vertical;
}

/* Header & Status Bar */
#top-header {
    dock: top;
    height: 3;
    background: #1e1f20;
    color: #e3e3e3;
    border-bottom: hkey #333538;
    padding: 0 2;
    content-align: center middle;
}

#header-brand {
    width: auto;
}

#header-stepper {
    color: #9aa0a6;
    text-align: right;
    width: 1fr;
}

#bottom-bar {
    dock: bottom;
    height: 3;
    background: #1e1f20;
    border-top: hkey #333538;
    padding: 0 2;
}

#status-tip {
    color: #d3e3fd;
    text-style: italic;
    width: 1fr;
}

#keyboard-hints {
    color: #9aa0a6;
    text-align: right;
    width: auto;
}

/* 2-Column Wizard Layout */
#workspace-layout {
    width: 100%;
    height: 1fr;
    layout: horizontal;
    background: #131314;
}

#sidebar-nav {
    width: 32;
    height: 100%;
    background: #1e1f20;
    border-right: round #444746;
    padding: 1 1;
}

#sidebar-container {
    width: 100%;
    height: auto;
}

#sidebar-content {
    width: 100%;
    height: auto;
}

#content-area {
    width: 1fr;
    height: 1fr;
    padding: 1 2;
    overflow-y: auto;
}

#content-panel {
    width: 100%;
    height: auto;
    background: #1e1f20;
    border: round #444746;
    padding: 1 2;
}

.wizard-step-title {
    color: #a8c7fa;
    text-style: bold;
    margin-bottom: 0;
}

.wizard-step-subtitle {
    color: #9aa0a6;
    margin-bottom: 1;
}

/* Log and Diagnostic Cards */
#terminal-log-card {
    width: 100%;
    height: auto;
    background: #131314;
    border: round #444746;
    padding: 1 2;
    margin: 1 0;
}

/* Actionable Remedy Card */
#remedy-card {
    width: 100%;
    height: auto;
    background: #201a14;
    border: round #fdd663;
    padding: 1 2;
    margin: 1 0;
}

/* Options Container & Cards */
#options-container {
    width: 100%;
    height: auto;
    margin: 1 0;
}

.option-card {
    width: 100%;
    height: auto;
    min-height: 3;
    background: #28292a;
    border: round #444746;
    margin-bottom: 1;
    padding: 0 1;
    color: #e3e3e3;
}

.option-card:hover {
    background: #333538;
    border: round #8ab4f8;
}

.option-card.-active {
    background: #0842a0;
    border: round #a8c7fa;
    color: #ffffff;
    text-style: bold;
}

/* Button Rows */
.action-button-row {
    width: 100%;
    height: auto;
    align: right middle;
    margin-top: 1;
}

.action-button {
    margin-left: 1;
    background: #0842a0;
    color: #d3e3fd;
    border: solid #a8c7fa;
    text-style: bold;
    min-width: 22;
}

.action-button:hover {
    background: #0b57d0;
    color: #ffffff;
}

.secondary-button {
    margin-right: 1;
    background: #28292a;
    color: #e3e3e3;
    border: solid #444746;
    min-width: 18;
}

.secondary-button:hover {
    background: #333538;
    color: #a8c7fa;
    border: solid #8ab4f8;
}

/* Modals */
#help-modal-container {
    width: 80;
    height: auto;
    max-height: 90%;
    background: #1e1f20;
    border: round #a8c7fa;
    padding: 1 2;
}

#exit-modal-container {
    width: 60;
    height: auto;
    background: #1e1f20;
    border: round #f28b82;
    padding: 1 2;
    align: center middle;
}
"""
