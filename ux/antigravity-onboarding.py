#!/usr/bin/env python3
import os
import sys
import time
import random
import threading

# Standard ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"

# Foreground Colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright Foreground Colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Global flags
NON_INTERACTIVE = False

def typewriter_print(text, delay=0.015, color=WHITE, bold=False, indent=""):
    """Prints text with a typewriter effect, supporting color and bold formatting."""
    sys.stdout.write(indent)
    if bold:
        sys.stdout.write(BOLD)
    sys.stdout.write(color)
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if not NON_INTERACTIVE:
            time.sleep(delay)
    
    sys.stdout.write(RESET + "\n")
    sys.stdout.flush()

class Spinner:
    """An elegant terminal progress spinner."""
    def __init__(self, message="Loading...", color=CYAN):
        self.message = message
        self.color = color
        self._running = False
        self._thread = None
        self.chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def _spin(self):
        idx = 0
        while self._running:
            char = self.chars[idx % len(self.chars)]
            sys.stdout.write(f"\r {self.color}{char}{RESET} {self.message}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.08)

    def start(self):
        self._running = True
        if NON_INTERACTIVE:
            sys.stdout.write(f" {self.color}* {RESET} {self.message}...\n")
            sys.stdout.flush()
            return
        self._thread = threading.Thread(target=self._spin)
        self._thread.daemon = True
        self._thread.start()

    def stop(self, success=True, custom_message=None):
        self._running = False
        if self._thread:
            self._thread.join()
        
        # Clear line
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
        
        status_symbol = f"{GREEN}✔{RESET}" if success else f"{RED}✘{RESET}"
        final_msg = custom_message if custom_message else self.message
        sys.stdout.write(f" {status_symbol} {final_msg}\n")
        sys.stdout.flush()

def draw_banner():
    banner = r"""
    _   _  _ _____ ___ ___ ___   _  _   _ ___ _______   __
   /_\ | \| |_   _|_ _/ __| _ \ /_\ \ \ / /_ _|_   _\ \ / /
  / _ \| .` | | |  | | (_ |   // _ \ \ V / | |  | |  \ V / 
 /_/ \_\_|\_| |_| |___\___|_|_|_/ \_\ \_/ |___| |_|   |_|  
                                                           """
    print(BRIGHT_CYAN + banner + RESET)
    print(f"   {BRIGHT_GREEN}⚡ Agent Substrate Onboarding • High-Density Infrastructure ⚡{RESET}")

def clear_screen():
    if not NON_INTERACTIVE:
        os.system('clear' if os.name == 'posix' else 'cls')

def get_input(prompt, choices=None, default=None):
    """Safely gets user input, supporting non-interactive fallbacks."""
    if NON_INTERACTIVE:
        val = default if default is not None else (choices[0] if choices else "")
        print(f"{prompt} {BRIGHT_GREEN}{val} {DIM}(auto){RESET}")
        return val

    choice_str = f" [{'/'.join(choices)}]" if choices else ""
    default_str = f" (default: {default})" if default else ""
    
    while True:
        try:
            sys.stdout.write(f"{prompt}{choice_str}{default_str}: ")
            sys.stdout.flush()
            user_val = input().strip()
            if not user_val and default is not None:
                return default
            if choices and user_val not in choices:
                print(f"{RED}Invalid option. Please choose from {choices}{RESET}")
                continue
            return user_val
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}Onboarding aborted.{RESET}")
            sys.exit(1)

def animate_progress(message, duration=2.0):
    """Draws a beautiful high-fidelity progress bar."""
    steps = 40
    step_duration = duration / steps
    sys.stdout.write(f" {CYAN}ℹ{RESET} {message}\n")
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        filled = int((i / steps) * 30)
        empty = 30 - filled
        bar = f"{BRIGHT_GREEN}█{RESET}" * filled + f"{DIM}░{RESET}" * empty
        sys.stdout.write(f"\r  [{bar}] {percent}%")
        sys.stdout.flush()
        if not NON_INTERACTIVE:
            time.sleep(step_duration)
    sys.stdout.write("\n\n")
    sys.stdout.flush()

