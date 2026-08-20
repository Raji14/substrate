"""High-Definition (1080p/720p) Video Recording Generator for Agent Substrate Onboarding.

Renders each scene, animation frame, keyboard interaction, doctor check, and modal dialog
into a video file (onboarding_demo.mp4) with Google Material 3 tokens, rich icons,
and pixel-perfect button layouts with zero label bleeding.
"""

import os
import sys
import numpy as np
import imageio
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1280
HEIGHT = 720
FPS = 30

# Colors (Google Material 3 Dark Theme)
BG_CANVAS = (19, 19, 20)           # #131314
SURFACE_PANEL = (30, 31, 32)       # #1e1f20
CARD_BG = (40, 41, 42)             # #28292a
CARD_HOVER = (51, 53, 56)          # #333538
CARD_ACTIVE = (8, 66, 160)         # #0842a0 (Primary Container)
BORDER_COLOR = (68, 71, 70)        # #444746
BORDER_FOCUS = (138, 180, 248)     # #8ab4f8
TEXT_PRIMARY = (227, 227, 227)     # #e3e3e3
TEXT_MUTED = (154, 160, 166)       # #9aa0a6
TEXT_WHITE = (255, 255, 255)

# Google 4-Colors
GOOGLE_BLUE = (138, 180, 248)      # #8ab4f8
GOOGLE_RED = (242, 139, 130)       # #f28b82
GOOGLE_YELLOW = (253, 214, 99)     # #fdd663
GOOGLE_GREEN = (129, 201, 149)     # #81c995
M3_PRIMARY = (168, 199, 250)       # #a8c7fa

# Font loading
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/SFNSMono.ttf"

font_xs = ImageFont.truetype(FONT_PATH, 11)
font_sm = ImageFont.truetype(FONT_PATH, 13)
font_base = ImageFont.truetype(FONT_PATH, 15)
font_md = ImageFont.truetype(FONT_PATH, 17)
font_lg = ImageFont.truetype(FONT_PATH, 20)
font_logo = ImageFont.truetype(FONT_PATH, 13)

SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def get_google_gradient_color(progress: float):
    stops = [
        (138, 180, 248),  # Blue
        (242, 139, 130),  # Red
        (253, 214, 99),   # Yellow
        (129, 201, 149),  # Green
        (168, 199, 250),  # Light Blue
    ]
    p = max(0.0, min(1.0, progress))
    num_seg = len(stops) - 1
    idx = min(int(p * num_seg), num_seg - 1)
    seg_p = (p * num_seg) - idx
    c1, c2 = stops[idx], stops[idx + 1]
    r = int(c1[0] + (c2[0] - c1[0]) * seg_p)
    g = int(c1[1] + (c2[1] - c1[1]) * seg_p)
    b = int(c1[2] + (c2[2] - c1[2]) * seg_p)
    return (r, g, b)


def draw_pill_button(draw, right_x, y, text, is_primary=True, outline_color=None, custom_font=font_xs):
    """Draws a button calculated from text bounds so label NEVER bleeds outside."""
    bbox = custom_font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    pad_h = 16
    pad_v = 10
    btn_w = text_w + (pad_h * 2)
    btn_h = text_h + (pad_v * 2)
    
    left_x = right_x - btn_w
    top_y = y
    
    bg = CARD_ACTIVE if is_primary else CARD_BG
    out = outline_color or (M3_PRIMARY if is_primary else BORDER_COLOR)
    fg = TEXT_WHITE if is_primary else (M3_PRIMARY if outline_color else TEXT_MUTED)
    
    draw.rounded_rectangle([left_x, top_y, right_x, top_y + btn_h], radius=6, fill=bg, outline=out, width=1)
    draw.text((left_x + pad_h, top_y + pad_v - 1), text, font=custom_font, fill=fg)
    
    return left_x - 12  # returns next right_x for left-adjacent button


