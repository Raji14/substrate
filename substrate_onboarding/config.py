"""Configuration schemas, options, and state models for Agent Substrate Onboarding.

Includes:
- Step 0: Welcome Screen (Hero ASCII Logo, Gradient Animation, Feature Highlights, Setup Tracks)
- Steps 1-8: Interactive Getting Set Up Journey:
  1. Check your setup
  2. Create a cluster
  3. Turn on Substrate
  4. Install the CLI
  5. First actor
  6. Send a request
  7. Pause & resume
  8. Scale it up
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class OnboardingStep(str, Enum):
    WELCOME = "welcome"                  # Step 0: Welcome & Setup Track Selection
    CHECK_SETUP = "check_setup"          # Step 1: Check your setup
    CREATE_CLUSTER = "create_cluster"    # Step 2: Create a cluster
    TURN_ON_SUBSTRATE = "turn_on_sub"    # Step 3: Turn on Substrate
    INSTALL_CLI = "install_cli"          # Step 4: Install the CLI
    FIRST_ACTOR = "first_actor"          # Step 5: First actor
    SEND_REQUEST = "send_request"        # Step 6: Send a request
    PAUSE_RESUME = "pause_resume"        # Step 7: Pause & resume
    SCALE_UP = "scale_up"                # Step 8: Scale it up
    COMPLETE = "complete"

    # Backward compatibility aliases
    CLUSTER = "check_setup"
    CONTROL_PLANE = "create_cluster"
    NODE_POOL = "turn_on_sub"
    AUTOSCALING = "install_cli"
    DEPLOY_WORKERPOOL = "first_actor"
    LAUNCHPAD = "scale_up"
    DOCTOR = "check_setup"
    QUESTIONNAIRE = "create_cluster"
    AUTH = "turn_on_sub"
    SUMMARY = "scale_up"


@dataclass
class OptionItem:
    id: str
    title: str
    description: str
    icon: str = "⚡"
    tip: str = ""


# Setup Tracks for Welcome Screen
SETUP_TRACKS: List[OptionItem] = [
    OptionItem(
        id="track_local_sandbox",
        title="Local Sandbox (Kind / Docker Desktop) (Recommended)",
        description="Zero cloud costs. Spins up a local Kubernetes cluster on your machine in 30 seconds.",
        icon="🧪",
        tip="Perfect for quick prototyping and local agent development.",
    ),
    OptionItem(
        id="track_gke_cluster",
        title="Google Kubernetes Engine (GKE Production Fleet)",
        description="High-density MicroVM isolation, Custom Compute Class (CCC), and Spot autoscaling.",
        icon="⚡",
        tip="For enterprise scale and production multi-tenant agent swarms.",
    ),
    OptionItem(
        id="track_custom_k8s",
        title="Custom Existing Kubernetes Cluster",
        description="Installs Substrate onto your current active kubeconfig context.",
        icon="🏢",
        tip="Uses existing nodes and namespaces.",
    ),
]

CLUSTER_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="demo_cluster_us_central1",
        title="gke_demo_project_us-central1-a_demo-cluster (Recommended)",
        description="GKE v1.31.1-gke.1520000 in us-central1-a (Target: demo-cluster)",
        icon="🌐",
        tip="Connects to primary cluster.",
    ),
    OptionItem(
        id="staging_cluster_us_west1",
        title="gke_demo_project_us-west1-b_staging-cluster",
        description="GKE v1.31.0 in us-west1-b (Target: staging-cluster)",
        icon="🧪",
        tip="Staging cluster.",
    ),
]

NODEPOOL_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="ccc_auto",
        title="Automatically create a compatible Node Pool using Custom Compute Class (Recommended)",
        description="Applies manifest (agent-spot-ccc) with n2-standard-48, Spot fallback, and nested-virt",
        icon="⚡",
        tip="Auto provisions node pool.",
    ),
]

AUTOSCALING_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="auto_hpa",
        title="Automatically configure HPA & CapacityBuffer with sensible defaults",
        description="OneHPA min=10, max=100 and fixed-replica-buffer 3 standby",
        icon="⚡",
    ),
]

DEPLOY_WP_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="deploy_yes",
        title="Yes, deploy default WorkerPool [default-worker-pool] (Recommended)",
        description="10 standby replicas, microVM sandbox isolation",
        icon="🚀",
    ),
]

TRACK_OPTIONS = SETUP_TRACKS
DATAPLANE_OPTIONS = NODEPOOL_OPTIONS
SANDBOX_OPTIONS = AUTOSCALING_OPTIONS
EDITOR_OPTIONS = DEPLOY_WP_OPTIONS


@dataclass
class StepMetadata:
    step_num: int
    title: str
    heading: str
    description: str
    real_command: str
    checklist_title: str
    checklist_items: List[str]
    done_message: str
    next_action_label: str
    benchmark_text: Optional[str] = None


STEP_CONFIGS: Dict[OnboardingStep, StepMetadata] = {
    OnboardingStep.WELCOME: StepMetadata(
        step_num=0,
        title="Welcome",
        heading="Agent Substrate — Getting Set Up",
        description="High-density sandboxing and sub-100ms runtime for autonomous AI agents on Kubernetes.",
        real_command="atectl onboard",
        checklist_title="System Readiness Check",
        checklist_items=[
            "Docker / Containerd Engine: Active",
            "Kubernetes API Connection: Verified",
            "Substrate Control Plane: Ready for install",
        ],
        done_message="Ready to begin setup! Press [Enter] to start.",
        next_action_label="Get Started (Enter) →",
    ),
    OnboardingStep.CHECK_SETUP: StepMetadata(
        step_num=1,
        title="Check your setup",
        heading="Check your environment",
        description="We'll check if you have everything needed to run Substrate locally — a container runtime, Python, and cluster tools.",
        real_command="which docker && which kubectl && which python3",
        checklist_title="Checking prerequisites...",
        checklist_items=[
            "Container runtime detected (Docker / Podman / Colima)",
            "Python 3.10+ runtime available",
            "Kubectl command utility ready in PATH",
        ],
        done_message="Everything's ready. Let's create your cluster next.",
        next_action_label="Create a cluster (Enter) →",
    ),
    OnboardingStep.CREATE_CLUSTER: StepMetadata(
        step_num=2,
        title="Create a cluster",
        heading="Create a local cluster",
        description="This spins up a small Kubernetes cluster right on your machine — a private sandbox that's fully yours.",
        real_command="hack/create-kind-cluster.sh",
        checklist_title="Creating your cluster...",
        checklist_items=[
            "Creating your local cluster",
            "Setting up a place to store container images",
            "Your cluster is up and ready",
        ],
        done_message="Cluster's ready. Now let's install Substrate itself.",
        next_action_label="Turn on Substrate (Enter) →",
    ),
    OnboardingStep.TURN_ON_SUBSTRATE: StepMetadata(
        step_num=3,
        title="Turn on Substrate",
        heading="Turn on Substrate Control Plane",
        description="Installing the Substrate core controllers, state registry, and high-speed networking into your cluster.",
        real_command="kubectl apply -f manifests/substrate-control-plane.yaml",
        checklist_title="Installing Substrate components...",
        checklist_items=[
            "Applying CustomResourceDefinitions (WorkerPool, ActorTemplate, Actor)",
            "Deploying Valkey Metadata & State Registry",
            "Bootstrapping Substrate Gateway & API Server (listening on :8080)",
            "Initializing eBPF network routing controller in [substrate-system]",
        ],
        done_message="Substrate is active! Next, let's install the CLI.",
        next_action_label="Install the CLI (Enter) →",
    ),
    OnboardingStep.INSTALL_CLI: StepMetadata(
        step_num=4,
        title="Install the CLI",
        heading="Install the atectl CLI",
        description="The atectl tool lets you manage actors, worker pools, and memory snapshots with simple commands — zero Kubernetes YAML required.",
        real_command="go install ./cmd/atectl || curl -sSL https://ate.dev/atectl | sh",
        checklist_title="Configuring developer CLI...",
        checklist_items=[
            "Downloading atectl binary for your architecture (macOS / Linux)",
            "Registering shell autocompletions and PATH bindings",
            "CLI verified: atectl version v0.2.1-ga",
        ],
        done_message="CLI is installed and ready. Let's deploy your first actor!",
        next_action_label="Deploy first actor (Enter) →",
    ),
    OnboardingStep.FIRST_ACTOR: StepMetadata(
        step_num=5,
        title="First actor",
        heading="Deploy your first actor",
        description="Launch an AI agent container from a standard template into a pre-warmed sandbox — no YAML manifests required.",
        real_command="atectl actor create my-first-actor --template=default-agent --atespace=default-atespace",
        checklist_title="Launching actor session...",
        checklist_items=[
            "Resolving agent container image (gcr.io/ate-platform/agent:v1)",
            "Injecting into pre-warmed worker sandbox",
            "Actor [my-first-actor] is live and listening on port 8080",
        ],
        done_message="Actor is running! Let's send it an interactive request.",
        next_action_label="Send a request (Enter) →",
    ),
    OnboardingStep.SEND_REQUEST: StepMetadata(
        step_num=6,
        title="Send a request",
        heading="Send a request to your actor",
        description="Communicate with your running actor through the Substrate Gateway with real-time response streaming.",
        real_command='atectl actor execute my-first-actor --prompt="Analyze recent logs and report status"',
        checklist_title="Streaming execution turn...",
        checklist_items=[
            "Routing turn request through Substrate Gateway",
            "Actor turn completed in 82ms (First token: 14ms)",
            'Response received: "System operating normally. 0 errors detected."',
        ],
        done_message="Great response! Now let's see how Substrate saves compute when idle.",
        next_action_label="Test Pause & Resume (Enter) →",
        benchmark_text="Turn Latency: 82ms  │  TTFT (First Token): 14ms  │  Throughput: 120 tok/s",
    ),
    OnboardingStep.PAUSE_RESUME: StepMetadata(
        step_num=7,
        title="Pause & resume",
        heading="Pause & resume (0% idle CPU)",
        description="When agents are idle waiting for human input, Substrate checkpoints their memory to disk to save 90% compute, waking them in under 200ms.",
        real_command="atectl actor suspend my-first-actor && atectl actor resume my-first-actor",
        checklist_title="Testing data plane suspend/resume...",
        checklist_items=[
            "Suspending idle actor memory state to disk (38ms, CPU drops to 0%)",
            "Request parking held incoming user message in queue",
            "Restoring actor memory state on wake event in 115ms",
        ],
        done_message="Sub-200ms instant resume confirmed! Finally, let's scale your fleet.",
        next_action_label="Scale it up (Enter) →",
        benchmark_text="Cold Start (890ms)  ➔  Suspend (38ms, 0% CPU)  ➔  Warm Resume (115ms)",
    ),
    OnboardingStep.SCALE_UP: StepMetadata(
        step_num=8,
        title="Scale it up",
        heading="Scale worker fleet & Day-2 Operations",
        description="Scale worker pools with pre-warmed standby capacity buffers so your agent swarms are always ready for traffic spikes.",
        real_command="atectl create workerpools production-fleet --workers=20 --isolation=microvm",
        checklist_title="Scaling worker pool capacity...",
        checklist_items=[
            "Worker pool [production-fleet] scaled to 20 warm pods",
            "Standby CapacityBuffer configured (3 warm spares ready)",
            "Live inspection verified: atectl get workerpools (Ready: 20/20)",
        ],
        done_message="You're all set! Enjoy building high-density AI agents with Agent Substrate.",
        next_action_label="🚀 Finish Onboarding (Enter)",
    ),
}


@dataclass
class CheckResult:
    name: str
    category: str = "System"
    status: str = "pending"
    message: str = ""
    details: Optional[str] = None
    fix_command: Optional[str] = None
    doc_url: Optional[str] = "https://ate.dev/docs/prereqs"
    plain_description: Optional[str] = None
    duration_ms: int = 0
    is_fatal: bool = False
    is_critical: bool = False


@dataclass
class UserSetupState:
    current_step: OnboardingStep = OnboardingStep.WELCOME
    selected_track: str = "track_local_sandbox"
    selected_cluster: str = "local-sandbox"
    is_complete: bool = False
