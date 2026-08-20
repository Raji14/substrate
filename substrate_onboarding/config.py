"""Configuration schemas, options, and state models for Agent Substrate Onboarding.

Addresses:
1. Splash Title: "Agent Substrate" ASCII logo without duplicate subtitle.
2. Two Installation Choices:
   - [1] Quickstart: Automatic cluster detection & default configuration (Recommended)
   - [2] Advanced: Custom installation with kubectl
3. Pre-existing Cluster Requirement & Private GA Gated Agreement.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class OnboardingStep(str, Enum):
    WELCOME = "welcome"                          # Step 0: Welcome & Setup Track Selection
    CHECK_SETUP = "check_setup"                  # Step 1: Check your environment
    CONNECT_CLUSTER = "connect_cluster"          # Step 2: Connect pre-existing cluster
    PRIVATE_GA_AGREEMENT = "private_ga"          # Step 3: Private GA gated access & agreement
    TURN_ON_SUBSTRATE = "turn_on_sub"            # Step 4: Turn on Substrate Control Plane
    INSTALL_CLI = "install_cli"                  # Step 5: Install the CLI
    FIRST_ACTOR = "first_actor"                  # Step 6: First actor
    SEND_REQUEST = "send_request"                # Step 7: Send a request
    PAUSE_RESUME = "pause_resume"                # Step 8: Pause & resume
    SCALE_UP = "scale_up"                        # Step 9: Scale it up & Live Launchpad
    COMPLETE = "complete"

    # Backward compatibility aliases
    CLUSTER = "connect_cluster"
    CREATE_CLUSTER = "connect_cluster"
    CONTROL_PLANE = "turn_on_sub"
    NODE_POOL = "turn_on_sub"
    AUTOSCALING = "install_cli"
    DEPLOY_WORKERPOOL = "first_actor"
    LAUNCHPAD = "scale_up"
    DOCTOR = "check_setup"
    QUESTIONNAIRE = "connect_cluster"
    AUTH = "private_ga"
    SUMMARY = "scale_up"


@dataclass
class OptionItem:
    id: str
    title: str
    description: str
    icon: str = "⚡"
    tip: str = ""
    shortcut_key: str = "1"


# Two Streamlined Setup Tracks for Welcome Screen
SETUP_TRACKS: List[OptionItem] = [
    OptionItem(
        id="track_quickstart",
        title="Quickstart — Automatic cluster detection & default configuration (Recommended)",
        description="Automatically connects to your pre-configured cluster and applies sensible defaults in seconds.",
        icon="🚀",
        tip="Press [1] or [Enter] for 1-click automatic bootstrap.",
        shortcut_key="1",
    ),
    OptionItem(
        id="track_advanced",
        title="Advanced — Custom installation with kubectl",
        description="Customize YAML manifests, resource quotas, microVM isolation drivers, and eBPF routing rules.",
        icon="⚙️",
        tip="Press [2] for tailored manifest configuration.",
        shortcut_key="2",
    ),
]

CLUSTER_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="cluster_demo_gke",
        title="gke_enterprise_us-central1_prod-cluster (Active Context) (Recommended)",
        description="GKE v1.31.1-gke.1520000 in us-central1 (Nodes: 12 ready, CPU: 96 cores)",
        icon="🌐",
        tip="Active kubeconfig context verified.",
    ),
    OptionItem(
        id="cluster_local_kind",
        title="kind-substrate-sandbox (Local Context)",
        description="Kubernetes v1.31.0 local developer cluster (Nodes: 3 ready)",
        icon="🧪",
        tip="Local sandbox context.",
    ),
]

NODEPOOL_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="ccc_auto",
        title="Automatically configure Custom Compute Class (Recommended)",
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
    is_agreement_step: bool = False


STEP_CONFIGS: Dict[OnboardingStep, StepMetadata] = {
    OnboardingStep.WELCOME: StepMetadata(
        step_num=0,
        title="Welcome",
        heading="Agent Substrate — Private GA Onboarding",
        description="High-density sandboxing and sub-100ms runtime for autonomous AI agents on pre-existing Kubernetes clusters.",
        real_command="atectl onboard --private-ga",
        checklist_title="System Readiness Check",
        checklist_items=[
            "Pre-configured Kubernetes Cluster: Required & Portable",
            "Private GA Customer Agreement: Gated Authorization",
            "Substrate Control Plane: Ready for install",
        ],
        done_message="Ready to begin setup! Press [Enter] to start.",
        next_action_label="Get Started (Enter) →",
    ),
    OnboardingStep.CHECK_SETUP: StepMetadata(
        step_num=1,
        title="Check your setup",
        heading="Check your environment",
        description="We'll check if you have everything needed to run Substrate — a container runtime, Python, and kubectl CLI.",
        real_command="which docker && which kubectl && which python3",
        checklist_title="Checking prerequisites...",
        checklist_items=[
            "Container runtime detected (Docker / Podman / Containerd)",
            "Python 3.10+ runtime available",
            "Kubectl command utility ready in PATH",
        ],
        done_message="Prerequisites verified. Let's connect your pre-configured cluster next.",
        next_action_label="Connect your cluster [Enter ↵] →",
    ),
    OnboardingStep.CONNECT_CLUSTER: StepMetadata(
        step_num=2,
        title="Connect your cluster",
        heading="Verify Pre-configured Kubernetes Cluster",
        description="Substrate runs on any pre-existing Kubernetes cluster — ensuring infrastructure portability across GKE, EKS, AKS, OpenShift, or on-prem with zero cloud lock-in.",
        real_command="kubectl cluster-info && kubectl get nodes -o wide",
        checklist_title="Verifying pre-configured cluster...",
        checklist_items=[
            "Connecting to active kubeconfig cluster: [demo-cluster]",
            "Verified Kubernetes API server compatibility (v1.31.1-gke / Portable)",
            "Validating node capacity (12 ready nodes, hardware virtualization enabled)",
        ],
        done_message="Pre-configured cluster verified! Now let's complete the Private GA agreement.",
        next_action_label="Private GA Agreement [Enter ↵] →",
    ),
    OnboardingStep.PRIVATE_GA_AGREEMENT: StepMetadata(
        step_num=3,
        title="Private GA Agreement",
        heading="Private GA Access & Contractual Agreement",
        description="Because this is a Private General Availability release, customers must acknowledge that production support and SLAs require an explicit agreement with Google.",
        real_command='atectl auth register --customer="Acme Corp" --token="ga-sub-8f92a-live-contract"',
        checklist_title="Registering Private GA customer...",
        checklist_items=[
            "Customer credentials & organization verified (Acme Corp)",
            "Private GA License Token registered: [ga-sub-8f92a-live-contract]",
            "Acknowledgment recorded: Production support requires an explicit agreement with Google",
        ],
        done_message="Private GA agreement acknowledged! Now let's turn on Substrate.",
        next_action_label="Turn on Substrate [Enter ↵] →",
        is_agreement_step=True,
    ),
    OnboardingStep.TURN_ON_SUBSTRATE: StepMetadata(
        step_num=4,
        title="Turn on Substrate",
        heading="Turn on Substrate Control Plane",
        description="Installing the Substrate core controllers, state registry, and high-speed networking onto your cluster in namespace [substrate-system].",
        real_command="kubectl apply -f manifests/substrate-control-plane.yaml",
        checklist_title="Installing Substrate components...",
        checklist_items=[
            "Applying CustomResourceDefinitions (WorkerPool, ActorTemplate, Actor)",
            "Deploying Valkey Metadata & State Registry",
            "Bootstrapping Substrate Gateway & API Server (listening on :8080)",
            "Initializing eBPF network routing controller in [substrate-system]",
        ],
        done_message="Substrate is active! Next, let's install the CLI.",
        next_action_label="Install the CLI [Enter ↵] →",
    ),
    OnboardingStep.INSTALL_CLI: StepMetadata(
        step_num=5,
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
        next_action_label="Deploy first actor [Enter ↵] →",
    ),
    OnboardingStep.FIRST_ACTOR: StepMetadata(
        step_num=6,
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
        next_action_label="Send a request [Enter ↵] →",
    ),
    OnboardingStep.SEND_REQUEST: StepMetadata(
        step_num=7,
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
        next_action_label="Test Pause & Resume [Enter ↵] →",
        benchmark_text="Turn Latency: 82ms  │  TTFT (First Token): 14ms  │  Throughput: 120 tok/s",
    ),
    OnboardingStep.PAUSE_RESUME: StepMetadata(
        step_num=8,
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
        next_action_label="Scale it up [Enter ↵] →",
        benchmark_text="Cold Start (890ms)  ➔  Suspend (38ms, 0% CPU)  ➔  Warm Resume (115ms)",
    ),
    OnboardingStep.SCALE_UP: StepMetadata(
        step_num=9,
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
        next_action_label="🚀 Finish Onboarding [Enter ↵]",
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
    selected_track: str = "track_quickstart"
    selected_cluster: str = "demo-cluster"
    customer_org: str = "Acme Corp"
    customer_email: str = "rajithal@enterprise.com"
    ga_token: str = "ga-sub-8f92a-live-contract"
    agreement_accepted: bool = True
    is_complete: bool = False
