"""Theme, color tokens, and styling for Agent Substrate Onboarding TUI.

Matches the clean, high-taste dark aesthetic:
- Deep dark navy base: #090d16 (Sidebar), #0d1117 (Content/Cards), #161b22 (Commands)
- Accent Cyan/Blue:    #70d6ff / #8ab4f8 / #1565c0
- Accent Green:        #81c995 / #00e676
- Accent Yellow:       #fdd663
- Borders & Outlines:  #21262d / #30363d / #444746
"""

from __future__ import annotations

from typing import List, Tuple
from rich.style import Style
from rich.text import Text

M3_SURFACE = "#0d1117"
M3_SURFACE_PANEL = "#090d16"
M3_SURFACE_CARD = "#161b22"
M3_SURFACE_HOVER = "#21262d"
M3_OUTLINE = "#30363d"
M3_OUTLINE_FOCUS = "#70d6ff"

GOOGLE_BLUE = "#70d6ff"
GOOGLE_RED = "#f28b82"
GOOGLE_YELLOW = "#fdd663"
GOOGLE_GREEN = "#81c995"

M3_TEXT_PRIMARY = "#e3e3e3"
M3_TEXT_MUTED = "#80868b"
M3_TEXT_WHITE = "#ffffff"


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def get_gradient_color(progress: float) -> Tuple[int, int, int]:
    stops = [
        hex_to_rgb(GOOGLE_BLUE),
        hex_to_rgb(GOOGLE_RED),
        hex_to_rgb(GOOGLE_YELLOW),
        hex_to_rgb(GOOGLE_GREEN),
        hex_to_rgb(GOOGLE_BLUE),
    ]
    p = max(0.0, min(1.0, progress))
    num_segments = len(stops) - 1
    segment_idx = min(int(p * num_segments), num_segments - 1)
    seg_progress = (p * num_segments) - segment_idx
    c1, c2 = stops[segment_idx], stops[segment_idx + 1]
    return (
        int(c1[0] + (c2[0] - c1[0]) * seg_progress),
        int(c1[1] + (c2[1] - c1[1]) * seg_progress),
        int(c1[2] + (c2[2] - c1[2]) * seg_progress),
    )


def apply_google_gradient(text_lines: List[str]) -> Text:
    """Helper for logo gradient rendering."""
    rich_text = Text()
    for y, line in enumerate(text_lines):
        rich_text.append(line, style="bold #70d6ff")
        if y < len(text_lines) - 1:
            rich_text.append("\n")
    return rich_text


apply_pastel_gradient = apply_google_gradient


APP_CSS = """
Screen {
    background: #090d16;
    color: #e3e3e3;
    layers: base modal;
    layout: vertical;
}

/* Welcome Screen Hero & Cards */
#welcome-main-container {
    width: 100%;
    height: 1fr;
    background: #090d16;
    padding: 1 3;
    overflow-y: auto;
    align: center top;
}

#welcome-hero-logo {
    width: 100%;
    height: auto;
    text-align: center;
    margin-top: 1;
    margin-bottom: 0;
}

#welcome-hero-subtitle {
    width: 100%;
    text-align: center;
    color: #70d6ff;
    text-style: bold;
    margin-bottom: 1;
}

#welcome-features-row {
    width: 100%;
    height: auto;
    margin-bottom: 1;
}

.wonder-feature-card {
    width: 1fr;
    height: auto;
    background: #161b22;
    border: solid #30363d;
    padding: 1 2;
    margin: 0 1;
}

#welcome-tracks-title {
    color: #ffffff;
    text-style: bold;
    margin-top: 1;
    margin-bottom: 1;
}

#welcome-tracks-list {
    width: 100%;
    height: auto;
}

.track-option-card {
    width: 100%;
    height: auto;
    background: #161b22;
    border: solid #30363d;
    padding: 1 2;
    margin-bottom: 1;
}

#welcome-preflight-badge {
    width: 100%;
    height: auto;
    background: #0d1117;
    border: solid #21262d;
    padding: 1 2;
    margin-top: 1;
    text-align: center;
}

#welcome-action-row {
    width: 100%;
    height: auto;
    align: right middle;
    margin-top: 1;
    margin-bottom: 1;
}

/* Workspace 2-Column Grid Layout */
#workspace-layout {
    width: 100%;
    height: 1fr;
    layout: horizontal;
    background: #090d16;
}

#sidebar-nav {
    width: 30;
    height: 100%;
    background: #090d16;
    border-right: solid #21262d;
    padding: 2 2;
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
    background: #0d1117;
    padding: 2 3;
    overflow-y: auto;
}

#content-panel {
    width: 100%;
    height: auto;
}

.step-indicator-label {
    color: #80868b;
    margin-bottom: 0;
}

.wizard-step-title {
    color: #ffffff;
    text-style: bold;
    margin-bottom: 1;
}

.wizard-step-description {
    color: #e3e3e3;
    margin-bottom: 1;
}

/* Real Command Callout */
#command-callout-card {
    width: 100%;
    height: auto;
    background: #161b22;
    border: solid #30363d;
    padding: 1 2;
    margin: 1 0;
}

.section-subtitle-label {
    color: #ffffff;
    text-style: bold;
    margin-top: 1;
    margin-bottom: 1;
}

#cluster-selection-list {
    width: 100%;
    height: auto;
    margin-bottom: 1;
}

.cluster-option-row {
    width: 100%;
    height: auto;
    background: #161b22;
    border: solid #30363d;
    padding: 1 2;
    margin-bottom: 1;
}

#cluster-verification-box {
    width: 100%;
    height: auto;
    background: #11151c;
    border: solid #30363d;
    padding: 1 2;
    margin: 1 0;
}

/* Execution Checklist Card */
#execution-checklist-card {
    width: 100%;
    height: auto;
    background: #090d16;
    border: solid #21262d;
    padding: 1 2;
    margin: 1 0;
}

/* Button Rows */
.action-button-row {
    width: 100%;
    height: auto;
    align: right middle;
    margin-top: 2;
}

.action-button {
    margin-left: 1;
    background: #1565c0;
    color: #ffffff;
    border: solid #70d6ff;
    text-style: bold;
    min-width: 24;
}

.action-button:hover {
    background: #1976d2;
    color: #ffffff;
}

.secondary-button {
    margin-right: 1;
    background: #161b22;
    color: #e3e3e3;
    border: solid #30363d;
    min-width: 16;
}

.secondary-button:hover {
    background: #21262d;
    color: #70d6ff;
    border: solid #70d6ff;
}

/* Bottom Bar */
#bottom-bar {
    dock: bottom;
    height: 3;
    background: #090d16;
    border-top: solid #21262d;
    padding: 0 2;
}

#status-tip {
    color: #70d6ff;
    text-style: italic;
    width: 1fr;
}

#keyboard-hints {
    color: #80868b;
    text-align: right;
    width: auto;
}

/* Top Header */
#top-header {
    dock: top;
    height: 3;
    background: #090d16;
    color: #e3e3e3;
    border-bottom: solid #21262d;
    padding: 0 2;
}

#header-brand {
    width: auto;
}

#header-stepper {
    color: #80868b;
    text-align: right;
    width: 1fr;
}

/* Modals */
#help-modal-container {
    width: 80;
    height: auto;
    background: #161b22;
    border: round #70d6ff;
    padding: 1 2;
}

#exit-modal-container {
    width: 60;
    height: auto;
    background: #161b22;
    border: round #f28b82;
    padding: 1 2;
    align: center middle;
}
"""
