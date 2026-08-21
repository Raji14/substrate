"""High-Definition (720p/1080p) Video Recording Generator for Agent Substrate Onboarding.

Features:
- "Agent Substrate" Google 4-color gradient splash title
- Step 2: Side-by-side cluster selection with Region details & Conditional GKE Private GA agreement
- Step 4: Compatible Node Pool (Scan -> CCC/Manual options -> Progress)
- Step 5: WorkerPool Autoscaling (HPA & CapacityBuffer)
- Step 6: Confirm & Deploy Substrate WorkerPool (Yes vs. No, skip)
- Step 7: Installation Complete (Celebratory hero banner + next steps runnable code)
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

# Colors
BG_CANVAS = (9, 13, 22)           # #090d16
BG_CONTENT = (13, 17, 23)         # #0d1117
BG_CARD = (22, 27, 34)            # #161b22
BG_CMD = (17, 21, 28)             # #11151c
BORDER_DARK = (33, 38, 45)        # #21262d
BORDER_SUBTLE = (48, 54, 61)      # #30363d

ACCENT_CYAN = (112, 214, 255)     # #70d6ff
ACCENT_BLUE = (21, 101, 192)      # #1565c0
ACCENT_GREEN = (129, 201, 149)    # #81c995
ACCENT_YELLOW = (253, 214, 99)    # #fdd663
ACCENT_RED = (242, 139, 130)      # #f28b82

GOOGLE_BLUE = (138, 180, 248)     # #8ab4f8
GOOGLE_RED = (242, 139, 130)      # #f28b82
GOOGLE_YELLOW = (253, 214, 99)    # #fdd663
GOOGLE_GREEN = (129, 201, 149)    # #81c995

TEXT_WHITE = (255, 255, 255)
TEXT_PRIMARY = (227, 227, 227)    # #e3e3e3
TEXT_MUTED = (128, 134, 139)      # #80868b
TEXT_DIM = (95, 99, 104)          # #5f6368

# Font loading
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/SFNSMono.ttf"

font_mono = ImageFont.truetype(FONT_PATH, 9)
font_xs = ImageFont.truetype(FONT_PATH, 11)
font_sm = ImageFont.truetype(FONT_PATH, 13)
font_base = ImageFont.truetype(FONT_PATH, 15)
font_md = ImageFont.truetype(FONT_PATH, 17)
font_lg = ImageFont.truetype(FONT_PATH, 20)

LOGO_LINES = [
    r"    _    ____ _____ _   _ _____        ____  _   _ ____  ____ _____ ____     _  _____ _____ ",
    r"   / \  / ___| ____| \ | |_   _|      / ___|| | | | __ )/ ___|_   _|  _ \   / \|_   _| ____|",
    r"  / _ \| |  _|  _| |  \| | | |        \___ \| | | |  _ \\___ \ | | | |_) | / _ \ | | |  _|  ",
    r" / ___ \ |_| | |___| |\  | | |         ___) | |_| | |_) |___) || | |  _ < / ___ \| | | |___ ",
    r"/_/   \_\____|_____|_| \_| |_|        |____/ \___/|____/|____/ |_| |_| \_\_/   \_\_| |_____|",
]

INTRO_TEXT = "Welcome to Agent Substrate — the high-density execution runtime with a pierceable abstraction for Platform Engineers and AI Application Developers."

STEPS_DATA = [
    {
        "num": 1,
        "title": "Check your setup",
        "heading": "Check your environment",
        "desc": "We'll check if you have everything needed to run Substrate — a container runtime, Python, and kubectl CLI.",
        "cmd": "which docker && which kubectl && which python3",
        "chk_title": "Checking prerequisites...",
        "chk_items": [
            "Container runtime detected (Docker / Podman / Containerd)",
            "Python 3.10+ runtime available",
            "Kubectl command utility ready in PATH",
        ],
        "done": "Done",
        "prompt": "Prerequisites verified. Let's select your target cluster next.",
        "btn": "Connect your cluster [Enter ↵] →",
    },
    {
        "num": 2,
        "title": "Connect your cluster",
        "heading": "Select Cluster & Verify Substrate Control Plane",
        "desc": "Choose a cluster from your kubeconfig. We'll verify its provider type, region, and probe for existing Substrate components in real-time.",
        "cmd": "",
        "chk_title": "",
        "chk_items": [],
        "done": "",
        "prompt": "",
        "btn": "Turn on Substrate [Enter ↵] →",
        "custom_box": "cluster_side_by_side",
    },
    {
        "num": 3,
        "title": "Turn on Substrate",
        "heading": "Turn on Substrate Control Plane",
        "desc": "Installing the Substrate core controllers, state registry, and high-speed networking onto your cluster in namespace [substrate-system].",
        "cmd": "kubectl apply -f manifests/substrate-control-plane.yaml",
        "chk_title": "Installing Substrate components...",
        "chk_items": [
            "Applying CustomResourceDefinitions (WorkerPool, ActorTemplate, Actor)",
            "Deploying Valkey Metadata & State Registry",
            "Bootstrapping Substrate Gateway & API Server (listening on :8080)",
            "Initializing eBPF network routing controller in [substrate-system]",
        ],
        "done": "Done",
        "prompt": "Substrate control plane is active! Next, let's configure the worker pool node fleet.",
        "btn": "Set up WorkerPool [Enter ↵] →",
    },
    {
        "num": 4,
        "title": "Compatible Node Pool",
        "heading": "Set up Compatible WorkerPool Node Fleet",
        "desc": "Scanning cluster node pools for hardware nested virtualization. If no compatible pool is found, configure one via Custom Compute Class (CCC).",
        "cmd": "kubectl apply -f manifests/workerpool-ccc.yaml",
        "chk_title": "Configuring compatible node pool...",
        "chk_items": [
            "Scanning existing node pools: No hardware nested-virt pool detected",
            "Applying Custom Compute Class manifest [agent-spot-ccc] (n2-standard-48, KVM)",
            "Configuring Spot fallback & capacity reservation",
            "Compatible node pool ready for high-density agent sandboxing",
        ],
        "done": "Done",
        "prompt": "Compatible node pool configured! Now let's set up autoscaling.",
        "btn": "Configure Autoscaling [Enter ↵] →",
        "custom_box": "nodepool_ccc",
        "yaml_notice": "💡 Tip: You can modify and re-apply the Custom Compute Class YAML manifest later at any time (e.g. manifests/workerpool-ccc.yaml).",
    },
    {
        "num": 5,
        "title": "Configure Autoscaling",
        "heading": "Configure WorkerPool Autoscaling (HPA & CapacityBuffer)",
        "desc": "Configure horizontal pod autoscaling and standby capacity buffers for instant (<100ms) cold starts.",
        "cmd": "kubectl apply -f manifests/workerpool-autoscaling.yaml",
        "chk_title": "Applying autoscaling & capacity buffer...",
        "chk_items": [
            "Applying HorizontalPodAutoscaler (OneHPA: minReplicas=10, maxReplicas=100)",
            "Applying CapacityBuffer (fixed-replica-buffer: 3 standby replicas via buffer.gke.io/standby-capacity)",
            "Standby buffer verified: Ready for instant (<100ms) agent session injection",
        ],
        "done": "Done",
        "prompt": "Autoscaling active! Now let's deploy the default Substrate WorkerPool.",
        "btn": "Deploy WorkerPool [Enter ↵] →",
        "custom_box": "autoscaling_hpa",
        "yaml_notice": "💡 Tip: You can modify and re-apply the HPA and CapacityBuffer YAML manifests later at any time (e.g. manifests/workerpool-autoscaling.yaml).",
    },
    {
        "num": 6,
        "title": "Deploy WorkerPool",
        "heading": "Confirm & Deploy Substrate WorkerPool",
        "desc": "Deploy the default Substrate WorkerPool into namespace [substrate-system] with pre-warmed agent sandboxes.",
        "cmd": "kubectl apply -f manifests/default-workerpool.yaml",
        "chk_title": "Deploying default Substrate WorkerPool...",
        "chk_items": [
            "Resolving worker sandbox image (gcr.io/ate-platform/worker:v1)",
            "Deploying WorkerPool CR [default-worker-pool] in namespace [substrate-system]",
            "Provisioning 10 warm worker sandboxes (3 standby buffer replicas active)",
            "WorkerPool is ready: 10/10 warm pods listening for agent turns",
        ],
        "done": "Done",
        "prompt": "WorkerPool configured! Proceeding to installation summary.",
        "btn": "Complete Installation [Enter ↵] →",
        "custom_box": "deploy_wp",
    },
    {
        "num": 7,
        "title": "Installation Complete",
        "heading": "Agent Substrate on GKE Installation Complete! 🎉",
        "desc": "Agent Substrate on GKE installation is complete and the cluster is now ready for high-density agent workloads.",
        "cmd": "",
        "chk_title": "",
        "chk_items": [],
        "done": "",
        "prompt": "",
        "btn": "🚀 Finish & Close [Enter ↵]",
        "custom_box": "celebration_complete",
    },
]


def render_welcome_screen(typewriter_progress=1.0):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    wx, wy, ww, wh = 80, 40, 1120, 640
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=10, fill=BG_CANVAS, outline=BORDER_DARK, width=1)

    draw.rectangle([wx, wy, wx + ww, wy + 34], fill=(9, 13, 22))
    draw.ellipse([wx + 14, wy + 12, wx + 24, wy + 22], fill=(255, 95, 86))
    draw.ellipse([wx + 30, wy + 12, wx + 40, wy + 22], fill=(255, 189, 46))
    draw.ellipse([wx + 46, wy + 12, wx + 56, wy + 22], fill=(39, 201, 63))
    draw.text((wx + 360, wy + 10), "rajithal@rajithal: ~/workspaces/substrate — substrate onboard", fill=TEXT_MUTED, font=font_xs)

    # Shaded ambient container for ASCII art
    draw.rounded_rectangle([wx + 150, wy + 42, wx + 970, wy + 128], radius=8, fill=(11, 16, 25), outline=(25, 45, 65), width=1)

    ly = wy + 48
    vibrant_colors = [
        (0, 240, 255),   # Bright Electric Cyan
        (255, 59, 105),  # Bright Crimson
        (255, 208, 0),   # Bright Gold
        (0, 255, 136),   # Bright Emerald Green
        (56, 182, 255),  # Bright Sky Blue
    ]
    for i, line in enumerate(LOGO_LINES):
        # 3D Drop Shadow Shading
        draw.text((wx + 182, ly + 2), line, fill=(0, 0, 0), font=font_xs)
        draw.text((wx + 181, ly + 1), line, fill=(10, 20, 30), font=font_xs)
        draw.text((wx + 180, ly), line, fill=vibrant_colors[i % len(vibrant_colors)], font=font_xs)
        ly += 14

    tag_y = ly + 10
    draw.text((wx + 320, tag_y), "⚡ High-Density Sandboxing & Sub-100ms Cold-Start Runtime", fill=(0, 240, 255), font=font_sm)

    tw_y = tag_y + 24
    chars_to_show = int(len(INTRO_TEXT) * typewriter_progress)
    disp_text = INTRO_TEXT[:chars_to_show]
    if typewriter_progress < 1.0:
        disp_text += "▌"
    draw.text((wx + 130, tw_y), disp_text, fill=TEXT_PRIMARY, font=font_xs)

    fx, fy, fw, fh = wx + 130, tw_y + 26, 860, 118
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=8, fill=BG_CARD, outline=ACCENT_CYAN, width=1)
    draw.rounded_rectangle([fx + 16, fy - 10, fx + 260, fy + 8], radius=4, fill=ACCENT_BLUE)
    draw.text((fx + 24, fy - 8), "⚡ CORE SUBSTRATE CAPABILITIES", fill=TEXT_WHITE, font=font_xs)

    rows = [
        ("🛠️  Platform Fleet :", "Warm worker pools on pre-existing K8s with MicroVM & capacity buffers", GOOGLE_BLUE),
        ("🤖  Agent Workloads :", "No-YAML container templates, turn hooks & request parking", GOOGLE_GREEN),
        ("⚡  Instant Resume  :", "Suspend idle actors to 0% CPU; restore state in <200ms", GOOGLE_YELLOW),
        ("🔒  Gated Access    :", "Automatic detection & terms acknowledgment on Google Cloud GKE", GOOGLE_RED),
    ]
    ry = fy + 16
    for lbl, desc, col in rows:
        draw.text((fx + 16, ry), lbl, fill=col, font=font_xs)
        draw.text((fx + 180, ry), desc, fill=TEXT_WHITE, font=font_xs)
        ry += 24

    tx = wx + 130
    ty = fy + fh + 14
    draw.text((tx, ty), "Choose your installation path:", fill=TEXT_WHITE, font=font_sm)
    draw.text((tx + fw - 160, ty), "Press [1] or [2]", fill=ACCENT_CYAN, font=font_xs)

    tracks = [
        ("[1] * Quickstart — Automatic cluster detection & default configuration (Recommended)", "Automatically connects to your pre-configured cluster and applies sensible defaults in seconds.", True),
        ("[2] # Advanced — Custom installation with kubectl", "Customize YAML manifests, resource quotas, microVM isolation drivers, and eBPF routing rules.", False),
    ]
    card_y = ty + 22
    for t_title, t_desc, t_sel in tracks:
        c_bg = ACCENT_BLUE if t_sel else BG_CARD
        c_outline = ACCENT_CYAN if t_sel else BORDER_SUBTLE
        draw.rounded_rectangle([tx, card_y, tx + fw, card_y + 44], radius=6, fill=c_bg, outline=c_outline, width=1)
        draw.text((tx + 12, card_y + 6), t_title, fill=TEXT_WHITE, font=font_xs)
        draw.text((tx + 12, card_y + 24), t_desc, fill=(211, 227, 253) if t_sel else TEXT_MUTED, font=font_xs)
        card_y += 50

    bx, by = wx + 130, card_y + 8
    draw.rounded_rectangle([bx, by, bx + fw, by + 28], radius=6, fill=(13, 17, 23), outline=BORDER_DARK, width=1)
    badges = ["✔ K8s: Connected", "✔ Python 3.10+: Ready", "⚡ MicroVM: Ready", "★ GKE & K8s: Supported"]
    badge_x = bx + 24
    for b in badges:
        draw.text((badge_x, by + 6), b, fill=ACCENT_GREEN if "✔" in b else (ACCENT_GREEN if "★" in b else ACCENT_CYAN), font=font_xs)
        badge_x += 210

    # Bottom Persistent TUI Keymap Dock Bar
    draw.rectangle([wx, wy + wh - 30, wx + ww, wy + wh], fill=(9, 13, 22))
    draw.line([wx, wy + wh - 30, wx + ww, wy + wh - 30], fill=BORDER_DARK, width=1)
    draw.text((wx + 16, wy + wh - 22), "[↵] Begin Setup   [1] Quickstart   [2] Advanced   [?] Help", fill=ACCENT_CYAN, font=font_xs)
    draw.text((wx + ww - 90, wy + wh - 22), "Welcome", fill=TEXT_MUTED, font=font_xs)

    return img


def render_step_frame(step_idx):
    data = STEPS_DATA[step_idx]
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    wx, wy, ww, wh = 80, 40, 1120, 640
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=10, fill=BG_CONTENT, outline=BORDER_DARK, width=1)

    draw.rectangle([wx, wy, wx + ww, wy + 34], fill=(9, 13, 22))
    draw.ellipse([wx + 14, wy + 12, wx + 24, wy + 22], fill=(255, 95, 86))
    draw.ellipse([wx + 30, wy + 12, wx + 40, wy + 22], fill=(255, 189, 46))
    draw.text((wx + 70, wy + 10), "rajithal@rajithal: ~/workspaces/substrate — substrate onboard", fill=TEXT_MUTED, font=font_xs)
    if step_idx >= 1:
        # Top Header Cluster Context Badge
        draw.rounded_rectangle([wx + ww - 380, wy + 6, wx + ww - 14, wy + 28], radius=11, fill=(18, 30, 48), outline=ACCENT_CYAN, width=1)
        draw.ellipse([wx + ww - 370, wy + 14, wx + ww - 364, wy + 20], fill=ACCENT_GREEN)
        draw.text((wx + ww - 358, wy + 9), "Connected: gke_enterprise_us-central1_prod", fill=ACCENT_CYAN, font=font_xs)

    # Left Sidebar (width 230)
    sw = 230
    draw.rectangle([wx, wy + 35, wx + sw, wy + wh], fill=BG_CANVAS)
    draw.line([wx + sw, wy + 35, wx + sw, wy + wh], fill=BORDER_DARK, width=1)

    draw.text((wx + 16, wy + 48), "Agent Substrate", fill=ACCENT_CYAN, font=font_base)
    draw.text((wx + 16, wy + 66), "Getting set up", fill=TEXT_MUTED, font=font_xs)

    draw.line([wx + 16, wy + 86, wx + sw - 16, wy + 86], fill=(33, 38, 45), width=3)
    fill_w = int(((step_idx + 1) / 7.0) * (sw - 32))
    draw.line([wx + 16, wy + 86, wx + 16 + fill_w, wy + 86], fill=ACCENT_CYAN, width=3)

    draw.text((wx + 16, wy + 96), f"{step_idx} of 7 steps", fill=TEXT_MUTED, font=font_xs)

    # 7 Steps List in Sidebar
    sy = wy + 116
    for i, s in enumerate(STEPS_DATA):
        num = i + 1
        if i < step_idx:
            draw.text((wx + 16, sy), "✓", fill=ACCENT_GREEN, font=font_xs)
            draw.text((wx + 30, sy), s["title"][:22], fill=TEXT_PRIMARY, font=font_xs)
        elif i == step_idx:
            draw.text((wx + 16, sy), str(num), fill=ACCENT_CYAN, font=font_xs)
            draw.text((wx + 30, sy), s["title"][:22], fill=ACCENT_CYAN, font=font_xs)
        else:
            draw.text((wx + 16, sy), str(num), fill=TEXT_DIM, font=font_xs)
            draw.text((wx + 30, sy), s["title"][:22], fill=TEXT_DIM, font=font_xs)
        sy += 24

    # Right Content Area
    cx = wx + sw + 30
    cy = wy + 42
    cw = ww - sw - 60

    draw.text((cx, cy), f"Step {data['num']} of 7", fill=TEXT_MUTED, font=font_xs)
    draw.text((cx, cy + 16), data["heading"], fill=TEXT_WHITE, font=font_md)
    draw.text((cx, cy + 38), data["desc"], fill=TEXT_PRIMARY, font=font_xs)

    # STEP 2: SIDE-BY-SIDE CLUSTER SELECTOR
    if data.get("custom_box") == "cluster_side_by_side":
        cy_step2 = cy + 64
        half_w = (cw - 16) // 2

        draw.text((cx, cy_step2), "Target Cluster (Press [1-4]):", fill=TEXT_WHITE, font=font_xs)
        clusters_info = [
            ("[1] * gke_enterprise_us-central1_prod", "GKE • Region: us-central1 (Iowa) • 12 nodes", True),
            ("[2] # aws-eks-production-us-east-1", "EKS • Region: us-east-1 (N. Virginia) • 8 nodes", False),
            ("[3] # azure-aks-agent-fleet-eastus", "AKS • Region: eastus (Virginia) • 6 nodes", False),
            ("[4] # kind-substrate-sandbox", "Kind • Region: local (localhost) • 3 nodes", False),
        ]
        list_y = cy_step2 + 18
        for c_title, c_desc, c_sel in clusters_info:
            c_bg = ACCENT_BLUE if c_sel else BG_CMD
            c_out = ACCENT_CYAN if c_sel else BORDER_SUBTLE
            draw.rounded_rectangle([cx, list_y, cx + half_w, list_y + 40], radius=6, fill=c_bg, outline=c_out, width=1)
            draw.text((cx + 10, list_y + 5), c_title, fill=TEXT_WHITE, font=font_xs)
            draw.text((cx + 10, list_y + 22), c_desc, fill=(211, 227, 253) if c_sel else TEXT_MUTED, font=font_xs)
            list_y += 46

        rx = cx + half_w + 16
        draw.text((rx, cy_step2), "Verification & Probe Status:", fill=TEXT_WHITE, font=font_xs)

        box_y = cy_step2 + 18
        draw.rounded_rectangle([rx, box_y, rx + half_w, box_y + 88], radius=6, fill=BG_CARD, outline=ACCENT_CYAN, width=1)
        draw.text((rx + 12, box_y + 8), "🌐 CLUSTER VERIFICATION:", fill=ACCENT_CYAN, font=font_xs)
        draw.text((rx + 12, box_y + 24), "• Provider: Google Kubernetes Engine (GKE v1.31) [✓]", fill=TEXT_WHITE, font=font_xs)
        draw.text((rx + 12, box_y + 40), "• Region  : us-central1 (Iowa)", fill=GOOGLE_BLUE, font=font_xs)
        draw.text((rx + 12, box_y + 56), "• Capacity: 12 ready nodes (Hardware microVM ready)", fill=ACCENT_GREEN, font=font_xs)
        draw.text((rx + 12, box_y + 72), "• Substrate: [substrate-system] ➔ Clean Ready", fill=ACCENT_YELLOW, font=font_xs)

        chk_y = box_y + 98
        draw.rounded_rectangle([rx, chk_y, rx + half_w, chk_y + 68], radius=6, fill=BG_CMD, outline=BORDER_DARK, width=1)
        draw.text((rx + 12, chk_y + 8), "⚡ PROBE CHECKLIST:", fill=ACCENT_CYAN, font=font_xs)
        draw.text((rx + 12, chk_y + 24), "  ✓ API Reachability: Connected to active context", fill=TEXT_WHITE, font=font_xs)
        draw.text((rx + 12, chk_y + 44), "  ✓ Clean cluster ready for Substrate install", fill=ACCENT_GREEN, font=font_xs)

        by = chk_y + 78

    elif data.get("custom_box") in ["nodepool_ccc", "autoscaling_hpa", "deploy_wp"]:
        # Option Selection Step (Steps 4, 5, 6)
        ey = cy + 50

        if data.get("yaml_notice"):
            draw.rounded_rectangle([cx, ey, cx + cw, ey + 24], radius=4, fill=(25, 28, 20), outline=ACCENT_YELLOW, width=1)
            draw.text((cx + 10, ey + 5), data["yaml_notice"], fill=ACCENT_YELLOW, font=font_xs)
            ey += 30

        draw.text((cx, ey), "Choose configuration option (Press [1-3]):", fill=TEXT_WHITE, font=font_xs)
        ey += 16

        if data["custom_box"] == "nodepool_ccc":
            draw.rounded_rectangle([cx, ey, cx + cw, ey + 36], radius=6, fill=(25, 28, 20), outline=ACCENT_YELLOW, width=1)
            draw.text((cx + 10, ey + 4), "🔍 CLUSTER NODE POOL SCAN: Probed 12 nodes across 2 zones", fill=ACCENT_CYAN, font=font_xs)
            draw.text((cx + 10, ey + 18), "⚠️ Scan Result: No node pool detected with hardware nested virtualization enabled.", fill=ACCENT_YELLOW, font=font_xs)
            ey += 42
            opts = [
                ("[1] * Automatically create a compatible node pool using Custom Compute Class (Recommended)", "Applies manifest with n2-standard-48, Spot fallback, and nested virtualization enabled.", True),
                ("[2] # Create a compatible node pool manually via gcloud", "Generates gcloud container node-pools create command with --enable-nested-virtualization.", False),
                ("[3] # Choose a different cluster", "Return to Step 2 to select another cluster context from your kubeconfig.", False),
            ]
        elif data["custom_box"] == "autoscaling_hpa":
            opts = [
                ("[1] * Automatically configure HPA & CapacityBuffer with sensible defaults (Recommended)", "Applies OneHPA (min=10, max=100) and fixed-replica-buffer (3 standby replicas) for <100ms injection.", True),
                ("[2] # Configure autoscaling manually via kubectl", "Export template manifests to customize scaling metrics, CPU/memory thresholds, and buffer headroom.", False),
                ("[3] # Skip autoscaling configuration", "Keep fixed worker pool replica count without horizontal dynamic scaling.", False),
            ]
        else: # deploy_wp
            opts = [
                ("[1] * Yes, deploy default Substrate WorkerPool [default-worker-pool] (Recommended)", "Bootstraps 10 warm worker sandboxes with microVM isolation and instant actor attachment in [substrate-system].", True),
                ("[2] # No, skip default WorkerPool deployment", "Skip initial worker pool provisioning. You can create custom worker pools at any time via kubectl or atectl.", False),
            ]

        for o_title, o_desc, o_sel in opts:
            o_bg = ACCENT_BLUE if o_sel else BG_CMD
            o_out = ACCENT_CYAN if o_sel else BORDER_SUBTLE
            draw.rounded_rectangle([cx, ey, cx + cw, ey + 36], radius=6, fill=o_bg, outline=o_out, width=1)
            draw.text((cx + 10, ey + 4), o_title, fill=TEXT_WHITE, font=font_xs)
            draw.text((cx + 10, ey + 19), o_desc, fill=(211, 227, 253) if o_sel else TEXT_MUTED, font=font_xs)
            ey += 40

        card_h = 130
        draw.rounded_rectangle([cx, ey, cx + cw, ey + card_h], radius=6, fill=BG_CARD, outline=BORDER_DARK, width=1)
        draw.text((cx + 16, ey + 10), data["chk_title"], fill=ACCENT_CYAN, font=font_sm)
        iy = ey + 28
        for item in data["chk_items"][:3]:
            draw.text((cx + 16, iy), "✓", fill=ACCENT_GREEN, font=font_sm)
            draw.text((cx + 34, iy), item, fill=TEXT_WHITE, font=font_xs)
            iy += 18
        draw.text((cx + 16, iy + 4), data["done"], fill=ACCENT_GREEN, font=font_base)
        draw.text((cx + 16, iy + 22), data["prompt"], fill=TEXT_PRIMARY, font=font_xs)
        by = ey + card_h + 10

    elif data.get("custom_box") == "celebration_complete":
        # STEP 7: CELEBRATION, ASCII LOGO, METRICS & NEXT STEPS
        ey = cy + 40
        # Celebratory Banner with ASCII Logo
        draw.rounded_rectangle([cx, ey, cx + cw, ey + 82], radius=8, fill=(18, 30, 24), outline=ACCENT_GREEN, width=1)
        ascii_lines_sm = [
            "    _    ____ _____ _   _ _____        ____  _   _ ____  ____ _____ ____     _  _____ _____",
            "   / \\  / ___| ____| \\ | |_   _|      / ___|| | | | __ )/ ___|_   _|  _ \\   / \\|_   _| ____|",
            "  / _ \\| |  _|  _| |  \\| | | |        \\___ \\| | | |  _ \\\\___ \\ | | | |_) | / _ \\ | | |  _|",
            " / ___ \\ |_| | |___| |\\  | | |         ___) | |_| | |_) |___) || | |  _ < / ___ \\| | | |___",
            "/_/   \\_\\____|_____|_| \\_| |_|        |____/ \\___/|____/|____/ |_| |_| \\_\\_/   \\_\\_| |_____|"
        ]
        ay = ey + 5
        for line in ascii_lines_sm:
            draw.text((cx + 14, ay), line, fill=ACCENT_CYAN, font=font_mono)
            ay += 11
        draw.text((cx + 14, ay + 3), "⚡ High-Density MicroVM Runtime Active (Ready for workloads)", fill=ACCENT_GREEN, font=font_xs)
        ey += 90

        # Live Verification Cold-Start Playground
        draw.rounded_rectangle([cx, ey, cx + cw, ey + 64], radius=8, fill=(15, 25, 38), outline=ACCENT_CYAN, width=1)
        draw.text((cx + 14, ey + 8), "⚡ LIVE VERIFICATION PLAYGROUND  •  Run live cold-start verification? [y/n]", fill=ACCENT_CYAN, font=font_xs)
        draw.text((cx + 14, ey + 25), "✓ [y] Yes, run test turn (48ms verified)   │   [n] No, skip test turn", fill=ACCENT_GREEN, font=font_xs)
        draw.text((cx + 14, ey + 42), "{\"status\": \"ready\", \"worker\": \"default-worker-pool-8f4b\", \"latency\": \"48ms\"}", fill=GOOGLE_BLUE, font=font_xs)
        ey += 72

        # Next Step 1: Deploy actor & Port-forward
        draw.rounded_rectangle([cx, ey, cx + cw, ey + 92], radius=8, fill=BG_CMD, outline=BORDER_SUBTLE, width=1)
        draw.text((cx + 14, ey + 8), "🔌 0. Connect local terminal: kubectl port-forward svc/substrate-gateway 8080:8080 -n substrate-system", fill=ACCENT_CYAN, font=font_xs)
        draw.text((cx + 14, ey + 28), "🤖 1. Deploy first actor: atectl actor create my-first-actor --workerpool=default-worker-pool", fill=ACCENT_YELLOW, font=font_xs)
        draw.text((cx + 14, ey + 48), "      Execute turn     : atectl actor execute my-first-actor --prompt=\"Analyze logs\"", fill=TEXT_WHITE, font=font_xs)
        draw.text((cx + 14, ey + 68), "📊 2. Stream telemetry : atectl logs workerpool/default-worker-pool --follow", fill=GOOGLE_BLUE, font=font_xs)
        ey += 100

        # Teardown footnote
        draw.rounded_rectangle([cx, ey, cx + cw, ey + 32], radius=6, fill=BG_CMD, outline=BORDER_DARK, width=1)
        draw.text((cx + 14, ey + 9), "💡 Clean up anytime: kubectl delete -f manifests/substrate-control-plane.yaml or atectl uninstall", fill=TEXT_MUTED, font=font_xs)
        by = ey + 42

    else:
        # Step 1 (Clean Preflight Checklist) or Step 3 (GitOps Manifest + Checklist)
        ey = cy + 56
        if data["num"] == 3:
            # Declarative GitOps Drawer
            draw.rounded_rectangle([cx, ey, cx + cw, ey + 38], radius=6, fill=BG_CMD, outline=ACCENT_CYAN, width=1)
            draw.text((cx + 12, ey + 8), "</> Declarative Control-Plane Manifest: manifests/substrate-control-plane.yaml", fill=ACCENT_CYAN, font=font_xs)
            draw.text((cx + 12, ey + 22), "kubectl apply -f manifests/substrate-control-plane.yaml", fill=TEXT_WHITE, font=font_xs)
            ey += 46

        card_h = 180 if data["num"] == 1 else 150
        draw.rounded_rectangle([cx, ey, cx + cw, ey + card_h], radius=8, fill=BG_CARD, outline=BORDER_DARK, width=1)
        draw.text((cx + 20, ey + 10), data["chk_title"], fill=ACCENT_CYAN, font=font_sm)

        iy = ey + 28
        for item in data["chk_items"]:
            draw.text((cx + 20, iy), "✓", fill=ACCENT_GREEN, font=font_sm)
            draw.text((cx + 40, iy), item, fill=TEXT_WHITE, font=font_xs)
            iy += 20

        draw.text((cx + 20, iy + 4), data["done"], fill=ACCENT_GREEN, font=font_base)
        draw.text((cx + 20, iy + 22), data["prompt"], fill=TEXT_PRIMARY, font=font_xs)
        by = ey + card_h + 10

    # Bottom Persistent TUI Keymap Dock Bar
    draw.rectangle([wx, wy + wh - 30, wx + ww, wy + wh], fill=(9, 13, 22))
    draw.line([wx, wy + wh - 30, wx + ww, wy + wh - 30], fill=BORDER_DARK, width=1)

    keymap_str = "[↵] Next   [1-4] Pick & Advance   [↑/↓] Select   [b] Back   [m] YAML   [?] Help"
    if step_idx == 0:
        keymap_str = "[↵] Next: Connect Cluster   [b] Back   [?] Help"
    elif step_idx == 1:
        keymap_str = "[↵] Next: Turn on Substrate   [1-4] Pick & Advance   [↑/↓] Select   [b] Back   [?] Help"
    elif step_idx == 2:
        keymap_str = "[↵] Next: Node Pool   [m] YAML Manifest   [b] Back   [?] Help"
    elif step_idx == 3:
        keymap_str = "[↵] Next: Autoscaling   [1-3] Pick & Advance   [↑/↓] Select   [m] YAML   [b] Back   [?] Help"
    elif step_idx == 4:
        keymap_str = "[↵] Next: WorkerPool   [1-3] Pick & Advance   [↑/↓] Select   [m] YAML   [b] Back   [?] Help"
    elif step_idx == 5:
        keymap_str = "[↵] Finish Installation   [1-2] Pick & Advance   [↑/↓] Select   [m] YAML   [b] Back   [?] Help"
    elif step_idx == 6:
        keymap_str = "[↵] Close   [y] Run Test Turn   [n] Skip   [0] Restart Setup   [b] Back   [?] Help"

    draw.text((wx + 16, wy + wh - 22), keymap_str, fill=ACCENT_CYAN, font=font_xs)
    draw.text((wx + ww - 110, wy + wh - 22), f"Step {step_idx + 1} of 7", fill=TEXT_MUTED, font=font_xs)

    return img


def generate_demo_video(output_path="demos/onboarding-tui/onboarding_demo.mp4"):
    print(f"🎬 Generating HD Demo Video: {output_path}...")
    writer = imageio.get_writer(output_path, fps=FPS, codec="libx264", quality=8)

    num_welcome_frames = int(3.0 * FPS)
    for f in range(num_welcome_frames):
        progress = min(1.0, (f + 1) / (FPS * 1.5))
        w_img = render_welcome_screen(typewriter_progress=progress)
        writer.append_data(np.array(w_img))

    durations = [2.2, 3.2, 2.5, 3.0, 3.0, 3.0, 3.5]
    for i in range(7):
        num_frames = int(durations[i] * FPS)
        frame_img = render_step_frame(i)
        frame_np = np.array(frame_img)
        for _ in range(num_frames):
            writer.append_data(frame_np)

    writer.close()
    print(f"✅ Video generated successfully: {output_path}")


def export_step_screenshots(out_dir="demos/onboarding-tui/screenshots"):
    os.makedirs(out_dir, exist_ok=True)
    print(f"📸 Exporting high-res screenshots to {out_dir}...")
    
    w_img = render_welcome_screen(typewriter_progress=1.0)
    w_img.save(os.path.join(out_dir, "step0_welcome.png"))
    print("  ✓ Saved step0_welcome.png")

    for i in range(7):
        fname = f"step{i+1}_{STEPS_DATA[i]['title'].lower().replace(' ', '_').replace('&', 'and')}.png"
        img = render_step_frame(i)
        img.save(os.path.join(out_dir, fname))
        print(f"  ✓ Saved {fname}")


if __name__ == "__main__":
    export_step_screenshots()
    generate_demo_video()