def main():
    global NON_INTERACTIVE
    
    # Enable non-interactive mode if running inside a script or if --headless is passed
    if len(sys.argv) > 1 and sys.argv[1] in ["--headless", "--non-interactive", "-y"]:
        NON_INTERACTIVE = True
    elif not sys.stdin.isatty():
        NON_INTERACTIVE = True

    clear_screen()
    draw_banner()
    print()
    
    # Meet Newton - The Flight Companion
    typewriter_print("Newton: 👋 Hey there, pilot! Welcome to Antigravity.", color=BRIGHT_YELLOW, bold=True)
    typewriter_print("Newton: I'm your onboarding flight companion. Today, we are setting up", color=BRIGHT_YELLOW)
    typewriter_print("        your Agent Substrate on Google Kubernetes Engine (GKE).", color=BRIGHT_YELLOW)
    typewriter_print("        Let's deploy some high-density, sub-second suspend/resume agent sandbox infrastructure!", color=BRIGHT_YELLOW)
    print(f"{DIM}--------------------------------------------------------------------------------{RESET}\n")

    # --- STEP 1: CONTEXT & CLUSTER CHECK ---
    typewriter_print("STEP 1: GKE Cluster Connection Check", color=BRIGHT_BLUE, bold=True)
    typewriter_print("Analyzing your local environment and local Kubernetes configuration...", color=BRIGHT_BLACK)
    
    s1 = Spinner("Scanning kubecontext for active GKE clusters")
    s1.start()
    time.sleep(1.2 if not NON_INTERACTIVE else 0.1)
    s1.stop(success=True, custom_message="Scan complete. Located 3 GKE Cluster contexts:")

    print(f"\n  {DIM}[1]{RESET} gke-prod-us-central1-c  {DIM}(120 Nodes, production, nested-virtualization enabled){RESET}")
    print(f"  {DIM}[2]{RESET} gke-dev-regional         {DIM}(12 Nodes, development, nested-virtualization enabled){RESET}")
    print(f"  {DIM}[3]{RESET} staging-aurora          {DIM}(4 Nodes, testing, non-nested compute){RESET}\n")

    cluster_choice = get_input("Newton: Select a target cluster index to proceed with the Antigravity setup", choices=["1", "2", "3"], default="2")
    
    cluster_names = {
        "1": "gke-prod-us-central1-c",
        "2": "gke-dev-regional",
        "3": "staging-aurora"
    }
    selected_cluster = cluster_names[cluster_choice]
    
    typewriter_print(f"\nNewton: Great choice! Directing Antigravity targeting {BRIGHT_CYAN}{selected_cluster}{RESET}.", color=BRIGHT_YELLOW)
    if cluster_choice == "3":
        typewriter_print("Newton: ⚠️  Note: staging-aurora does not support nested virtualization. We will fallback to", color=BRIGHT_RED)
        typewriter_print("        gVisor userspace syscall interception for tenant isolation instead of Cloud Hypervisor.", color=BRIGHT_RED)
    else:
        typewriter_print("Newton: Nested virtualization is supported on this cluster! We will use Cloud Hypervisor (CHV)", color=BRIGHT_GREEN)
        typewriter_print("        for hardware-virtualized microVM isolation. Peak security and peak speed! 🚀", color=BRIGHT_GREEN)
    
    print()

    # --- STEP 2: INSTALL CORE SUBSTRATE ---
    typewriter_print("STEP 2: Bootstrapping Agent Substrate Core Controllers", color=BRIGHT_BLUE, bold=True)
    typewriter_print("Installing the open-source Substrate CLI ('atectl') and core orchestrators.", color=BRIGHT_BLACK)
    print()

    s2 = Spinner("Downloading atectl CLI binary (v0.9.2-beta)...")
    s2.start()
    time.sleep(1.0 if not NON_INTERACTIVE else 0.1)
    s2.stop(success=True, custom_message="atectl CLI successfully installed to /usr/local/bin/atectl")

    s3 = Spinner("Registering Kubernetes Custom Resource Definitions (CRDs)...")
    s3.start()
    time.sleep(0.8 if not NON_INTERACTIVE else 0.1)
    # List the CRDs being registered
    crds = ["workerpools.ate.dev", "actortemplates.ate.dev", "actors.ate.dev"]
    s3.stop(success=True, custom_message=f"Registered CRDs: {', '.join([BRIGHT_MAGENTA + c + RESET for c in crds])}")

    s4 = Spinner("Installing Substrate Data Plane and eBPF network interceptors...")
    s4.start()
    time.sleep(1.2 if not NON_INTERACTIVE else 0.1)
    s4.stop(success=True, custom_message="eBPF high-speed routing data plane successfully active.")

    print()

    # --- STEP 3: PROVISION WORKER POOL (GAMIFIED MAP) ---
    typewriter_print("STEP 3: Provisioning Your Worker Pool", color=BRIGHT_BLUE, bold=True)
    typewriter_print("A Worker Pool consists of pre-warmed Kubernetes pods ('Workers') running on GKE nodes.", color=BRIGHT_BLACK)
    typewriter_print("They sit in a standby, pre-initialized state waiting to inject active agent sessions ('Actors').", color=BRIGHT_BLACK)
    print()

    isolation_type = "microvm" if cluster_choice != "3" else "gvisor"
    
    typewriter_print(f"Newton: Let's create your first Worker Pool using `atectl`.", color=BRIGHT_YELLOW)
    typewriter_print(f"        I recommend provisioning with a 10% warm standby capacity buffer to prevent allocation lag.", color=BRIGHT_YELLOW)
    
    capacity_str = get_input("Newton: How many target concurrent worker instances do you want to allocate?", default="50")
    capacity = int(capacity_str)

    print(f"\nExecuting Command:")
    print(f"  {BRIGHT_WHITE}$ atectl create workerpool main-pool \\{RESET}")
    print(f"      {BRIGHT_WHITE}--isolation={isolation_type} \\{RESET}")
    print(f"      {BRIGHT_WHITE}--workers={capacity} \\{RESET}")
    print(f"      {BRIGHT_WHITE}--min-cpus=2 --min-memory=2GiB \\{RESET}")
    print(f"      {BRIGHT_WHITE}--autoscale --buffer-ratio=0.10{RESET}\n")

    s5 = Spinner("GKE allocating GCE nodes & spinning up Worker Pods...")
    s5.start()
    time.sleep(1.0 if not NON_INTERACTIVE else 0.1)
    s5.stop(success=True, custom_message="Node pool scaled up. Initializing pre-warmed sandbox sandboxes:")

    # Map simulation of the pre-warming cluster pods (Revealing the Map UX)
    print(f"\n  {BOLD}Worker Pool Pre-Warming Topology Map:{RESET}")
    
    grid_size = min(capacity, 100)
    cols = 20
    rows = (grid_size + cols - 1) // cols
    
    # Animate state transition of workers in real time
    states = ["⚙"] * grid_size  # Initializing
    
    for cycle in range(3):
        if NON_INTERACTIVE:
            break
        # Print grid
        sys.stdout.write("\033[F" * (rows + 1))
        sys.stdout.write("\033[J")
        
        # update states
        for i in range(grid_size):
            r = random.random()
            if cycle == 0:
                states[i] = f"{YELLOW}⚙{RESET}" if r < 0.5 else f"{RED}░{RESET}"
            elif cycle == 1:
                states[i] = f"{BRIGHT_GREEN}░{RESET}" if r < 0.6 else f"{YELLOW}⚙{RESET}"
            else:
                states[i] = f"{GREEN}█{RESET}" if r < 0.9 else f"{BRIGHT_GREEN}░{RESET}"
                
        # Draw grid
        for r_idx in range(rows):
            row_str = "   "
            for c_idx in range(cols):
                idx = r_idx * cols + c_idx
                if idx < grid_size:
                    row_str += f"[{states[idx]}] "
            print(row_str)
        print(f"   {DIM}Progress: {int((cycle+1)/3*100)}% Pre-warmed{RESET}")
        sys.stdout.flush()
        time.sleep(0.7)

    # Final fully warmed output
    if not NON_INTERACTIVE:
        sys.stdout.write("\033[F" * (rows + 1))
        sys.stdout.write("\033[J")
    
    # 100% warmed up
    for r_idx in range(rows):
        row_str = "   "
        for c_idx in range(cols):
            idx = r_idx * cols + c_idx
            if idx < grid_size:
                row_str += f"[{BRIGHT_GREEN}█{RESET}] "
        print(row_str)
    print(f"   {BRIGHT_GREEN}✔ 100% Warmed up. Capacity available: {capacity} pre-warmed idle worker pods.{RESET}\n")

    typewriter_print(f"Newton: Magnificent! Our worker pools are sitting completely idle, cost-optimized,", color=BRIGHT_YELLOW)
    typewriter_print(f"        and holding zero process state, waiting for the first agent activation.", color=BRIGHT_YELLOW)
    print()

    # --- STEP 4: CREATE TEMPLATE & TEST SUSPEND/RESUME ---
    typewriter_print("STEP 4: Deploying Your First Agent Actor Template", color=BRIGHT_BLUE, bold=True)
    typewriter_print("We will define an Actor Template which encapsulates the agent OCI image.", color=BRIGHT_BLACK)
    print()

    print(f"Executing Command:")
    print(f"  {BRIGHT_WHITE}$ atectl create template coder-agent \\{RESET}")
    print(f"      {BRIGHT_WHITE}--image=gcr.io/antigravity/coder-agent:v1.0.0 \\{RESET}")
    print(f"      {BRIGHT_WHITE}--worker-pool=main-pool{RESET}\n")

    s6 = Spinner("Registering 'coder-agent' Actor Template...")
    s6.start()
    time.sleep(0.8 if not NON_INTERACTIVE else 0.1)
    s6.stop(success=True, custom_message="ActorTemplate 'coder-agent' registered. Version: v1alpha1.v1")

    print()
    typewriter_print("Newton: Let's run a speed test! We will instantiate an Actor, execute", color=BRIGHT_YELLOW)
    typewriter_print("        a quick command, suspend it to disk, and then wake it up.", color=BRIGHT_YELLOW)
    typewriter_print("        Watch the latency closely. Real-time UX is what we live for!", color=BRIGHT_YELLOW)
    print()

    s7 = Spinner("Waking up new Actor 'test-session-77' (Cold Start / Clean Boot)...")
    s7.start()
    time.sleep(1.2 if not NON_INTERACTIVE else 0.1)
    s7.stop(success=True, custom_message=f"Actor 'test-session-77' initialized. Latency: {BRIGHT_YELLOW}912ms{RESET} (Image layers pulled & mounted)")

    s8 = Spinner("Executing test workload inside sandbox...")
    s8.start()
    time.sleep(0.5 if not NON_INTERACTIVE else 0.1)
    s8.stop(success=True, custom_message="Workload executed. Returned: 'Hello from Antigravity Agent Substrate!'")

    s9 = Spinner("Sending idle signal. Suspending actor state to GCS snapshot L2...")
    s9.start()
    time.sleep(0.8 if not NON_INTERACTIVE else 0.1)
    s9.stop(success=True, custom_message=f"State snapshotted. CPU/Memory fully reclaimed. Latency: {BRIGHT_GREEN}42ms{RESET}")

    s10 = Spinner("Triggering invocation. Resuming actor 'test-session-77' from warm cache...")
    s10.start()
    time.sleep(0.6 if not NON_INTERACTIVE else 0.1)
    latency = random.randint(110, 165)
    s10.stop(success=True, custom_message=f"Actor resumed in {BRIGHT_GREEN}{latency}ms{RESET}! (L1 Local SSD snapshot cache hit!)")

    print()

    # --- STEP 5: PROGRESSIVE DISCLOSURE (CODE INTEGRATION) ---
    typewriter_print("STEP 5: Platform Integration (How to build on me)", color=BRIGHT_BLUE, bold=True)
    typewriter_print("Integration is simple! In your platform backend or agent harness code,", color=BRIGHT_BLACK)
    typewriter_print("you will invoke the REST/gRPC endpoint and send turn-completion signals.", color=BRIGHT_BLACK)
    print()

    print(f"  {DIM}=== Python Integration Snippet ==={RESET}")
    print(f"""  {BRIGHT_WHITE}import requests

  # 1. Instantiate or Resume Actor session on onboarding / prompt
  actor_id = "user-alice-session"
  response = requests.post(
      f"https://api.substrate.gke/v1/atespaces/default/actors/{{actor_id}}/execute",
      json={{"prompt": "Refactor app/main.py to include custom routing"}}
  )
  print("Agent result:", response.json()["output"])

  # 2. Tell Substrate the turn is complete to trigger instant suspend (save $$$)
  requests.post(
      f"https://api.substrate.gke/v1/atespaces/default/actors/{{actor_id}}/idle"
  ){RESET}""")
    print(f"  {DIM}=================================={RESET}\n")

    typewriter_print("Newton: Easy, right? Under the hood, Substrate intercepts the '/idle' call,", color=BRIGHT_YELLOW)
    typewriter_print("        checkpoints the container filesystem, saves the snapshot to GCS,", color=BRIGHT_YELLOW)
    typewriter_print("        and releases the worker back to the pool in milliseconds. High density!", color=BRIGHT_YELLOW)
    print()

    # --- SUCCESS OUTRO ---
    print(f"{DIM}--------------------------------------------------------------------------------{RESET}")
    typewriter_print("🎉 ONBOARDING JOURNEY SUCCESSFUL!", color=BRIGHT_GREEN, bold=True)
    typewriter_print("Newton: You are now fully certified to build, scale, and pilot agent workloads", color=BRIGHT_GREEN)
    typewriter_print("        on Antigravity x GKE Substrate. Your unit economics just got a 10X upgrade!", color=BRIGHT_GREEN)
    print()
    print(f"  {BOLD}Top Cheat-Sheet Commands:{RESET}")
    print(f"    • {CYAN}atectl status{RESET}              Show overall cluster and registry state.")
    print(f"    • {CYAN}atectl top workers{RESET}         Monitor memory overcommit and cache saturation.")
    print(f"    • {CYAN}atectl list actors{RESET}         List active and suspended sessions.")
    print(f"    • {CYAN}atectl logs <actor-id>{RESET}    Retrieve real-time telemetry spans and logs.")
    print()
    typewriter_print("Newton: Over and out, captain. May your latencies be low and your scale be high! 🚀📡", color=BRIGHT_YELLOW, bold=True)
    print()

if __name__ == "__main__":
    main()