def draw_window_base(draw, title_step=1, active_step_name="1. Welcome", tip_text="", legend_text=""):
    """Draw the outer terminal frame, title bar, stepper breadcrumbs, and bottom status bar."""
    # Background radial wash
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=BG_CANVAS)

    # Window Outer Box
    wx, wy, ww, wh = 100, 35, 1080, 650
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=14, fill=SURFACE_PANEL, outline=BORDER_COLOR, width=1)

    # Title Bar
    draw.rectangle([wx, wy, wx + ww, wy + 38], fill=(26, 27, 28))
    draw.line([wx, wy + 38, wx + ww, wy + 38], fill=BORDER_COLOR, width=1)

    # Mac dots
    draw.ellipse([wx + 16, wy + 13, wx + 28, wy + 25], fill=(255, 95, 86))
    draw.ellipse([wx + 34, wy + 13, wx + 46, wy + 25], fill=(255, 189, 46))
    draw.ellipse([wx + 52, wy + 13, wx + 64, wy + 25], fill=(39, 201, 63))

    # Window Title
    title_str = "⚡ Agent Substrate Onboarding — GKE Workload Multiplexing"
    draw.text((wx + ww // 2 - 240, wy + 11), title_str, font=font_sm, fill=TEXT_MUTED)

    # Stepper Bar with Snazzy Icons
    sy = wy + 39
    draw.rectangle([wx, sy, wx + ww, sy + 32], fill=(22, 23, 24))
    draw.line([wx, sy + 32, wx + ww, sy + 32], fill=BORDER_COLOR, width=1)

    steps = [
        (1, "🩺 1. Pre-Flight"),
        (2, "🛠️ 2. Platform Setup"),
        (3, "🤖 3. Agent Deployment"),
        (4, "🛸 4. Launchpad"),
    ]
    cur_x = wx + 18
    for step_num, step_name in steps:
        bbox = font_xs.getbbox(step_name)
        step_w = bbox[2] - bbox[0]
        if step_num == title_step:
            draw.rounded_rectangle([cur_x - 4, sy + 5, cur_x + step_w + 12, sy + 27], radius=6, fill=M3_PRIMARY)
            draw.text((cur_x + 2, sy + 7), step_name, font=font_xs, fill=(0, 48, 98))
            cur_x += step_w + 20
        else:
            draw.text((cur_x, sy + 8), step_name, font=font_xs, fill=TEXT_MUTED)
            cur_x += step_w + 8

        if step_num < 4:
            draw.text((cur_x, sy + 8), "›", font=font_xs, fill=(80, 84, 90))
            cur_x += 16

    if legend_text:
        bbox = font_xs.getbbox(legend_text)
        leg_w = bbox[2] - bbox[0]
        draw.text((wx + ww - leg_w - 18, sy + 8), legend_text, font=font_xs, fill=TEXT_MUTED)

    # Bottom Status Bar
    by = wy + wh - 36
    draw.rectangle([wx, by, wx + ww, wy + wh], fill=(26, 27, 28))
    draw.line([wx, by, wx + ww, by], fill=BORDER_COLOR, width=1)

    if tip_text:
        draw.text((wx + 18, by + 10), f"💡 {tip_text}", font=font_xs, fill=M3_PRIMARY)

    bottom_hints = "[Enter] Proceed  [/help] Help  [Ctrl+C] Exit"
    draw.text((wx + ww - 310, by + 10), bottom_hints, font=font_xs, fill=TEXT_MUTED)

    # Viewport Bounds: (wx + 20, wy + 85, ww - 40, wh - 130)
    return wx + 20, wy + 85, ww - 40, wh - 130


def render_scene_1_welcome(frame_idx, total_frames):
    """Scene 1: Welcome Splash with Google 4-Color Gradient & Typewriter."""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_CANVAS)
    draw = ImageDraw.Draw(img)

    tip = "Welcome to Agent Substrate. Press [Enter] to start your onboarding."
    vx, vy, vw, vh = draw_window_base(draw, title_step=1, tip_text=tip, legend_text="[Enter] Start  [/help] Help")

    # Card Panel
    cx, cy, cw, ch = vx + 80, vy + 15, vw - 160, vh - 30
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10, fill=(24, 25, 26), outline=BORDER_COLOR, width=1)

    # ASCII Logo with Google 4-Color Gradient
    logo_lines = [
        r"   ____  _   _ ____  ____ _____ ____     _  _____ _____ ",
        r"  / ___|| | | | __ )/ ___|_   _|  _ \   / \|_   _| ____|",
        r"  \___ \| | | |  _ \\___ \ | | | |_) | / _ \ | | |  _|  ",
        r"   ___) | |_| | |_) |___) || | |  _ < / ___ \| | | |___ ",
        r"  |____/ \___/|____/|____/ |_| |_| \_\_/   \_\_| |_____|",
    ]

    ly = cy + 25
    for y_idx, line in enumerate(logo_lines):
        lx = cx + (cw - len(line) * 8) // 2
        for x_idx, char in enumerate(line):
            if not char.isspace():
                p = (x_idx / len(line) * 0.7) + (y_idx / len(logo_lines) * 0.3)
                color = get_google_gradient_color(p)
                draw.text((lx + x_idx * 8, ly + y_idx * 16), char, font=font_logo, fill=color)

    # Subtitle with Snazzy Icon
    sub_title = "⚡ A G E N T   S U B S T R A T E ⚡"
    draw.text((cx + (cw - len(sub_title) * 8.5) // 2, cy + 120), sub_title, font=font_sm, fill=GOOGLE_BLUE)

    # Typewriter streaming
    full_intro = "Welcome to Agent Substrate on GKE — the high-density execution plane with a pierceable abstraction for Platform Engineers and AI Engineers."
    typed_len = min(len(full_intro), int((frame_idx / (total_frames * 0.65)) * len(full_intro)))
    typed_text = full_intro[:typed_len]

    # Wrap text cleanly
    line1 = typed_text[:88]
    line2 = typed_text[88:] if len(typed_text) > 88 else ""

    draw.text((cx + (cw - len(line1) * 7.5) // 2, cy + 150), line1, font=font_sm, fill=TEXT_PRIMARY)
    if line2:
        cursor = " ▌" if (frame_idx // 6) % 2 == 0 else ""
        draw.text((cx + (cw - len(line2) * 7.5) // 2, cy + 172), line2 + cursor, font=font_sm, fill=TEXT_PRIMARY)
    else:
        cursor = " ▌" if (frame_idx // 6) % 2 == 0 else ""
        draw.text((cx + (cw - len(line1) * 7.5) // 2 + len(line1) * 7.5, cy + 150), cursor, font=font_sm, fill=M3_PRIMARY)

    # Core Capabilities Feature Card with generous spacing & legible title
    fx, fy, fw, fh = cx + 60, cy + 205, cw - 120, 160
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=8, fill=(19, 20, 22), outline=GOOGLE_BLUE, width=1)

    # Title badge
    badge_text = " ⚡ CORE SUBSTRATE CAPABILITIES "
    bw = int(len(badge_text) * 8)
    draw.rounded_rectangle([fx + 20, fy - 10, fx + 20 + bw, fy + 12], radius=4, fill=(8, 66, 160), outline=M3_PRIMARY, width=1)
    draw.text((fx + 24, fy - 6), badge_text, font=font_xs, fill=(255, 255, 255))

    # Capability rows with generous vertical spacing
    row1_y = fy + 26
    draw.text((fx + 24, row1_y), "🛠️  Platform Fleet  :", font=font_sm, fill=M3_PRIMARY)
    draw.text((fx + 215, row1_y), "Warm worker pools on GKE with MicroVM & Spot buffers", font=font_sm, fill=(255, 255, 255))

    row2_y = fy + 68
    draw.text((fx + 24, row2_y), "🤖  Agent Workloads :", font=font_sm, fill=GOOGLE_GREEN)
    draw.text((fx + 215, row2_y), "No-YAML container templates, turn hooks & request parking", font=font_sm, fill=(255, 255, 255))

    row3_y = fy + 110
    draw.text((fx + 24, row3_y), "⚡  Instant Resume  :", font=font_sm, fill=GOOGLE_YELLOW)
    draw.text((fx + 215, row3_y), "Suspend idle actors to 0% CPU; restore state in <200ms", font=font_sm, fill=(255, 255, 255))

    # Pulsing CTA
    cta_text = "▶ Press [ENTER] to start Pre-Flight Diagnostics..."
    alpha_pulse = 1.0 if (frame_idx // 10) % 2 == 0 else 0.5
    cta_color = (int(M3_PRIMARY[0] * alpha_pulse), int(M3_PRIMARY[1] * alpha_pulse), int(M3_PRIMARY[2] * alpha_pulse))
    draw.text((cx + (cw - len(cta_text) * 8.5) // 2, cy + 395), cta_text, font=font_md, fill=cta_color)

    return np.array(img)


def render_scene_2_wizard(substep=0, selected_idx=0, frame_idx=0):
    """Scene 2: Guided Questionnaire Wizard with glowing selection cards."""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_CANVAS)
    draw = ImageDraw.Draw(img)

    substeps_data = [
        {
            "step_title": "🤖 Step 1 of 3: Persona & Architecture Target (Pierceable Abstraction)",
            "step_desc": "Select your role and multiplexing target for GKE worker pools & actor sessions:",
            "tip": "Runs 'atectl create workerpools' with capacity buffers, Custom Compute Classes (CCC), and Spot optimization.",
            "options": [
                ("🛠️", "Platform Engineer — Fleet WorkerPools", "Provision fungible, pre-warmed GKE worker pools with microVM/gVisor isolation"),
                ("🤖", "AI Engineer — No-YAML Agent Deployment", "Deploy ActorTemplates (OCI images) and multiplex sessions without Kubernetes YAML"),
                ("⚡", "Full-Stack Platform & Autonomous Swarms", "End-to-end setup: WorkerPool fleets, ActorTemplates, Envoy dataplane, & telemetry"),
                ("💻", "Local Dev & Rapid MicroVM Prototyping", "Fast iteration on macOS/Linux using Docker, Colima, or Kind clusters"),
            ],
        },
        {
            "step_title": "⚡ Step 2 of 3: WorkerPool & Dataplane Topology (--isolation / --workers)",
            "step_desc": "Select the worker fleet isolation boundary and state store architecture:",
            "tip": "Applies --isolation=microvm --workers=100 --atenet-router=envoy --store-backend=redis for sub-50ms resume.",
            "options": [
                ("⚡", "MicroVM WorkerPool + Envoy Dataplane", "100 pre-warmed workers (Cloud Hypervisor), Envoy proxy, and Redis state store"),
                ("🛡️", "gVisor WorkerPool + Agent Gateway Router", "Hardened userspace syscall sandboxing with dynamic TLS and stream multiplexing"),
                ("🐘", "Enterprise Multi-Tenant Fleet + PostgreSQL", "Relational persistence for multi-tenant audit logs, RBAC, and durable actor state"),
            ],
        },
        {
            "step_title": "🛡️ Step 3 of 3: Optimization & Image Pre-caching (--workerpool / precache)",
            "step_desc": "Select your image caching strategy and sandbox checkpointing storage:",
            "tip": "Enables 'atectl precache image' for instant zero-delay rollouts across worker nodes.",
            "options": [
                ("⚡", "Local SSD Image Pre-caching (RL & Large Models)", "Pre-warm heavy environment images onto Local SSDs to eliminate image pull delays"),
                ("🛡️", "Cloud Hypervisor MicroVM (Hardware Virtualized)", "Hardware-virtualized microVM isolation with nested virtualization on N2/C3/C4 nodes"),
                ("🪣", "GCS Snapshot Checkpointing (L2 Storage)", "Persistent GCS bucket for microVM memory/disk state suspend and resume"),
            ],
        },
    ]

    cur_data = substeps_data[substep]
    vx, vy, vw, vh = draw_window_base(
        draw,
        title_step=2,
        tip_text=cur_data["tip"],
        legend_text=f"[↑/↓] Select ({selected_idx + 1}/{len(cur_data['options'])})  [Enter] Next",
    )

    # Card Panel
    cx, cy, cw, ch = vx + 40, vy + 10, vw - 80, vh - 20
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10, fill=(24, 25, 26), outline=BORDER_COLOR, width=1)

    # Headers with Snazzy Icons
    draw.text((cx + 24, cy + 20), "🛠️ STEP 2: PLATFORM SETUP & WORKERPOOL TOPOLOGY", font=font_md, fill=M3_PRIMARY)
    draw.text((cx + 24, cy + 46), cur_data["step_title"], font=font_sm, fill=M3_PRIMARY)
    draw.text((cx + 24, cy + 66), cur_data["step_desc"], font=font_xs, fill=TEXT_MUTED)

    # Option Cards
    oy = cy + 96
    for idx, (icon, title, desc) in enumerate(cur_data["options"]):
        is_sel = idx == selected_idx
        card_fill = CARD_ACTIVE if is_sel else CARD_BG
        card_outline = M3_PRIMARY if is_sel else BORDER_COLOR
        card_w = cw - 48

        draw.rounded_rectangle([cx + 24, oy, cx + 24 + card_w, oy + 46], radius=8, fill=card_fill, outline=card_outline, width=2 if is_sel else 1)

        # Indicator
        ind = "▶" if is_sel else " "
        draw.text((cx + 36, oy + 14), ind, font=font_sm, fill=M3_PRIMARY)
        draw.text((cx + 56, oy + 13), icon, font=font_sm, fill=TEXT_WHITE)
        draw.text((cx + 88, oy + 14), title, font=font_sm, fill=TEXT_WHITE if is_sel else TEXT_PRIMARY)
        draw.text((cx + 88 + len(title) * 8 + 14, oy + 14), f"— {desc}", font=font_xs, fill=(211, 227, 253) if is_sel else TEXT_MUTED)

        oy += 56

    # Action Buttons with Dynamic Bounding (Zero Label Bleed)
    by = cy + ch - 48
    draw.line([cx + 24, by - 10, cx + cw - 24, by - 10], fill=BORDER_COLOR, width=1)

    # Right-aligned buttons
    rx = cx + cw - 24
    rx = draw_pill_button(draw, rx, by, "Next Step [Enter] →", is_primary=True)
    rx = draw_pill_button(draw, rx, by, "Skip Defaults (/skip)", is_primary=False)
    
    # Left-aligned back button
    draw_pill_button(draw, cx + 130, by, "← Back (b)", is_primary=False)

    return np.array(img)


def render_scene_3_doctor(frame_idx=0):
    """Scene 3: Environment Pre-Flight Doctor with live diagnostic probes, spinners, and inline remedy execution."""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_CANVAS)
    draw = ImageDraw.Draw(img)

    tip = "Running GKE, Cloud Hypervisor, and Substrate pre-flight diagnostic probes..."
    vx, vy, vw, vh = draw_window_base(draw, title_step=1, tip_text=tip, legend_text="[r] Re-run  [Enter] Proceed")

    cx, cy, cw, ch = vx + 40, vy + 10, vw - 80, vh - 20
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10, fill=(24, 25, 26), outline=BORDER_COLOR, width=1)

    # Headers with Snazzy Icon
    draw.text((cx + 24, cy + 20), "🩺 STEP 1: PRE-FLIGHT ENVIRONMENT & GKE DIAGNOSTICS", font=font_md, fill=M3_PRIMARY)
    draw.text((cx + 24, cy + 46), "Checking your local tools, connected GKE cluster, and cloud storage before starting...", font=font_xs, fill=TEXT_MUTED)

    # If frame_idx >= 105, simulate that inline fix was executed and Docker is now healthy!
    docker_is_fixed = frame_idx >= 105
    docker_status = "ok" if docker_is_fixed else "warning"
    docker_msg = "Docker sandbox started & ready (Colima runtime)" if docker_is_fixed else "Docker or Colima is not running"
    docker_remedy = None if docker_is_fixed else "open -a Docker || colima start"

    probes = [
        ("Version Control (Git)", "ok", "Git v2.55 (Identity: Rajitha Leonhard)", None, None, 10),
        ("Python Environment", "ok", "Python v3.13.7 (darwin) ready", None, None, 20),
        ("Agent Sandbox Engine (Docker / Colima)", docker_status, docker_msg, docker_remedy, "https://ate.dev/docs/sandboxes", 35),
        ("Connected Cloud Cluster (GKE / Kubectl)", "ok", "Connected to cluster context (gke-agent-cluster)", None, None, 50),
        ("Substrate Helper Tools (atectl)", "ok", "atectl CLI v0.17 ready (No-YAML agent operations)", None, None, 65),
        ("Cloud Connection & Memory Storage", "ok", "Cloud connection healthy (4ms) — memory saves instantly", None, None, 80),
    ]

    oy = cy + 74
    for name, status, msg, remedy, doc_url, trigger_frame in probes:
        card_w = cw - 48
        is_done = frame_idx >= trigger_frame
        is_running = not is_done and frame_idx >= trigger_frame - 15

        if is_running:
            b_color = M3_PRIMARY
            sp_char = SPINNER_FRAMES[(frame_idx // 3) % len(SPINNER_FRAMES)]
            main_text = f"{sp_char} Checking {name}... [RUNNING]"
            badge_text = "[RUNNING]"
            badge_col = M3_PRIMARY
        elif is_done:
            if status == "ok":
                b_color = GOOGLE_GREEN
                main_text = f"✓ Checking {name}... ({msg})"
                badge_text = "[OK]"
                badge_col = GOOGLE_GREEN
            else:
                b_color = GOOGLE_YELLOW
                main_text = f"▲ Checking {name}... ({msg})"
                badge_text = "[WARNING]"
                badge_col = GOOGLE_YELLOW
        else:
            b_color = BORDER_COLOR
            main_text = f"○ Checking {name}... [WAITING]"
            badge_text = "[PENDING]"
            badge_col = TEXT_MUTED

        draw.rounded_rectangle([cx + 24, oy, cx + 24 + card_w, oy + 32], radius=6, fill=CARD_BG)
        draw.line([cx + 24, oy, cx + 24, oy + 32], fill=b_color, width=4)

        draw.text((cx + 36, oy + 8), main_text, font=font_xs, fill=TEXT_WHITE if is_done else TEXT_MUTED)
        draw.text((cx + cw - 120, oy + 8), badge_text, font=font_xs, fill=badge_col)

        if is_done and remedy:
            oy += 36
            # Actionable Remedy Card
            rem_h = 48
            draw.rounded_rectangle([cx + 40, oy, cx + 24 + card_w - 16, oy + rem_h], radius=6, fill=(24, 25, 26), outline=GOOGLE_YELLOW, width=1)
            draw.text((cx + 50, oy + 6), "💡 Action Required: Docker is needed so agents run in safe, isolated sandboxes.", font=font_xs, fill=GOOGLE_YELLOW)
            
            # Inner Action Bar
            draw.rounded_rectangle([cx + 50, oy + 22, cx + 24 + card_w - 28, oy + rem_h - 4], radius=4, fill=(18, 19, 20), outline=BORDER_COLOR)
            draw.text((cx + 58, oy + 26), f"📋 {remedy}", font=font_xs, fill=GOOGLE_BLUE)
            
            # Action buttons
            draw.rounded_rectangle([cx + cw - 280, oy + 24, cx + cw - 215, oy + rem_h - 6], radius=4, fill=(40, 42, 44), outline=BORDER_COLOR)
            draw.text((cx + cw - 275, oy + 26), "📋 Copy", font=font_xs, fill=TEXT_WHITE)

            is_fixing = 80 <= frame_idx < 105
            fix_bg = (11, 87, 208) if is_fixing else M3_PRIMARY
            fix_text = "⚡ Fixing..." if is_fixing else "⚡ Fix Inline"
            draw.rounded_rectangle([cx + cw - 210, oy + 24, cx + cw - 145, oy + rem_h - 6], radius=4, fill=fix_bg)
            draw.text((cx + cw - 205, oy + 26), fix_text, font=font_xs, fill=(255, 255, 255) if is_fixing else (0, 48, 98))

            draw.rounded_rectangle([cx + cw - 140, oy + 24, cx + cw - 40, oy + rem_h - 6], radius=4, fill=(30, 40, 55), outline=GOOGLE_BLUE)
            draw.text((cx + cw - 135, oy + 26), "📖 Docs ↗", font=font_xs, fill=GOOGLE_BLUE)

            oy += rem_h + 8
        else:
            oy += 38

    if docker_is_fixed:
        draw.text((cx + 36, oy + 12), "✓ Inline remediation completed: All 6/6 diagnostics passed!", font=font_xs, fill=GOOGLE_GREEN)

    # Bottom buttons with dynamic bounding
    by = cy + ch - 48
    draw.line([cx + 24, by - 10, cx + cw - 24, by - 10], fill=BORDER_COLOR, width=1)
    
    rx = cx + cw - 24
    rx = draw_pill_button(draw, rx, by, "Proceed to Platform Setup [Enter] →", is_primary=True)
    rx = draw_pill_button(draw, rx, by, "Re-run Checks (r)", is_primary=False)
    draw_pill_button(draw, cx + 130, by, "← Back (b)", is_primary=False)

    return np.array(img)


def render_scene_4_auth(frame_idx=0):
    """Scene 4: Integration, Credentials & Google IAP OAuth screen."""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_CANVAS)
    draw = ImageDraw.Draw(img)

    tip = "Enter LLM API credentials or authenticate via Google IAP. Type /skip for local offline mode."
    vx, vy, vw, vh = draw_window_base(draw, title_step=3, tip_text=tip, legend_text="[Enter] Submit  [/skip] Bypass")

    cx, cy, cw, ch = vx + 40, vy + 10, vw - 80, vh - 20
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10, fill=(24, 25, 26), outline=BORDER_COLOR, width=1)

    # Headers with Snazzy Icon
    draw.text((cx + 24, cy + 20), "🤖 STEP 3: AGENT DEPLOYMENT & CREDENTIAL LINKAGE", font=font_md, fill=M3_PRIMARY)
    draw.text((cx + 24, cy + 46), "Link your workspace credentials (LLM API keys, Google IAP OAuth) for Actor runtime dispatch:", font=font_xs, fill=TEXT_MUTED)

    draw.text((cx + 24, cy + 90), "API Key / Token:", font=font_xs, fill=TEXT_MUTED)

    # Input Box
    masked = frame_idx < 40 or frame_idx > 80
    key_display = "sk-ant-••••••••••••••••••••••••••••" if masked else "sk-ant-api03-89f4a9b2c01e5d3-live"

    draw.rounded_rectangle([cx + 24, cy + 112, cx + cw - 150, cy + 150], radius=6, fill=(19, 19, 20), outline=BORDER_FOCUS, width=1)
    draw.text((cx + 36, cy + 122), key_display, font=font_sm, fill=TEXT_WHITE)

    # Toggle Mask Button
    mask_btn = "👁 Show" if masked else "🔒 Hide"
    draw_pill_button(draw, cx + cw - 24, cy + 112, mask_btn, is_primary=False)

    # Google IAP Card
    ix, iy, iw, ih = cx + 24, cy + 175, cw - 48, 85
    draw.rounded_rectangle([ix, iy, ix + iw, iy + ih], radius=8, fill=(19, 20, 22), outline=GOOGLE_BLUE, width=1)

    # Title badge
    badge_text = " 🌐 ENTERPRISE AUTHENTICATION (GOOGLE CLOUD IAP) "
    bw = int(len(badge_text) * 8)
    draw.rounded_rectangle([ix + 16, iy - 10, ix + 16 + bw, iy + 12], radius=4, fill=(8, 66, 160), outline=M3_PRIMARY, width=1)
    draw.text((ix + 20, iy - 6), badge_text, font=font_xs, fill=(255, 255, 255))

    draw.text((ix + 20, iy + 22), "Agent Substrate integrates with Google Identity-Aware Proxy (Port 8443)", font=font_sm, fill=(255, 255, 255))
    draw.text((ix + 20, iy + 48), "for zero-trust workforce single-sign-on and role-based actor access.", font=font_sm, fill=(211, 227, 253))

    if frame_idx >= 60:
        sp_char = SPINNER_FRAMES[(frame_idx // 3) % len(SPINNER_FRAMES)]
        if frame_idx < 100:
            draw.text((cx + 24, cy + 275), f"{sp_char} Waiting for authorization from Google Identity-Aware Proxy portal...", font=font_sm, fill=M3_PRIMARY)
        else:
            draw.text((cx + 24, cy + 275), "✓ Google IAP authorization received! ServiceAccount authenticated. [OK]", font=font_sm, fill=GOOGLE_GREEN)

    # Bottom Buttons with dynamic bounding
    by = cy + ch - 48
    draw.line([cx + 24, by - 10, cx + cw - 24, by - 10], fill=BORDER_COLOR, width=1)

    rx = cx + cw - 24
    rx = draw_pill_button(draw, rx, by, "Proceed to Launchpad [Enter] →", is_primary=True)
    rx = draw_pill_button(draw, rx, by, "🌐 Authenticate via Google IAP", is_primary=False, outline_color=M3_PRIMARY)
    draw_pill_button(draw, cx + 130, by, "← Back (b)", is_primary=False)

    return np.array(img)


def render_scene_5_launchpad(progress_pct=100.0, show_celebration=True, frame_idx=0):
    """Scene 5: Summary Card, Compilation Progress Bar & Celebration."""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_CANVAS)
    draw = ImageDraw.Draw(img)

    tip = "Onboarding successfully finished! Press [Enter] or click Launch."
    vx, vy, vw, vh = draw_window_base(draw, title_step=4, tip_text=tip, legend_text="[Enter] Launch Substrate  [/help] Help")

    cx, cy, cw, ch = vx + 40, vy + 10, vw - 80, vh - 20
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10, fill=(24, 25, 26), outline=BORDER_COLOR, width=1)

    # Headers with Snazzy Icon
    draw.text((cx + 24, cy + 20), "🛸 STEP 4: CLUSTER LAUNCHPAD & 3-PHASE OPERATIONS RUNBOOK", font=font_md, fill=M3_PRIMARY)
    draw.text((cx + 24, cy + 46), "Review your GKE Substrate profile before compiling manifests & starting worker pools:", font=font_xs, fill=TEXT_MUTED)

    # Summary Box
    sy = cy + 66
    draw.rounded_rectangle([cx + 24, sy, cx + cw - 24, sy + 115], radius=8, fill=(19, 19, 20), outline=M3_PRIMARY, width=1)

    summary_items = [
        ("Persona & Target:", "🛠️ Platform Engineer — Fleet WorkerPools"),
        ("WorkerPool Topology:", "⚡ MicroVM WorkerPool + Envoy Dataplane"),
        ("Optimization & Runtime:", "⚡ Local SSD Image Pre-caching"),
        ("Authentication Mode:", "Google IAP (Authenticated)"),
        ("GKE Cluster Target:", "gke-agent-cluster (us-central1-a)"),
        ("Pre-Flight Health:", "5/6 Diagnostics Passed (Healthy)"),
    ]

    for i, (k, v) in enumerate(summary_items):
        col = 0 if i < 3 else 1
        row = i % 3
        kx = cx + 44 + col * (cw // 2 - 20)
        ky = sy + 14 + row * 32
        draw.text((kx, ky), k, font=font_xs, fill=TEXT_MUTED)
        draw.text((kx + 160, ky), v, font=font_xs, fill=TEXT_WHITE if "Health" not in k else GOOGLE_GREEN)

    # Progress Bar or Celebration
    if not show_celebration:
        py = sy + 130
        draw.rounded_rectangle([cx + 24, py, cx + cw - 24, py + 10], radius=5, fill=(40, 41, 42), outline=BORDER_COLOR)

        fill_w = int((cw - 48) * (progress_pct / 100.0))
        if fill_w > 0:
            draw.rounded_rectangle([cx + 24, py, cx + 24 + fill_w, py + 10], radius=5, fill=M3_PRIMARY)

        # Progress text
        if progress_pct < 30:
            pmsg = "Generating substrate.yaml & WorkerPool CRD manifests..."
        elif progress_pct < 60:
            pmsg = "Configuring Envoy dataplane, Valkey cache & GCS snapshot bucket..."
        elif progress_pct < 90:
            pmsg = "Testing data plane: Cold Boot (912ms) → Suspend (42ms) → Warm Resume (120ms)..."
        else:
            pmsg = "Workspace configured successfully! Worker pool ready for dispatch."

        draw.text((cx + (cw - len(pmsg) * 7.5) // 2, py + 18), f"⚙ {pmsg}", font=font_xs, fill=GOOGLE_BLUE)
    else:
        # Celebration Banner directly under summary box
        cely = sy + 125
        draw.rounded_rectangle([cx + 24, cely, cx + cw - 24, cely + 115], radius=8, fill=(20, 35, 26), outline=GOOGLE_GREEN, width=1)
        draw.text((cx + 40, cely + 10), "🎉 SUBSTRATE CONFIGURED — READY FOR PLATFORM & AI WORKLOADS!", font=font_sm, fill=GOOGLE_GREEN)
        draw.text((cx + 40, cely + 34), "🚀 Phase 1: curl -sSL ate.dev/install.sh | bash && atectl create workerpools my-pool --isolation=microvm", font=font_xs, fill=M3_PRIMARY)
        draw.text((cx + 40, cely + 56), "🤖 Phase 2: atectl create template my-agent --image gcr.io/repo/my-agent:v1 --worker-pool=workload=agent", font=font_xs, fill=GOOGLE_BLUE)
        draw.text((cx + 40, cely + 78), "📊 Phase 3: atectl top workers  |  atectl precache image gcr.io/rl-lab/env:v3.0 --workerpool=rl-pool", font=font_xs, fill=TEXT_PRIMARY)
        draw.text((cx + 40, cely + 96), "• Substrate Data Plane dynamically injects waking actors into ready worker pools in real-time.", font=font_xs, fill=TEXT_MUTED)

    # Bottom buttons with dynamic bounding
    by = cy + ch - 48
    draw.line([cx + 24, by - 10, cx + cw - 24, by - 10], fill=BORDER_COLOR, width=1)
    
    rx = cx + cw - 24
    rx = draw_pill_button(draw, rx, by, "Launch Agent Substrate 🚀", is_primary=True)
    draw_pill_button(draw, cx + 180, by, "← Modify Settings", is_primary=False)

    return np.array(img)


def render_scene_6_help_modal(frame_idx=0):
    """Scene 6: Interactive Help Overlay Modal with Slash Commands."""
    base_frame = render_scene_2_wizard(substep=0, selected_idx=0, frame_idx=0)
    img = Image.fromarray(base_frame)
    draw = ImageDraw.Draw(img)

    # Dark overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 180))
    img.paste(Image.alpha_composite(Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)), overlay), (0, 0))

    # Dialog Box
    dx, dy, dw, dh = WIDTH // 2 - 320, HEIGHT // 2 - 200, 640, 400
    draw.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=14, fill=(30, 31, 32), outline=M3_PRIMARY, width=2)

    draw.text((dx + (dw - 380) // 2, dy + 20), "⚡ KEYBOARD SHORTCUTS & SLASH COMMANDS", font=font_sm, fill=M3_PRIMARY)

    draw.text((dx + 30, dy + 55), "Global Slash Commands:", font=font_xs, fill=M3_PRIMARY)

    cmds = [
        ("/help", "/?, /h, F1", "Show this interactive command overlay"),
        ("/skip", "/s, /next", "Skip current question using recommended defaults"),
        ("/back", "/prev, /b", "Return to previous onboarding screen"),
        ("/doctor", "/check", "Run or inspect environment pre-flight diagnostics"),
        ("/exit", "/quit, /q", "Pause onboarding and exit cleanly"),
    ]

    cy = dy + 78
    for cmd, alias, desc in cmds:
        draw.text((dx + 40, cy), cmd, font=font_xs, fill=M3_PRIMARY)
        draw.text((dx + 110, cy), alias, font=font_xs, fill=TEXT_MUTED)
        draw.text((dx + 230, cy), desc, font=font_xs, fill=TEXT_PRIMARY)
        draw.line([dx + 30, cy + 18, dx + dw - 30, cy + 18], fill=(45, 47, 49), width=1)
        cy += 26

    draw.text((dx + 30, cy + 15), "Keyboard Shortcuts:", font=font_xs, fill=M3_PRIMARY)
    keys = [
        ("[Up / Down]", "Navigate items, options, and lists"),
        ("[Enter]", "Confirm selection / Submit input / Proceed"),
        ("[Space]", "Toggle selection or buttons"),
        ("[Ctrl+C / Ctrl+D]", "Pause onboarding & prompt exit confirmation"),
        ("[Esc]", "Close modal dialogs"),
    ]
    cy += 38
    for k, desc in keys:
        draw.text((dx + 40, cy), k, font=font_xs, fill=GOOGLE_BLUE)
        draw.text((dx + 230, cy), desc, font=font_xs, fill=TEXT_PRIMARY)
        cy += 24

    draw_pill_button(draw, dx + dw - 24, dy + dh - 40, "Close (Esc)", is_primary=False)

    return np.array(img)


def generate_full_video(output_path: str):
    """Generate high-definition MP4 recording of the full onboarding journey with Option A PRFAQ sequencing."""
    print(f"🎬 Generating video recording: {output_path}")
    writer = imageio.get_writer(output_path, fps=FPS, codec="libx264", quality=8)

    # 1. Welcome Scene (0.0s - 4.0s = 120 frames)
    print("  • Rendering Scene 1: Welcome Splash & Typewriter...")
    scene1_frames = 120
    for i in range(scene1_frames):
        frame = render_scene_1_welcome(i, scene1_frames)
        writer.append_data(frame)

    # 2. Step 1: Pre-Flight Environment Doctor (4.0s - 9.0s = 150 frames)
    print("  • Rendering Scene 2: Step 1 Pre-Flight Environment Doctor...")
    for i in range(150):
        frame = render_scene_3_doctor(frame_idx=i)
        writer.append_data(frame)

    # 3. Step 2: Platform Setup Wizard Substeps 1, 2, 3 (9.0s - 16.0s = 210 frames)
    print("  • Rendering Scene 3: Step 2 Platform Setup & WorkerPool Topology...")
    # Substep 0: Navigate options (Platform Engineer -> AI Engineer -> Platform Engineer)
    for i in range(25):
        frame = render_scene_2_wizard(substep=0, selected_idx=0, frame_idx=i)
        writer.append_data(frame)
    for i in range(25):
        frame = render_scene_2_wizard(substep=0, selected_idx=1, frame_idx=i)
        writer.append_data(frame)
    for i in range(20):
        frame = render_scene_2_wizard(substep=0, selected_idx=0, frame_idx=i)
        writer.append_data(frame)

    # Substep 1: Navigate Dataplane options
    for i in range(35):
        frame = render_scene_2_wizard(substep=1, selected_idx=0, frame_idx=i)
        writer.append_data(frame)
    for i in range(35):
        frame = render_scene_2_wizard(substep=1, selected_idx=0, frame_idx=i)
        writer.append_data(frame)

    # Substep 2: Select Local SSD Caching
    for i in range(70):
        frame = render_scene_2_wizard(substep=2, selected_idx=0, frame_idx=i)
        writer.append_data(frame)

    # 4. Step 3: Agent Deployment & Credentials (16.0s - 21.0s = 150 frames)
    print("  • Rendering Scene 4: Step 3 Agent Deployment & Credentials...")
    for i in range(150):
        frame = render_scene_4_auth(frame_idx=i)
        writer.append_data(frame)

    # 5. Step 4: Cluster Launchpad & Compilation Progress (21.0s - 27.0s = 180 frames)
    print("  • Rendering Scene 5: Step 4 Compilation Progress & Launchpad...")
    for i in range(180):
        progress = min(100.0, (i / 130.0) * 100.0)
        show_cel = i >= 130
        frame = render_scene_5_launchpad(progress_pct=progress, show_celebration=show_cel, frame_idx=i)
        writer.append_data(frame)

    # 6. Help Overlay Modal (27.0s - 31.0s = 120 frames)
    print("  • Rendering Scene 6: Slash Commands & Help Modal...")
    for i in range(120):
        frame = render_scene_6_help_modal(frame_idx=i)
        writer.append_data(frame)

    # 7. Final Launchpad Hold (31.0s - 34.0s = 90 frames)
    for i in range(90):
        frame = render_scene_5_launchpad(progress_pct=100.0, show_celebration=True, frame_idx=i)
        writer.append_data(frame)

    writer.close()
    print(f"✅ Video recording completed successfully: {output_path}")


if __name__ == "__main__":
    out = os.path.abspath("demos/onboarding-tui/onboarding_demo.mp4")
    generate_full_video(out)
