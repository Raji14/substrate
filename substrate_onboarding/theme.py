"""Theme, color tokens, and ASCII styling for Agent Substrate Onboarding TUI.

Follows Google Material 3 (Material You) Dark Surface tokens and 4-Color Brand Palette:
- Google Blue:   #8ab4f8 / #a8c7fa / #0842a0
- Google Red:    #f28b82
- Google Yellow: #fdd663
- Google Green:  #81c995
- Dark Surfaces: #131314 (Base), #1e1f20 (Panels), #28292a (Cards), #333538 (Hover), #444746 (Outlines)
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
            # Smooth diagonal sweep
            diag_pos = (x / line_len * 0.7) + (y / total_lines * 0.3)
            r, g, b = get_gradient_color(diag_pos)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            rich_text.append(char, style=Style(color=hex_color, bold=True))
        if y < total_lines - 1:
            rich_text.append("\n")
    return rich_text


# Backward compatibility alias
apply_pastel_gradient = apply_google_gradient


APP_CSS = """
Screen {
    background: #131314;
    color: #e3e3e3;
    layers: base modal;
    layout: vertical;
}

#screen-container {
    width: 100%;
    height: 1fr;
    padding: 1 2;
    align: center middle;
    overflow-y: auto;
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

/* Welcome Screen */
#welcome-box {
    width: 96;
    height: auto;
    max-height: 95%;
    border: round #444746;
    background: #1e1f20;
    padding: 1 3;
    align: center middle;
}

#ascii-container {
    width: 100%;
    height: auto;
    content-align: center middle;
    margin-bottom: 1;
}

#typewriter-text {
    width: 100%;
    height: auto;
    min-height: 3;
    color: #e3e3e3;
    margin: 1 0;
}

#welcome-features-card {
    width: 100%;
    margin: 1 0;
}

#cta-prompt {
    width: 100%;
    content-align: center middle;
    color: #a8c7fa;
    text-style: bold;
    margin-top: 1;
}

/* Questionnaire Screen */
#wizard-box {
    width: 96;
    height: auto;
    max-height: 95%;
    border: round #444746;
    background: #1e1f20;
    padding: 1 3;
}

.wizard-step-title {
    color: #a8c7fa;
    text-style: bold;
    margin-bottom: 1;
}

.wizard-step-subtitle {
    color: #9aa0a6;
    margin-bottom: 1;
}

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

/* Doctor Screen */
#doctor-box {
    width: 96;
    height: auto;
    max-height: 95%;
    border: round #444746;
    background: #1e1f20;
    padding: 1 3;
}

#doctor-list {
    width: 100%;
    height: auto;
    margin: 1 0;
}

.doctor-item-row {
    width: 100%;
    height: auto;
    background: #28292a;
    border-left: solid #444746;
    padding: 0 1;
    margin-bottom: 1;
}

.doctor-item-row.-ok {
    border-left: heavy #81c995;
}

.doctor-item-row.-warning {
    border-left: heavy #fdd663;
}

.doctor-item-row.-failed {
    border-left: heavy #f28b82;
}

.doctor-item-row.-running {
    border-left: heavy #a8c7fa;
}

.remedy-box {
    width: 100%;
    background: #131314;
    border: solid #444746;
    color: #fdd663;
    padding: 0 1;
    margin: 0 0 1 1;
}

/* Auth Screen */
#auth-box {
    width: 92;
    height: auto;
    max-height: 95%;
    border: round #444746;
    background: #1e1f20;
    padding: 1 3;
}

#auth-inputs-container {
    width: 100%;
    margin: 1 0;
}

#api-key-label {
    color: #a8c7fa;
    text-style: bold;
    margin-bottom: 1;
}

#api-key-input-row {
    width: 100%;
    height: auto;
    align: center middle;
}

#api-key-input {
    width: 1fr;
    border: solid #444746;
    background: #131314;
    color: #f2f2f2;
}

#api-key-input:focus {
    border: solid #a8c7fa;
}

#btn-toggle-mask {
    min-width: 12;
    margin-left: 1;
}

#iap-info-card {
    width: 100%;
    margin: 1 0;
}

#oauth-status-label {
    width: 100%;
    content-align: center middle;
    margin: 1 0;
}

.error-pill {
    color: #f28b82;
    text-style: bold;
    background: #371b1d;
    border: solid #f28b82;
    padding: 0 1;
    margin-top: 1;
    display: none;
}

.error-pill.-visible {
    display: block;
}

/* Buttons and Controls with Adequate Padding (Zero Label Bleed) */
Button {
    height: 3;
    min-width: 18;
    padding: 0 2;
    content-align: center middle;
}

.auth-button-row {
    width: 100%;
    height: auto;
    align: center middle;
    margin: 1 0;
}

.action-button {
    margin: 0 1;
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
    margin: 0 1;
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

/* Summary Screen */
#summary-box {
    width: 96;
    height: auto;
    max-height: 95%;
    border: round #444746;
    background: #1e1f20;
    padding: 1 3;
}

#summary-card {
    width: 100%;
    margin: 0 0 1 0;
    padding: 0;
}

#progress-container {
    width: 100%;
    margin: 0;
    padding: 0;
}

#launch-progress-bar {
    width: 100%;
}

#launch-progress-label {
    color: #a8c7fa;
    text-style: italic;
    margin-top: 1;
    content-align: center middle;
}

#celebration-container {
    width: 100%;
    margin: 0;
    padding: 0;
}

#celebration-banner {
    width: 100%;
    background: #132219;
    border: round #81c995;
    padding: 1 2;
    margin: 0;
}

/* Modals */
.modal-dialog {
    width: 78;
    height: auto;
    background: #1e1f20;
    border: heavy #a8c7fa;
    padding: 1 2;
    align: center middle;
}

.modal-title {
    color: #a8c7fa;
    text-style: bold;
    content-align: center middle;
    margin-bottom: 1;
}

.modal-content {
    color: #e3e3e3;
    margin-bottom: 1;
}
"""
