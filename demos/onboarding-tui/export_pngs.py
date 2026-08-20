"""Export high-resolution PNG snapshots of all onboarding steps from the HD renderer."""

import os
import sys
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import importlib.util
spec = importlib.util.spec_from_file_location("generate_video", os.path.join(os.path.dirname(__file__), "generate_video.py"))
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
BRAIN_DIR = "/Users/rajithal/.gemini/jetski/brain/edded676-c356-45e5-9ba5-0cd978ce709a"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

scenes = [
    ("step0_welcome.png", gv.render_scene_1_welcome(110, 120)),
    ("step1_preflight_doctor.png", gv.render_scene_3_doctor(85)),
    ("step2_platform_setup.png", gv.render_scene_2_wizard(substep=0, selected_idx=0, frame_idx=69)),
    ("step3_agent_deployment.png", gv.render_scene_4_auth(frame_idx=140)),
    ("step4_cluster_launchpad.png", gv.render_scene_5_launchpad(progress_pct=100.0, show_celebration=True, frame_idx=170)),
    ("step5_help_modal.png", gv.render_scene_6_help_modal(frame_idx=110)),
]

print("Generating high-res PNG screenshots:")
for filename, arr in scenes:
    img = Image.fromarray(arr)
    out_path = os.path.join(OUTPUT_DIR, filename)
    brain_path = os.path.join(BRAIN_DIR, filename)
    img.save(out_path, "PNG")
    img.save(brain_path, "PNG")
    print(f"  ✓ Saved {out_path} and {brain_path}")

print("\nAll PNG screenshots generated successfully!")
