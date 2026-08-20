"""High-Definition (720p/1080p) Video Recording Generator for Agent Substrate 8-Step Onboarding.

Renders each of the 8 steps matching the exact screenshot layout:
- Left Sidebar: Substrate, Getting set up, progress line, X of 8 steps, 8 steps list.
- Right Area: Step X of 8, heading, description, 'Show the real command' callout, execution checklist, and Done state.
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

# Colors matching screenshot
BG_CANVAS = (9, 13, 22)           # #090d16
BG_CONTENT = (13, 17, 23)         # #0d1117
BG_CARD = (9, 13, 22)             # #090d16
BG_CMD = (17, 21, 28)             # #11151c
BORDER_DARK = (33, 38, 45)        # #21262d
BORDER_SUBTLE = (48, 54, 61)      # #30363d

ACCENT_CYAN = (112, 214, 255)     # #70d6ff
ACCENT_BLUE = (21, 101, 192)      # #1565c0
ACCENT_GREEN = (129, 201, 149)    # #81c995

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

STEPS_DATA = [
    {
        "num": 1,
        "title": "Check your setup",
        "heading": "Check your environment",
        "desc": "We'll check if you have everything needed to run Substrate locally — a container runtime, Python, and cluster tools.",
        "cmd": "which docker && which kubectl && which python3",
        "chk_title": "Checking prerequisites...",
        "chk_items": [
            "Container runtime detected (Docker / Podman / Colima)",
            "Python 3.10+ runtime available",
            "Kubectl command utility ready in PATH",
        ],
        "done": "Done",
        "prompt": "Everything's ready. Let's create your cluster next.",
        "btn": "Create a cluster (Enter) →",
    },
    {
        "num": 2,
        "title": "Create a cluster",
        "heading": "Create a local cluster",
        "desc": "This spins up a small Kubernetes cluster right on your machine — a private sandbox that's fully yours.",
        "cmd": "hack/create-kind-cluster.sh",
        "chk_title": "Creating your cluster...",
        "chk_items": [
            "Creating your local cluster",
            "Setting up a place to store container images",
            "Your cluster is up and ready",
        ],
        "done": "Done",
        "prompt": "Cluster's ready. Now let's install Substrate itself.",
        "btn": "Turn on Substrate (Enter) →",
    },
    {
        "num": 3,
        "title": "Turn on Substrate",
        "heading": "Turn on Substrate Control Plane",
        "desc": "Installing the Substrate core controllers, state registry, and high-speed networking into your cluster.",
        "cmd": "kubectl apply -f manifests/substrate-control-plane.yaml",
        "chk_title": "Installing Substrate components...",
        "chk_items": [
            "Applying CustomResourceDefinitions (WorkerPool, ActorTemplate, Actor)",
            "Deploying Valkey Metadata & State Registry",
            "Bootstrapping Substrate Gateway & API Server (listening on :8080)",
            "Initializing eBPF network routing controller in [substrate-system]",
        ],
        "done": "Done",
        "prompt": "Substrate is active! Next, let's install the CLI.",
        "btn": "Install the CLI (Enter) →",
    },
    {
        "num": 4,
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
        "btn": "Deploy first actor (Enter) →",
    },
    {
        "num": 5,
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
        "btn": "Send a request (Enter) →",
    },
    {
        "num": 6,
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
        "btn": "Test Pause & Resume (Enter) →",
    },
    {
        "num": 7,
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
        "btn": "Scale it up (Enter) →",
    },
    {
        "num": 8,
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
        "btn": "Finish Onboarding (Enter)",
    },
]


def render_step_frame(step_idx=1):
    data = STEPS_DATA[step_idx]
    img = Image.new("RGB", (WIDTH, HEIGHT), (9, 13, 22))
    draw = ImageDraw.Draw(img)

    wx, wy, ww, wh = 80, 40, 1120, 640
    # Window shell
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=10, fill=BG_CONTENT, outline=BORDER_DARK, width=1)

    # Titlebar
    draw.rectangle([wx, wy, wx + ww, wy + 34], fill=BG_CANVAS)
    draw.line([wx, wy + 34, wx + ww, wy + 34], fill=BORDER_DARK, width=1)
    draw.ellipse([wx + 14, wy + 12, wx + 24, wy + 22], fill=(255, 95, 86))
    draw.ellipse([wx + 30, wy + 12, wx + 40, wy + 22], fill=(255, 189, 46))
    draw.ellipse([wx + 46, wy + 12, wx + 56, wy + 22], fill=(39, 201, 63))
    draw.text((wx + 360, wy + 10), "broyal@broyal: ~/workspaces/ate-demos/demos — substrate onboard", fill=TEXT_MUTED, font=font_xs)

    # Left Sidebar (width 240)
    sw = 240
    draw.rectangle([wx, wy + 35, wx + sw, wy + wh], fill=BG_CANVAS)
    draw.line([wx + sw, wy + 35, wx + sw, wy + wh], fill=BORDER_DARK, width=1)

    # Sidebar Header
    draw.text((wx + 20, wy + 55), "Substrate", fill=ACCENT_CYAN, font=font_base)
    draw.text((wx + 20, wy + 75), "Getting set up", fill=TEXT_MUTED, font=font_sm)

    # Progress Line
    draw.line([wx + 20, wy + 105, wx + sw - 20, wy + 105], fill=(33, 38, 45), width=3)
    fill_w = int(((step_idx + 1) / 8.0) * (sw - 40))
    draw.line([wx + 20, wy + 105, wx + 20 + fill_w, wy + 105], fill=ACCENT_CYAN, width=3)

    draw.text((wx + 20, wy + 120), f"{step_idx} of 8 steps", fill=TEXT_MUTED, font=font_xs)

    # 8 Steps List
    sy = wy + 150
    for i, s in enumerate(STEPS_DATA):
        num = i + 1
        if i < step_idx:
            draw.text((wx + 20, sy), "✓", fill=ACCENT_GREEN, font=font_sm)
            draw.text((wx + 38, sy), s["title"], fill=TEXT_PRIMARY, font=font_sm)
        elif i == step_idx:
            draw.text((wx + 20, sy), str(num), fill=ACCENT_CYAN, font=font_sm)
            draw.text((wx + 38, sy), s["title"], fill=ACCENT_CYAN, font=font_sm)
        else:
            draw.text((wx + 20, sy), str(num), fill=TEXT_DIM, font=font_sm)
            draw.text((wx + 38, sy), s["title"], fill=TEXT_DIM, font=font_sm)
        sy += 28

    # Right Content Area
    cx = wx + sw + 36
    cy = wy + 55
    cw = ww - sw - 72

    draw.text((cx, cy), f"Step {data['num']} of 8", fill=TEXT_MUTED, font=font_xs)
    draw.text((cx, cy + 18), data["heading"], fill=TEXT_WHITE, font=font_md)
    draw.text((cx, cy + 46), data["desc"], fill=TEXT_PRIMARY, font=font_sm)

    # Collapsible Command Box
    cby = cy + 86
    draw.rounded_rectangle([cx, cby, cx + cw, cby + 68], radius=8, fill=BG_CMD, outline=BORDER_SUBTLE, width=1)
    # Blue pill badge
    draw.rounded_rectangle([cx + 12, cby + 10, cx + 180, cby + 28], radius=4, fill=ACCENT_BLUE)
    draw.text((cx + 18, cby + 12), "▼ Show the real command", fill=TEXT_WHITE, font=font_xs)
    draw.text((cx + 14, cby + 40), data["cmd"], fill=ACCENT_CYAN, font=font_sm)

    # Execution Checklist Card
    ey = cby + 86
    draw.rounded_rectangle([cx, ey, cx + cw, ey + 240], radius=8, fill=BG_CARD, outline=BORDER_DARK, width=1)
    draw.text((cx + 20, ey + 18), data["chk_title"], fill=ACCENT_CYAN, font=font_sm)

    iy = ey + 48
    for item in data["chk_items"]:
        draw.text((cx + 20, iy), "✓", fill=ACCENT_GREEN, font=font_sm)
        draw.text((cx + 40, iy), item, fill=TEXT_WHITE, font=font_sm)
        iy += 30

    draw.text((cx + 20, iy + 10), data["done"], fill=ACCENT_GREEN if data["num"] < 8 else ACCENT_CYAN, font=font_base)
    draw.text((cx + 20, iy + 36), data["prompt"], fill=TEXT_PRIMARY, font=font_sm)

    # Action Button Row
    by = ey + 260
    if step_idx > 0:
        draw.rounded_rectangle([cx + cw - 360, by, cx + cw - 280, by + 34], radius=6, fill=BG_CMD, outline=BORDER_SUBTLE, width=1)
        draw.text((cx + cw - 345, by + 8), "← Back", fill=TEXT_PRIMARY, font=font_sm)

    draw.rounded_rectangle([cx + cw - 270, by, cx + cw, by + 34], radius=6, fill=ACCENT_BLUE, outline=ACCENT_CYAN, width=1)
    draw.text((cx + cw - 255, by + 8), data["btn"], fill=TEXT_WHITE, font=font_sm)

    return img


def generate_demo_video(output_path="demos/onboarding-tui/onboarding_demo.mp4"):
    print(f"🎬 Generating HD Demo Video: {output_path}...")
    writer = imageio.get_writer(output_path, fps=FPS, codec="libx264", quality=8)

    # Render each of the 8 steps
    durations = [2.2, 2.8, 2.2, 2.2, 2.2, 2.5, 2.8, 3.2]
    for i in range(8):
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
    
    for i in range(8):
        fname = f"step{i+1}_{STEPS_DATA[i]['title'].lower().replace(' ', '_')}.png"
        img = render_step_frame(i)
        img.save(os.path.join(out_dir, fname))
        print(f"  ✓ Saved {fname}")

    # Backward compatibility copies
    render_step_frame(0).save(os.path.join(out_dir, "step0_welcome.png"))
    render_step_frame(0).save(os.path.join(out_dir, "step1_preflight_doctor.png"))
    render_step_frame(1).save(os.path.join(out_dir, "step2_platform_setup.png"))
    render_step_frame(4).save(os.path.join(out_dir, "step3_agent_deployment.png"))
    render_step_frame(7).save(os.path.join(out_dir, "step4_cluster_launchpad.png"))


if __name__ == "__main__":
    export_step_screenshots()
    generate_demo_video()
