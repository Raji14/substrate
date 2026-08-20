"""High-Definition (720p/1080p) Video Recording Generator for Agent Substrate Onboarding.

Features:
- "Agent Substrate" Google 4-color gradient splash title
- 2 Streamlined installation choices (Quickstart & Advanced)
- Step 2: Side-by-side cluster selection list (Left) and verification probe (Right)
- Step 5: Compatible Node Pool (CCC / Nested-Virt scanning) with YAML re-apply note
- Step 6: WorkerPool Autoscaling (OneHPA min=10 max=100 & CapacityBuffer=3 standby)
- Step 7: Confirm & Deploy Substrate WorkerPool (10 warm replicas)
- Step 8-12: CLI Install, First Actor, Send Request, Pause/Resume, Scale Up
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

font_xs = ImageFont.truetype(FONT_PATH, 11)
font_sm = ImageFont.truetype(FONT_PATH, 13)
font_base = ImageFont.truetype(FONT_PATH, 15)
font_md = ImageFont.truetype(FONT_PATH, 17)
font_lg = ImageFont.truetype(FONT_PATH, 20)

LOGO_LINES = [
    "    _    ____ _____ _   _ _____   ____  _   _ ____  ____ _____ ____     _  _____ _____ ",
    "   / \\  / ___| ____| \\ | |_   _| / ___|| | | | __ )/ ___|_   _|  _ \\   / \\|_   _| ____|",
    "  / _ \\| |  _|  _| |  \\| | | |   \\___ \\| | | |  _ \\\\___ \\ | | | |_) | / _ \\ | | |  _|  ",
    " / ___ \\ |_| | |___| |\\  | | |    ___) | |_| | |_) |___) || | |  _ < / ___ \\| | | |___ ",
    "/_/   \\_\\____|_____|_| \\_| |_|   |____/ \\___/|____/|____/ |_| |_| \\_\\_/   \\_\\_| |_____|",
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
        "desc": "Choose a cluster from your kubeconfig. We'll verify its provider type and probe for existing Substrate components in real-time.",
        "cmd": "",
        "chk_title": "",
        "chk_items": [],
        "done": "",
        "prompt": "",
        "btn": "Private GA Agreement [Enter ↵] →",
        "custom_box": "cluster_side_by_side",
    },
    {
        "num": 3,
        "title": "Private GA Agreement",
        "heading": "Private GA Access & Contractual Agreement",
        "desc": "Because this is a Private General Availability release, customers must acknowledge that production support requires an agreement with Google.",
        "cmd": 'atectl auth register --customer="Acme Corp" --token="ga-sub-8f92a-live-contract"',
        "chk_title": "Registering Private GA customer...",
        "chk_items": [
            "Customer credentials & organization verified (Acme Corp)",
            "Private GA License Token registered: [ga-sub-8f92a-live-contract]",
            "Acknowledgment recorded: Production support requires an agreement with Google",
        ],
        "done": "Done",
        "prompt": "Private GA agreement acknowledged! Now let's turn on Substrate.",
        "btn": "Turn on Substrate [Enter ↵] →",
        "custom_box": "agreement",
    },
    {
        "num": 4,
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
        "num": 5,
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
        "num": 6,
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
        "num": 7,
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
        "prompt": "Default WorkerPool deployed! Now let's install the developer CLI.",
        "btn": "Install the CLI [Enter ↵] →",
        "custom_box": "deploy_wp",
    },
    {
        "num": 8,
        "title": "Install the CLI",
        "heading": "Install the atectl CLI",
        "desc": "The atectl tool lets you manage actors, worker pools, and memory snapshots with simple commands — zero Kubernetes YAML required.",
        "cmd": "go install ./cmd/atectl || curl -sSL https://ate.dev/atectl | sh",
        "chk_title": "Configuring developer CLI...",
        "chk_items": [
            "Downloading atectl binary for your architecture (macOS / Linux)",
            "Registering shell autocompletions and PATH bindings",
            "CLI verified: atectl version v0.2.1-ga",
        ],
        "done": "Done",
        "prompt": "CLI is installed and ready. Let's deploy your first actor!",
        "btn": "Deploy first actor [Enter ↵] →",
    },
    {
        "num": 9,
        "title": "First actor",
        "heading": "Deploy your first actor",
        "desc": "Launch an AI agent container from a standard template into a pre-warmed sandbox — no YAML manifests required.",
        "cmd": "atectl actor create my-first-actor --template=default-agent --atespace=default-atespace",
        "chk_title": "Launching actor session...",
        "chk_items": [
            "Resolving agent container image (gcr.io/ate-platform/agent:v1)",
            "Injecting into pre-warmed worker sandbox",
            "Actor [my-first-actor] is live and listening on port 8080",
        ],
        "done": "Done",
        "prompt": "Actor is running! Let's send it an interactive request.",
        "btn": "Send a request [Enter ↵] →",
    },
    {
        "num": 10,
        "title": "Send a request",
        "heading": "Send a request to your actor",
        "desc": "Communicate with your running actor through the Substrate Gateway with real-time response streaming.",
        "cmd": 'atectl actor execute my-first-actor --prompt="Analyze recent logs and report status"',
        "chk_title": "Streaming execution turn...",
        "chk_items": [
            "Routing turn request through Substrate Gateway",
            "Actor turn completed in 82ms (First token: 14ms)",
            'Response: "System operating normally. 0 errors detected."',
        ],
        "done": "Done",
        "prompt": "Great response! Now let's see how Substrate saves compute when idle.",
        "btn": "Test Pause & Resume [Enter ↵] →",
        "benchmark": "Turn Latency: 82ms  │  TTFT (First Token): 14ms  │  Throughput: 120 tok/s",
    },
    {
        "num": 11,
        "title": "Pause & resume",
        "heading": "Pause & resume (0% idle CPU)",
        "desc": "When agents are idle waiting for human input, Substrate checkpoints their memory to disk to save 90% compute, waking them in under 200ms.",
        "cmd": "atectl actor suspend my-first-actor && atectl actor resume my-first-actor",
        "chk_title": "Testing data plane suspend/resume...",
        "chk_items": [
            "Suspending idle actor memory state to disk (38ms, CPU drops to 0%)",
            "Request parking held incoming user message in queue",
            "Restoring actor memory state on wake event in 115ms",
        ],
        "done": "Done",
        "prompt": "Sub-200ms instant resume confirmed! Finally, let's scale your fleet.",
        "btn": "Scale it up [Enter ↵] →",
        "benchmark": "Cold Start (890ms) ➔ Suspend (38ms, 0% CPU) ➔ Warm Resume (115ms)",
    },
    {
        "num": 12,
        "title": "Scale it up",
        "heading": "Scale worker fleet & Day-2 Operations",
        "desc": "Scale worker pools with pre-warmed standby capacity buffers so your agent swarms are always ready for traffic spikes.",
        "cmd": "atectl create workerpools production-fleet --workers=20 --isolation=microvm",
        "chk_title": "Scaling worker pool capacity...",
        "chk_items": [
            "Worker pool [production-fleet] scaled to 20 warm pods",
            "Standby CapacityBuffer configured (3 warm spares ready)",
            "Live inspection verified: atectl get workerpools (Ready: 20/20)",
        ],
        "done": "Complete 🎉",
        "prompt": "You're all set! Enjoy building high-density AI agents with Agent Substrate.",
        "btn": "Finish Onboarding [Enter ↵]",
    },
]


def render_welcome_screen(typewriter_progress=1.0):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    wx, wy, ww, wh = 80, 40, 1120, 640
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=10, fill=BG_CANVAS, outline=BORDER_DARK, width=1)

    draw.rectangle([wx, wy, wx + ww, wy + 34], fill=(9, 13, 22))
    draw.line([wx, wy + 34, wx + ww, wy + 34], fill=BORDER_DARK, width=1)
    draw.ellipse([wx + 14, wy + 12, wx + 24, wy + 22], fill=(255, 95, 86))
    draw.ellipse([wx + 30, wy + 12, wx + 40, wy + 22], fill=(255, 189, 46))
    draw.ellipse([wx + 46, wy + 12, wx + 56, wy + 22], fill=(39, 201, 63))
    draw.text((wx + 360, wy + 10), "rajithal@rajithal: ~/workspaces/substrate — substrate onboard", fill=TEXT_MUTED, font=font_xs)

    ly = wy + 42
    logo_colors = [GOOGLE_BLUE, GOOGLE_RED, GOOGLE_YELLOW, GOOGLE_GREEN, GOOGLE_BLUE]
    for i, line in enumerate(LOGO_LINES):
        draw.text((wx + 180, ly), line, fill=logo_colors[i % len(logo_colors)], font=font_sm)
        ly += 16

    draw.text((wx + 270, ly + 4), "⚡ High-Density Sandboxing & Sub-100ms Cold-Start Runtime", fill=ACCENT_CYAN, font=font_sm)

    num_chars = int(len(INTRO_TEXT) * typewriter_progress)
    typed_str = INTRO_TEXT[:num_chars]
    cursor = " ▌" if typewriter_progress < 1.0 else ""
    
    if len(typed_str) > 78:
        split_pt = typed_str[:78].rfind(" ")
        line1 = typed_str[:split_pt]
        line2 = typed_str[split_pt+1:] + cursor
        draw.text((wx + 180, ly + 26), line1, fill=TEXT_PRIMARY, font=font_xs)
        draw.text((wx + 180, ly + 42), line2, fill=TEXT_PRIMARY, font=font_xs)
    else:
        draw.text((wx + 180, ly + 26), typed_str + cursor, fill=TEXT_PRIMARY, font=font_xs)

    fy = ly + 76
    draw.rounded_rectangle([wx + 100, fy, wx + ww - 100, fy + 88], radius=8, fill=BG_CARD, outline=ACCENT_CYAN, width=1)
    draw.rounded_rectangle([wx + 116, fy - 10, wx + 360, fy + 10], radius=4, fill=ACCENT_BLUE, outline=ACCENT_CYAN)
    draw.text((wx + 126, fy - 6), "⚡ CORE SUBSTRATE CAPABILITIES", fill=TEXT_WHITE, font=font_xs)

    draw.text((wx + 120, fy + 16), "*   Platform Fleet   : Warm worker pools on pre-existing K8s with MicroVM & capacity buffers", fill=GOOGLE_BLUE, font=font_xs)
    draw.text((wx + 120, fy + 32), "*   Agent Workloads  : No-YAML container templates, turn hooks & request parking", fill=GOOGLE_GREEN, font=font_xs)
    draw.text((wx + 120, fy + 48), "*   Instant Resume   : Suspend idle actors to 0% CPU; restore state in <200ms", fill=GOOGLE_YELLOW, font=font_xs)
    draw.text((wx + 120, fy + 64), "*   Private GA Gated : Customer registration & explicit Google support terms acknowledgment", fill=GOOGLE_RED, font=font_xs)

    ty = fy + 100
    draw.text((wx + 100, ty), "Choose your installation path (Press [1] or [2]):", fill=TEXT_WHITE, font=font_sm)

    tracks = [
        ("[1]  *  Quickstart — Automatic cluster detection & default configuration (Recommended)", "Automatically connects to your pre-configured cluster and applies sensible defaults in seconds.", True),
        ("[2]  #  Advanced — Custom installation with kubectl", "Customize YAML manifests, resource quotas, microVM isolation drivers, and eBPF routing rules.", False),
    ]
    toy = ty + 22
    for title, desc, is_sel in tracks:
        bg = ACCENT_BLUE if is_sel else BG_CARD
        out = ACCENT_CYAN if is_sel else BORDER_SUBTLE
        draw.rounded_rectangle([wx + 100, toy, wx + ww - 100, toy + 42], radius=6, fill=bg, outline=out, width=1)
        draw.text((wx + 114, toy + 7), "▶" if is_sel else "○", fill=TEXT_WHITE if is_sel else ACCENT_CYAN, font=font_sm)
        draw.text((wx + 134, toy + 6), title, fill=TEXT_WHITE, font=font_xs)
        draw.text((wx + 134, toy + 22), desc, fill=(211, 227, 253) if is_sel else TEXT_MUTED, font=font_xs)
        toy += 48

    dy = toy + 8
    draw.rounded_rectangle([wx + 100, dy, wx + ww - 100, dy + 26], radius=6, fill=BG_CONTENT, outline=BORDER_DARK, width=1)
    diag_str = "✓ Pre-configured K8s: Connected   │   ✓ Python 3.10+: Ready   │   * MicroVM Sandbox: Ready   │   * Private GA: Gated"
    draw.text((wx + 130, dy + 7), diag_str, fill=ACCENT_GREEN, font=font_xs)

    by = dy + 34
    draw.rounded_rectangle([wx + ww - 460, by, wx + ww - 100, by + 34], radius=6, fill=ACCENT_BLUE, outline=ACCENT_CYAN, width=1)
    draw.text((wx + ww - 440, by + 9), "▶  Press [Enter ↵] to Begin Getting Set Up →", fill=TEXT_WHITE, font=font_sm)

    return img


def render_step_frame(step_idx=0):
    data = STEPS_DATA[step_idx]
    img = Image.new("RGB", (WIDTH, HEIGHT), (9, 13, 22))
    draw = ImageDraw.Draw(img)

    wx, wy, ww, wh = 80, 40, 1120, 640
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=10, fill=BG_CONTENT, outline=BORDER_DARK, width=1)

    draw.rectangle([wx, wy, wx + ww, wy + 34], fill=BG_CANVAS)
    draw.line([wx, wy + 34, wx + ww, wy + 34], fill=BORDER_DARK, width=1)
    draw.ellipse([wx + 14, wy + 12, wx + 24, wy + 22], fill=(255, 95, 86))
    draw.ellipse([wx + 30, wy + 12, wx + 40, wy + 22], fill=(255, 189, 46))
    draw.ellipse([wx + 46, wy + 12, wx + 56, wy + 22], fill=(39, 201, 63))
    draw.text((wx + 360, wy + 10), "rajithal@rajithal: ~/workspaces/substrate — substrate onboard", fill=TEXT_MUTED, font=font_xs)

    # Left Sidebar (width 230)
    sw = 230
    draw.rectangle([wx, wy + 35, wx + sw, wy + wh], fill=BG_CANVAS)
    draw.line([wx + sw, wy + 35, wx + sw, wy + wh], fill=BORDER_DARK, width=1)

    draw.text((wx + 16, wy + 48), "Substrate", fill=ACCENT_CYAN, font=font_base)
    draw.text((wx + 16, wy + 66), "Getting set up", fill=TEXT_MUTED, font=font_xs)

    draw.line([wx + 16, wy + 86, wx + sw - 16, wy + 86], fill=(33, 38, 45), width=3)
    fill_w = int(((step_idx + 1) / 12.0) * (sw - 32))
    draw.line([wx + 16, wy + 86, wx + 16 + fill_w, wy + 86], fill=ACCENT_CYAN, width=3)

    draw.text((wx + 16, wy + 96), f"{step_idx} of 12 steps", fill=TEXT_MUTED, font=font_xs)

    # 12 Steps List in Sidebar
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
        sy += 20

    # Right Content Area
    cx = wx + sw + 30
    cy = wy + 42
    cw = ww - sw - 60

    draw.text((cx, cy), f"Step {data['num']} of 12", fill=TEXT_MUTED, font=font_xs)
    draw.text((cx, cy + 16), data["heading"], fill=TEXT_WHITE, font=font_md)
    draw.text((cx, cy + 38), data["desc"], fill=TEXT_PRIMARY, font=font_xs)

    # STEP 2: SIDE-BY-SIDE CLUSTER SELECTOR & VERIFICATION PROBE
    if data.get("custom_box") == "cluster_side_by_side":
        cy_step2 = cy + 64
        half_w = (cw - 16) // 2

        draw.text((cx, cy_step2), "Target Cluster (Press [1-4]):", fill=TEXT_WHITE, font=font_xs)
        clusters_info = [
            ("[1] * gke_enterprise_us-central1_prod", "GKE Standard • 12 nodes (96 vCPUs) • KVM", True),
            ("[2] # aws-eks-production-us-east-1", "AWS EKS • 8 nodes (64 vCPUs) • Nitro", False),
            ("[3] # azure-aks-agent-fleet-eastus", "Azure AKS • 6 nodes (48 vCPUs) • Hyper-V", False),
            ("[4] # kind-substrate-sandbox", "Local Sandbox • 3 nodes (24 vCPUs)", False),
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
        draw.rounded_rectangle([rx, box_y, rx + half_w, box_y + 86], radius=6, fill=BG_CARD, outline=ACCENT_CYAN, width=1)
        draw.text((rx + 12, box_y + 8), "🌐 CLUSTER VERIFICATION:", fill=ACCENT_CYAN, font=font_xs)
        draw.text((rx + 12, box_y + 26), "• Provider: Google Kubernetes Engine (GKE v1.31) [✓]", fill=TEXT_WHITE, font=font_xs)
        draw.text((rx + 12, box_y + 44), "• Capacity: 12 ready nodes (KVM microVM ready)", fill=ACCENT_GREEN, font=font_xs)
        draw.text((rx + 12, box_y + 64), "• Substrate: [substrate-system] ➔ Clean Ready", fill=ACCENT_YELLOW, font=font_xs)

        chk_y = box_y + 94
        draw.rounded_rectangle([rx, chk_y, rx + half_w, chk_y + 88], radius=6, fill=BG_CMD, outline=BORDER_DARK, width=1)
        draw.text((rx + 12, chk_y + 8), "⚡ PROBE CHECKLIST:", fill=ACCENT_CYAN, font=font_xs)
        draw.text((rx + 12, chk_y + 26), "  ✓ API Reachability: Connected to active context", fill=TEXT_WHITE, font=font_xs)
        draw.text((rx + 12, chk_y + 44), "  ✓ Compatibility: Kubernetes v1.28+ verified", fill=TEXT_WHITE, font=font_xs)
        draw.text((rx + 12, chk_y + 64), "  ✓ Clean cluster ready for Substrate install", fill=ACCENT_GREEN, font=font_xs)

        by = list_y + 8

    elif data.get("custom_box") in ["nodepool_ccc", "autoscaling_hpa", "deploy_wp"]:
        # Option Selection Step (Steps 5, 6, 7)
        ey = cy + 62
        draw.text((cx, ey), "Choose configuration option (Press [1-3]):", fill=TEXT_WHITE, font=font_xs)
        ey += 18

        if data["custom_box"] == "nodepool_ccc":
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
                ("[2] # Customize WorkerPool specifications", "Review and customize memory limits, vCPU allocations, and container sandbox isolation drivers.", False),
            ]

        for o_title, o_desc, o_sel in opts:
            o_bg = ACCENT_BLUE if o_sel else BG_CMD
            o_out = ACCENT_CYAN if o_sel else BORDER_SUBTLE
            draw.rounded_rectangle([cx, ey, cx + cw, ey + 38], radius=6, fill=o_bg, outline=o_out, width=1)
            draw.text((cx + 10, ey + 5), o_title, fill=TEXT_WHITE, font=font_xs)
            draw.text((cx + 10, ey + 21), o_desc, fill=(211, 227, 253) if o_sel else TEXT_MUTED, font=font_xs)
            ey += 44

        if data.get("yaml_notice"):
            draw.rounded_rectangle([cx, ey, cx + cw, ey + 26], radius=4, fill=(25, 28, 20), outline=ACCENT_YELLOW, width=1)
            draw.text((cx + 10, ey + 6), data["yaml_notice"], fill=ACCENT_YELLOW, font=font_xs)
            ey += 32

        # Checklist
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

    else:
        # Other Steps (1, 3, 4, 8, 9, 10, 11, 12)
        cby = cy + 62
        draw.rounded_rectangle([cx, cby, cx + cw, cby + 52], radius=8, fill=BG_CMD, outline=BORDER_SUBTLE, width=1)
        draw.rounded_rectangle([cx + 12, cby + 6, cx + 180, cby + 22], radius=4, fill=ACCENT_BLUE)
        draw.text((cx + 18, cby + 7), "▼ Show the real command", fill=TEXT_WHITE, font=font_xs)
        draw.text((cx + 14, cby + 30), data["cmd"], fill=ACCENT_CYAN, font=font_sm)

        ey = cby + 60
        if data.get("custom_box") == "agreement":
            draw.rounded_rectangle([cx, ey, cx + cw, ey + 64], radius=6, fill=(25, 28, 20), outline=ACCENT_YELLOW, width=1)
            draw.text((cx + 14, ey + 8), "[!] PRIVATE GA GATED REGISTRATION & CONTRACTUAL AGREEMENT:", fill=ACCENT_YELLOW, font=font_xs)
            draw.text((cx + 14, ey + 24), "Customer: Acme Corp (rajithal@enterprise.com) │ Token: ga-sub-8f92a-live-contract [✓]", fill=TEXT_WHITE, font=font_xs)
            draw.text((cx + 14, ey + 42), "[✓] I acknowledge that production support requires an explicit agreement with Google Cloud.", fill=ACCENT_CYAN, font=font_xs)
            ey += 72

        card_h = 160 if "benchmark" in data or data["num"] == 12 else 200
        draw.rounded_rectangle([cx, ey, cx + cw, ey + card_h], radius=8, fill=BG_CARD, outline=BORDER_DARK, width=1)
        draw.text((cx + 20, ey + 10), data["chk_title"], fill=ACCENT_CYAN, font=font_sm)

        iy = ey + 28
        for item in data["chk_items"]:
            draw.text((cx + 20, iy), "✓", fill=ACCENT_GREEN, font=font_sm)
            draw.text((cx + 40, iy), item, fill=TEXT_WHITE, font=font_xs)
            iy += 20

        draw.text((cx + 20, iy + 4), data["done"], fill=ACCENT_GREEN if data["num"] < 12 else ACCENT_CYAN, font=font_base)
        draw.text((cx + 20, iy + 22), data["prompt"], fill=TEXT_PRIMARY, font=font_xs)

        vy = ey + card_h + 8
        if "benchmark" in data:
            draw.rounded_rectangle([cx, vy, cx + cw, vy + 34], radius=6, fill=BG_CMD, outline=BORDER_SUBTLE, width=1)
            draw.text((cx + 14, vy + 9), f"⚡ BENCHMARK: {data['benchmark']}", fill=ACCENT_GREEN, font=font_xs)
            by = vy + 42
        elif data["num"] == 12:
            draw.rounded_rectangle([cx, vy, cx + cw, vy + 38], radius=6, fill=BG_CMD, outline=BORDER_SUBTLE, width=1)
            draw.text((cx + 14, vy + 5), "$ atectl get workerpools", fill=ACCENT_CYAN, font=font_xs)
            draw.text((cx + 14, vy + 20), "production-fleet  substrate-system  microvm  20/20  3  4%  8%  0", fill=ACCENT_GREEN, font=font_xs)
            by = vy + 46
        else:
            by = ey + card_h + 10

    # Action Button Row
    draw.rounded_rectangle([cx + cw - 380, by, cx + cw - 290, by + 32], radius=6, fill=BG_CMD, outline=BORDER_SUBTLE, width=1)
    draw.text((cx + cw - 365, by + 8), "← Back [b]", fill=TEXT_PRIMARY, font=font_xs)

    draw.rounded_rectangle([cx + cw - 280, by, cx + cw, by + 32], radius=6, fill=ACCENT_BLUE, outline=ACCENT_CYAN, width=1)
    draw.text((cx + cw - 265, by + 8), data["btn"], fill=TEXT_WHITE, font=font_xs)

    return img


def generate_demo_video(output_path="demos/onboarding-tui/onboarding_demo.mp4"):
    print(f"🎬 Generating HD Demo Video: {output_path}...")
    writer = imageio.get_writer(output_path, fps=FPS, codec="libx264", quality=8)

    num_welcome_frames = int(3.0 * FPS)
    for f in range(num_welcome_frames):
        progress = min(1.0, (f + 1) / (FPS * 1.5))
        w_img = render_welcome_screen(typewriter_progress=progress)
        writer.append_data(np.array(w_img))

    durations = [2.0, 2.8, 2.2, 2.0, 2.5, 2.5, 2.2, 2.0, 2.2, 2.5, 2.5, 3.0]
    for i in range(12):
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

    for i in range(12):
        fname = f"step{i+1}_{STEPS_DATA[i]['title'].lower().replace(' ', '_').replace('&', 'and')}.png"
        img = render_step_frame(i)
        img.save(os.path.join(out_dir, fname))
        print(f"  ✓ Saved {fname}")


if __name__ == "__main__":
    export_step_screenshots()
    generate_demo_video()
