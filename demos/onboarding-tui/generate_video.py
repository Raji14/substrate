"""High-Definition (720p/1080p) Video Recording Generator for Agent Substrate Day-0 Onboarding.

Renders each scene, animation frame, keyboard interaction, CCC remedy, and modal dialog
into a video file (onboarding_demo.mp4) with Google Material 3 tokens, rich icons,
and pixel-perfect 2-column Left Sidebar Navigation layout.
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

SPINNER_FRAMES = ["-", "\\", "|", "/"]

NAV_STEPS = [
    "1. Cluster Detection",
    "2. Control Plane",
    "3. Node Pool & CCC",
    "4. Autoscaling (HPA)",
    "5. Deploy WorkerPool",
    "6. Launchpad & Verify",
]


def draw_window_frame(active_step_idx=0, tip_text=""):
    """Draws outer container, terminal window, top bar, left sidebar, and bottom bar."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (17, 18, 19))
    draw = ImageDraw.Draw(img)

    # Window bounds
    wx, wy, ww, wh = 80, 40, 1120, 640
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=12, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)

    # Titlebar
    draw.rectangle([wx, wy, wx + ww, wy + 36], fill=(24, 25, 26))
    draw.line([wx, wy + 36, wx + ww, wy + 36], fill=(40, 41, 42), width=1)

    # Traffic lights
    draw.ellipse([wx + 16, wy + 12, wx + 28, wy + 24], fill=(255, 95, 86))
    draw.ellipse([wx + 34, wy + 12, wx + 46, wy + 24], fill=(255, 189, 46))
    draw.ellipse([wx + 52, wy + 12, wx + 64, wy + 24], fill=(39, 201, 63))
    draw.text((wx + 360, wy + 10), "broyal@broyal: ~/workspaces/ate-demos/demos — atectl onboard", fill=TEXT_MUTED, font=font_sm)

    # Top Brand Bar
    draw.rectangle([wx, wy + 37, wx + ww, wy + 76], fill=SURFACE_PANEL)
    draw.line([wx, wy + 76, wx + ww, wy + 76], fill=BORDER_COLOR, width=1)
    draw.text((wx + 20, wy + 48), "Google Cloud ", fill=GOOGLE_BLUE, font=font_base)
    draw.text((wx + 140, wy + 48), "│ Agent Substrate on GKE", fill=TEXT_WHITE, font=font_base)

    # Right side badge
    cluster_str = "[ Cluster: demo-cluster ]"
    draw.text((wx + ww - 310, wy + 50), cluster_str, fill=GOOGLE_BLUE, font=font_sm)
    draw.rounded_rectangle([wx + ww - 100, wy + 46, wx + ww - 20, wy + 68], radius=6, fill=CARD_ACTIVE, outline=M3_PRIMARY, width=1)
    draw.text((wx + ww - 90, wy + 50), "? Help", fill=M3_PRIMARY, font=font_xs)

    # Bottom Status Bar
    draw.rectangle([wx, wy + wh - 38, wx + ww, wy + wh], fill=SURFACE_PANEL)
    draw.line([wx, wy + wh - 38, wx + ww, wy + wh - 38], fill=BORDER_COLOR, width=1)
    draw.text((wx + 20, wy + wh - 26), f"[!] {tip_text}", fill=(211, 227, 253), font=font_sm)
    draw.text((wx + ww - 300, wy + wh - 26), "[Enter] Confirm  [b] Back  [F1] Help", fill=TEXT_MUTED, font=font_sm)

    # Left Sidebar Navigation (width 260)
    sw = 260
    draw.rectangle([wx, wy + 77, wx + sw, wy + wh - 39], fill=SURFACE_PANEL)
    draw.line([wx + sw, wy + 77, wx + sw, wy + wh - 39], fill=BORDER_COLOR, width=1)

    draw.text((wx + 16, wy + 94), "ONBOARDING WIZARD", fill=GOOGLE_BLUE, font=font_sm)

    # Render Nav Steps
    sy = wy + 124
    for i, step_name in enumerate(NAV_STEPS):
        if i < active_step_idx:
            icon = "✓"
            icon_col = GOOGLE_GREEN
            txt_col = GOOGLE_GREEN
            bg_col = None
        elif i == active_step_idx:
            icon = "▶"
            icon_col = M3_PRIMARY
            txt_col = TEXT_WHITE
            bg_col = CARD_ACTIVE
        else:
            icon = "○"
            icon_col = TEXT_MUTED
            txt_col = TEXT_MUTED
            bg_col = None

        if bg_col:
            draw.rounded_rectangle([wx + 12, sy - 4, wx + sw - 12, sy + 24], radius=6, fill=bg_col, outline=M3_PRIMARY, width=1)

        draw.text((wx + 20, sy), icon, fill=icon_col, font=font_sm)
        draw.text((wx + 40, sy), step_name, fill=txt_col, font=font_sm)
        sy += 36

    # Lower Sidebar Metadata Panel
    my = wy + wh - 170
    draw.rounded_rectangle([wx + 12, my, wx + sw - 12, my + 120], radius=8, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((wx + 20, my + 8), "CLUSTER CONTEXT", fill=GOOGLE_BLUE, font=font_xs)

    meta_items = [
        ("Cluster", "demo-cluster", GOOGLE_BLUE),
        ("Region", "us-central1-a", TEXT_WHITE),
        ("GKE K8s", "v1.31.1-gke", TEXT_WHITE),
        ("Namespace", "substrate-sys", TEXT_WHITE),
        ("Status", "Connected", GOOGLE_GREEN),
    ]
    my_row = my + 28
    for label, val, val_col in meta_items:
        draw.text((wx + 20, my_row), f"{label}:", fill=TEXT_MUTED, font=font_xs)
        draw.text((wx + 110, my_row), val, fill=val_col, font=font_xs)
        my_row += 18

    # Content Area coordinates
    cx = wx + sw + 24
    cy = wy + 94
    cw = ww - sw - 48

    return img, draw, cx, cy, cw


def draw_pill_button(draw, right_x, y, text, is_primary=True, custom_font=font_sm):
    bbox = custom_font.getbbox(text)
    w = (bbox[2] - bbox[0]) + 32
    h = (bbox[3] - bbox[1]) + 20
    x = right_x - w
    bg = CARD_ACTIVE if is_primary else CARD_BG
    out = M3_PRIMARY if is_primary else BORDER_COLOR
    draw.rounded_rectangle([x, y, right_x, y + h], radius=8, fill=bg, outline=out, width=1)
    draw.text((x + 16, y + 8), text, fill=TEXT_WHITE, font=custom_font)
    return x


# Scene 1: Step 1 Cluster Detection
def render_scene_step1(frame_idx=0):
    img, draw, cx, cy, cw = draw_window_frame(0, "Select target GKE cluster. Press [Enter] to install Substrate Control Plane.")
    
    draw.text((cx, cy), "[1/6] CLUSTER DETECTION & ENVIRONMENT SCAN", fill=M3_PRIMARY, font=font_md)
    draw.text((cx, cy + 24), "Scanning active kubeconfig for Google Kubernetes Engine (GKE) clusters...", fill=TEXT_MUTED, font=font_sm)

    # 3 Cluster Options
    clusters = [
        ("gke_demo_project_us-central1-a_demo-cluster (Recommended)", "GKE v1.31.1-gke.1520000 in us-central1-a (Target: demo-cluster)", True),
        ("gke_demo_project_us-west1-b_staging-cluster", "GKE v1.31.0 in us-west1-b (Target: staging-cluster)", False),
        ("gke_demo_project_europe-west1-c_analytics-cluster", "GKE v1.30.4 in europe-west1-c (Target: analytics-cluster)", False),
    ]
    oy = cy + 54
    for title, desc, is_act in clusters:
        bg = CARD_ACTIVE if is_act else CARD_BG
        out = M3_PRIMARY if is_act else BORDER_COLOR
        draw.rounded_rectangle([cx, oy, cx + cw, oy + 52], radius=10, fill=bg, outline=out, width=1)
        draw.text((cx + 16, oy + 12), "▶" if is_act else "○", fill=TEXT_WHITE if is_act else GOOGLE_BLUE, font=font_sm)
        draw.text((cx + 36, oy + 10), title, fill=TEXT_WHITE, font=font_sm)
        draw.text((cx + 36, oy + 30), desc, fill=(211, 227, 253) if is_act else TEXT_MUTED, font=font_xs)
        oy += 60

    # Diagnostic Box
    dy = oy + 6
    draw.rounded_rectangle([cx, dy, cx + cw, dy + 90], radius=10, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((cx + 16, dy + 12), "✓ Selected target cluster: demo-cluster", fill=GOOGLE_GREEN, font=font_sm)
    draw.text((cx + 16, dy + 36), "✓ Verified cluster type: Google Kubernetes Engine (v1.31.1-gke)", fill=GOOGLE_GREEN, font=font_sm)
    draw.text((cx + 16, dy + 60), "✓ Substrate Control Plane: No existing instance detected (Ready for clean install)", fill=GOOGLE_YELLOW, font=font_sm)

    # Action Button
    draw_pill_button(draw, cx + cw, dy + 110, "Install Substrate on [demo-cluster] (Enter) →", True)
    return img


# Scene 2: Step 2 Control Plane Installation
def render_scene_step2(progress_items=5):
    img, draw, cx, cy, cw = draw_window_frame(1, "Control plane components installing in namespace [substrate-system]...")
    
    draw.text((cx, cy), "[2/6] CONTROL PLANE INSTALLATION", fill=M3_PRIMARY, font=font_md)
    draw.text((cx, cy + 24), "Installing Agent Substrate Control Plane on cluster [demo-cluster] in namespace [substrate-system]...", fill=TEXT_MUTED, font=font_sm)

    items = [
        "Applying Substrate CustomResourceDefinitions (ate.dev/v1alpha1: WorkerPool, ActorTemplate, Actor)",
        "Deploying Valkey Metadata & State Registry",
        "Bootstrapping Substrate Gateway & API Server (listening on :8080)",
        "Initializing eBPF Network & Ingress/Egress Proxy Controller",
        "All control plane components successfully deployed in namespace [substrate-system].",
    ]
    dy = cy + 60
    draw.rounded_rectangle([cx, dy, cx + cw, dy + 210], radius=10, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)

    iy = dy + 16
    for i, desc in enumerate(items):
        if i < progress_items:
            draw.text((cx + 16, iy), "✓", fill=GOOGLE_GREEN, font=font_sm)
            draw.text((cx + 36, iy), desc, fill=GOOGLE_GREEN if i == 4 else TEXT_WHITE, font=font_sm)
        elif i == progress_items:
            sp = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
            draw.text((cx + 16, iy), sp, fill=GOOGLE_BLUE, font=font_sm)
            draw.text((cx + 36, iy), desc, fill=GOOGLE_BLUE, font=font_sm)
        else:
            draw.text((cx + 16, iy), "○", fill=TEXT_MUTED, font=font_sm)
            draw.text((cx + 36, iy), desc, fill=TEXT_MUTED, font=font_sm)
        iy += 36

    bx = draw_pill_button(draw, cx + cw, dy + 230, "Proceed to WorkerPool Setup (Enter) →", True)
    draw_pill_button(draw, bx - 16, dy + 230, "← Back (b)", False)
    return img


# Scene 3: Step 3 Node Pool & CCC Hardware Isolation
def render_scene_step3(fixed=False):
    img, draw, cx, cy, cw = draw_window_frame(2, "Select Node Pool configuration. CCC auto-provisions nested-virt N2 Spot instances.")
    
    draw.text((cx, cy), "[3/6] NODE POOL & HARDWARE NESTED VIRTUALIZATION", fill=M3_PRIMARY, font=font_md)
    draw.text((cx, cy + 24), "A Substrate WorkerPool requires a compatible GKE Node Pool with hardware nested virtualization.", fill=TEXT_MUTED, font=font_sm)

    # Diagnostic Box
    dy = cy + 54
    draw.rounded_rectangle([cx, dy, cx + cw, dy + 56], radius=10, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((cx + 16, dy + 10), "Scanning cluster [demo-cluster] node pools...", fill=TEXT_MUTED, font=font_xs)
    if not fixed:
        draw.text((cx + 16, dy + 30), "! No node pool detected with hardware nested virtualization enabled.", fill=GOOGLE_YELLOW, font=font_sm)
    else:
        draw.text((cx + 16, dy + 30), "✓ Node pool configured with nested virtualization enabled!", fill=GOOGLE_GREEN, font=font_sm)

    # Action Required Box
    ry = dy + 66
    draw.rounded_rectangle([cx, ry, cx + cw, ry + 78], radius=10, fill=(35, 30, 20), outline=GOOGLE_YELLOW, width=1)
    draw.text((cx + 16, ry + 10), "[!] Action Required: Create compatible Node Pool using Custom Compute Class (CCC)", fill=GOOGLE_YELLOW, font=font_sm)
    draw.text((cx + 16, ry + 32), "atectl create ccc agent-spot-ccc --machine-type=n2-standard-48 --nested-virt", fill=GOOGLE_BLUE, font=font_xs)
    draw.rounded_rectangle([cx + cw - 120, ry + 46, cx + cw - 16, ry + 70], radius=6, fill=CARD_BG, outline=GOOGLE_GREEN if fixed else BORDER_COLOR, width=1)
    draw.text((cx + cw - 110, ry + 50), "✓ Fixed" if fixed else "[Fix Inline]", fill=GOOGLE_GREEN if fixed else TEXT_WHITE, font=font_xs)

    # Options
    oy = ry + 88
    opts = [
        ("Automatically create a compatible Node Pool using Custom Compute Class (Recommended)", "Applies manifest (agent-spot-ccc) with n2-standard-48, Spot fallback, and nested-virt", True),
        ("Create a compatible Node Pool manually via gcloud", "Run 'gcloud container node-pools create --enable-nested-virtualization' in terminal", False),
    ]
    for title, desc, is_act in opts:
        bg = CARD_ACTIVE if is_act else CARD_BG
        out = M3_PRIMARY if is_act else BORDER_COLOR
        draw.rounded_rectangle([cx, oy, cx + cw, oy + 50], radius=10, fill=bg, outline=out, width=1)
        draw.text((cx + 16, oy + 10), "▶" if is_act else "○", fill=TEXT_WHITE if is_act else GOOGLE_BLUE, font=font_sm)
        draw.text((cx + 36, oy + 8), title, fill=TEXT_WHITE, font=font_sm)
        draw.text((cx + 36, oy + 28), desc, fill=(211, 227, 253) if is_act else TEXT_MUTED, font=font_xs)
        oy += 58

    bx = draw_pill_button(draw, cx + cw, oy + 10, "Apply CCC & Proceed (Enter) →", True)
    draw_pill_button(draw, bx - 16, oy + 10, "← Back (b)", False)
    return img


# Scene 4: Step 4 Autoscaling & CapacityBuffer
def render_scene_step4():
    img, draw, cx, cy, cw = draw_window_frame(3, "OneHPA scales 10-100 pods with 3 standby warm replicas ready.")
    
    draw.text((cx, cy), "[4/6] WORKERPOOL AUTOSCALING & CAPACITY BUFFERS", fill=M3_PRIMARY, font=font_md)
    draw.text((cx, cy + 24), "Substrate uses Kubernetes HPA along with an upstream CapacityBuffer for instant (<100ms) injection.", fill=TEXT_MUTED, font=font_sm)

    opts = [
        ("Automatically configure HPA & CapacityBuffer with sensible defaults (Recommended)", "Applies OneHPA (min=10, max=100) and fixed-replica-buffer (3 standby replicas)", True),
        ("Configure Autoscaling manually via kubectl", "Apply custom HorizontalPodAutoscaler and CapacityBuffer manifests later", False),
    ]
    oy = cy + 54
    for title, desc, is_act in opts:
        bg = CARD_ACTIVE if is_act else CARD_BG
        out = M3_PRIMARY if is_act else BORDER_COLOR
        draw.rounded_rectangle([cx, oy, cx + cw, oy + 50], radius=10, fill=bg, outline=out, width=1)
        draw.text((cx + 16, oy + 10), "▶" if is_act else "○", fill=TEXT_WHITE if is_act else GOOGLE_BLUE, font=font_sm)
        draw.text((cx + 36, oy + 8), title, fill=TEXT_WHITE, font=font_sm)
        draw.text((cx + 36, oy + 28), desc, fill=(211, 227, 253) if is_act else TEXT_MUTED, font=font_xs)
        oy += 58

    dy = oy + 6
    draw.rounded_rectangle([cx, dy, cx + cw, dy + 90], radius=10, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((cx + 16, dy + 12), "✓ Applying HorizontalPodAutoscaler (OneHPA: minReplicas=10, maxReplicas=100)", fill=GOOGLE_GREEN, font=font_sm)
    draw.text((cx + 16, dy + 36), "✓ Applying CapacityBuffer (fixed-replica-buffer: 3 standby replicas via buffer.gke.io)", fill=GOOGLE_GREEN, font=font_sm)
    draw.text((cx + 16, dy + 60), "✓ Standby buffer ready for instant (<100ms) agent session injection", fill=GOOGLE_GREEN, font=font_sm)

    bx = draw_pill_button(draw, cx + cw, dy + 110, "Configure Autoscaling & Proceed (Enter) →", True)
    draw_pill_button(draw, bx - 16, dy + 110, "← Back (b)", False)
    return img


# Scene 5: Step 5 Deploy WorkerPool
def render_scene_step5():
    img, draw, cx, cy, cw = draw_window_frame(4, "Deploying default WorkerPool with 10 standby MicroVM workers.")
    
    draw.text((cx, cy), "[5/6] DEPLOY DEFAULT WORKERPOOL (EXECUTION LAYER)", fill=M3_PRIMARY, font=font_md)
    draw.text((cx, cy + 24), "Proceed with deploying the default Substrate WorkerPool [default-worker-pool]?", fill=TEXT_MUTED, font=font_sm)

    opts = [
        ("Yes, deploy default WorkerPool [default-worker-pool] (Recommended)", "10 standby replicas, microVM sandbox isolation, 10% warm headroom", True),
        ("No, skip default WorkerPool deployment", "Only install control plane; create worker pools later via atectl CLI", False),
    ]
    oy = cy + 54
    for title, desc, is_act in opts:
        bg = CARD_ACTIVE if is_act else CARD_BG
        out = M3_PRIMARY if is_act else BORDER_COLOR
        draw.rounded_rectangle([cx, oy, cx + cw, oy + 50], radius=10, fill=bg, outline=out, width=1)
        draw.text((cx + 16, oy + 10), "▶" if is_act else "○", fill=TEXT_WHITE if is_act else GOOGLE_BLUE, font=font_sm)
        draw.text((cx + 36, oy + 8), title, fill=TEXT_WHITE, font=font_sm)
        draw.text((cx + 36, oy + 28), desc, fill=(211, 227, 253) if is_act else TEXT_MUTED, font=font_xs)
        oy += 58

    dy = oy + 6
    draw.rounded_rectangle([cx, dy, cx + cw, dy + 90], radius=10, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((cx + 16, dy + 12), "✓ WorkerPool CRD applied (10 replicas, OneHPA autoscaler enabled)", fill=GOOGLE_GREEN, font=font_sm)
    draw.text((cx + 16, dy + 36), "✓ CapacityBuffer configured with 10% warm standby headroom", fill=GOOGLE_GREEN, font=font_sm)
    draw.text((cx + 16, dy + 60), "* Data Plane Benchmark: Cold Start (890ms) -> Suspend (38ms) -> Resume (115ms)", fill=GOOGLE_YELLOW, font=font_sm)

    bx = draw_pill_button(draw, cx + cw, dy + 110, "Deploy WorkerPool & Launch (Enter) →", True)
    draw_pill_button(draw, bx - 16, dy + 110, "← Back (b)", False)
    return img


# Scene 6: Step 6 Launchpad & Verification
def render_scene_step6():
    img, draw, cx, cy, cw = draw_window_frame(5, "Agent Substrate installed successfully! Press [Enter] to exit to shell.")
    
    draw.text((cx, cy), "[6/6] LAUNCHPAD & LIVE CLUSTER VERIFICATION", fill=M3_PRIMARY, font=font_md)
    draw.text((cx, cy + 24), "✓ Agent Substrate on GKE Installation Complete! Cluster [demo-cluster] is ready.", fill=GOOGLE_GREEN, font=font_sm)

    # Verification Table
    dy = cy + 54
    draw.rounded_rectangle([cx, dy, cx + cw, dy + 90], radius=10, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((cx + 16, dy + 10), "$ atectl get workerpools", fill=GOOGLE_BLUE, font=font_xs)
    
    headers = "WORKERPOOL           NAMESPACE         ISOLATION  READY  STANDBY  CPU  MEM  QUEUE"
    vals    = "default-worker-pool  substrate-system  microvm    10/10  10       4%   8%   0"
    draw.text((cx + 16, dy + 32), headers, fill=M3_PRIMARY, font=font_xs)
    draw.text((cx + 16, dy + 56), vals, fill=GOOGLE_GREEN, font=font_xs)

    # Runbook Box
    ry = dy + 100
    draw.rounded_rectangle([cx, ry, cx + cw, ry + 120], radius=10, fill=(20, 35, 25), outline=GOOGLE_GREEN, width=1)
    draw.text((cx + 16, ry + 10), "DAY-0 QUICKSTART RUNBOOK (NEXT STEPS):", fill=GOOGLE_GREEN, font=font_sm)
    draw.text((cx + 16, ry + 32), "1. Deploy your first agent session (No-YAML):", fill=TEXT_WHITE, font=font_xs)
    draw.text((cx + 16, ry + 48), "   $ atectl actor create my-first-actor --template=default-agent", fill=GOOGLE_BLUE, font=font_xs)
    draw.text((cx + 16, ry + 68), "2. Inspect standby workers and memory overcommit:", fill=TEXT_WHITE, font=font_xs)
    draw.text((cx + 16, ry + 84), "   $ atectl top workers", fill=GOOGLE_BLUE, font=font_xs)

    bx = draw_pill_button(draw, cx + cw, ry + 135, "Finish & Launch CLI (Enter)", True)
    draw_pill_button(draw, bx - 16, ry + 135, "← Back (b)", False)
    return img


# Scene 7: Global Help Modal
def render_scene_help():
    img = render_scene_step3()
    # Dim overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 160))
    img.paste(Image.alpha_composite(Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)), overlay).convert("RGB"), (0, 0), overlay)
    draw = ImageDraw.Draw(img)

    # Modal Box
    mx, my, mw, mh = 360, 160, 560, 400
    draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=12, fill=SURFACE_PANEL, outline=M3_PRIMARY, width=2)

    draw.text((mx + 24, my + 24), "AGENT SUBSTRATE WIZARD HELP & SHORTCUTS", fill=M3_PRIMARY, font=font_md)

    shortcuts = [
        ("Enter / Space", "Confirm selection and proceed to next step"),
        ("↑ / ↓ (or k / j)", "Navigate options and cluster choices"),
        ("b", "Return to previous step"),
        ("/skip", "Skip current step with recommended defaults"),
        ("/doctor", "Jump straight to pre-flight diagnostic scan"),
        ("F1 / /help", "Toggle this command overlay"),
    ]

    sy = my + 64
    for key, desc in shortcuts:
        draw.text((mx + 24, sy), key, fill=GOOGLE_BLUE, font=font_sm)
        draw.text((mx + 180, sy), desc, fill=TEXT_WHITE, font=font_sm)
        draw.line([mx + 24, sy + 24, mx + mw - 24, sy + 24], fill=(50, 52, 55), width=1)
        sy += 38

    draw_pill_button(draw, mx + mw - 24, my + mh - 50, "Close Help (Esc)", True)
    return img


def generate_demo_video(output_path="demos/onboarding-tui/onboarding_demo.mp4"):
    print(f"🎬 Generating HD Demo Video: {output_path}...")
    writer = imageio.get_writer(output_path, fps=FPS, codec="libx264", quality=8)

    # Sequence of scenes with durations
    scenes = [
        (render_scene_step1, 2.5),
        (lambda: render_scene_step2(2), 0.8),
        (lambda: render_scene_step2(4), 0.8),
        (lambda: render_scene_step2(5), 1.8),
        (lambda: render_scene_step3(False), 1.8),
        (lambda: render_scene_step3(True), 2.0),
        (render_scene_step4, 2.2),
        (render_scene_step5, 2.2),
        (render_scene_step6, 3.0),
        (render_scene_help, 2.0),
    ]

    for scene_func, duration in scenes:
        num_frames = int(duration * FPS)
        for _ in range(num_frames):
            frame_img = scene_func()
            frame_np = np.array(frame_img)
            writer.append_data(frame_np)

    writer.close()
    print(f"✅ Video generated successfully: {output_path}")


def export_step_screenshots(out_dir="demos/onboarding-tui/screenshots"):
    os.makedirs(out_dir, exist_ok=True)
    print(f"📸 Exporting high-res screenshots to {out_dir}...")
    
    shots = [
        ("step1_cluster_detection.png", render_scene_step1()),
        ("step2_control_plane.png", render_scene_step2(5)),
        ("step3_nodepool_ccc.png", render_scene_step3(True)),
        ("step4_autoscaling.png", render_scene_step4()),
        ("step5_deploy_workerpool.png", render_scene_step5()),
        ("step6_launchpad_verify.png", render_scene_step6()),
        ("step7_help_modal.png", render_scene_help()),
        # Backward compatibility copies for guide
        ("step0_welcome.png", render_scene_step1()),
        ("step1_preflight_doctor.png", render_scene_step2(5)),
        ("step2_platform_setup.png", render_scene_step3(True)),
        ("step3_agent_deployment.png", render_scene_step4()),
        ("step4_cluster_launchpad.png", render_scene_step6()),
        ("step5_help_modal.png", render_scene_help()),
    ]

    for fname, img in shots:
        path = os.path.join(out_dir, fname)
        img.save(path)
        print(f"  ✓ Saved {fname}")


if __name__ == "__main__":
    export_step_screenshots()
    generate_demo_video()
