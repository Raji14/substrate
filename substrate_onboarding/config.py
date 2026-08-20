"""Configuration schemas, options, and state models for Agent Substrate Onboarding.

Addresses:
1. Splash Title: "Agent Substrate" with Google 4-color gradient.
2. Two Installation Choices: Quickstart and Advanced.
3. Side-by-side Cluster Selection & Verification.
4. Private GA Gated Agreement & Contractual Terms.
5. Post-Installation WorkerPool Configuration:
   - Compatible Node Pool setup (Scan cluster node pools, CCC vs gcloud vs different cluster, YAML re-apply note)
   - WorkerPool Autoscaling (HPA OneHPA min=10 max=100, CapacityBuffer=3 standby, instant injection, YAML note)
   - Confirm & deploy default Substrate WorkerPool
6. Fast Developer Loop: CLI Install, First Actor, Send Request, Pause/Resume, Scale Up.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class OnboardingStep(str, Enum):
    WELCOME = "welcome"                          # Step 0: Welcome & Setup Track Selection
    CHECK_SETUP = "check_setup"                  # Step 1: Check your environment
    CONNECT_CLUSTER = "connect_cluster"          # Step 2: Select cluster & verify control plane
    PRIVATE_GA_AGREEMENT = "private_ga"          # Step 3: Private GA gated access & agreement
    TURN_ON_SUBSTRATE = "turn_on_sub"            # Step 4: Turn on Substrate Control Plane
    COMPATIBLE_NODEPOOL = "compatible_nodepool"  # Step 5: Compatible Node Pool (CCC / Nested-Virt)
    CONFIG_AUTOSCALING = "config_autoscaling"    # Step 6: WorkerPool Autoscaling (HPA & CapacityBuffer)
    DEPLOY_WORKERPOOL = "deploy_workerpool"      # Step 7: Confirm & Deploy Substrate WorkerPool
    INSTALL_CLI = "install_cli"                  # Step 8: Install the CLI
    FIRST_ACTOR = "first_actor"                  # Step 9: First actor
    SEND_REQUEST = "send_request"                # Step 10: Send a request
    PAUSE_RESUME = "pause_resume"                # Step 11: Pause & resume
    SCALE_UP = "scale_up"                        # Step 12: Scale it up & Live Launchpad
    COMPLETE = "complete"

    # Backward compatibility aliases
    CLUSTER = "connect_cluster"
    CREATE_CLUSTER = "connect_cluster"
    CONTROL_PLANE = "turn_on_sub"
    NODE_POOL = "compatible_nodepool"
    AUTOSCALING = "config_autoscaling"
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
    provider: str = "Kubernetes"
    version: str = "v1.31"
    nodes: int = 12
    control_plane_status: str = "Not Installed"


# Setup Tracks for Welcome Screen
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

# Available Clusters from Kubeconfig
AVAILABLE_CLUSTERS: List[OptionItem] = [
    OptionItem(
        id="cluster_gke_prod",
        title="gke_enterprise_us-central1_prod",
        description="GKE Standard in us-central1 • 12 nodes (96 vCPUs) • KVM Ready",
        icon="🌐",
        tip="Active context. Recommended for production agent workloads.",
        shortcut_key="1",
        provider="Google Kubernetes Engine (GKE)",
        version="v1.31.1-gke.1520000",
        nodes=12,
        control_plane_status="Not Installed (Clean cluster ready for Substrate)",
    ),
    OptionItem(
        id="cluster_aws_eks",
        title="aws-eks-production-us-east-1",
        description="AWS EKS in us-east-1 • 8 nodes (64 vCPUs) • Nitro Enclaves",
        icon="☁️",
        tip="Multi-cloud enterprise cluster.",
        shortcut_key="2",
        provider="Amazon Elastic Kubernetes Service (EKS)",
        version="v1.30.4-eks",
        nodes=8,
        control_plane_status="Not Installed (Clean cluster ready for Substrate)",
    ),
    OptionItem(
        id="cluster_azure_aks",
        title="azure-aks-agent-fleet-eastus",
        description="Azure AKS in eastus • 6 nodes (48 vCPUs) • Hyper-V Isolated",
        icon="🔷",
        tip="Enterprise Azure cluster.",
        shortcut_key="3",
        provider="Azure Kubernetes Service (AKS)",
        version="v1.30.3-aks",
        nodes=6,
        control_plane_status="Not Installed (Clean cluster ready for Substrate)",
    ),
    OptionItem(
        id="cluster_local_kind",
        title="kind-substrate-sandbox",
        description="Local Kind Sandbox • 3 nodes (24 vCPUs) • Dev testbed",
        icon="🧪",
        tip="Local development sandbox.",
        shortcut_key="4",
        provider="Kind (Local Kubernetes)",
        version="v1.31.0",
        nodes=3,
        control_plane_status="Not Installed (Clean cluster ready for Substrate)",
    ),
]

# Step 5: Compatible Node Pool Options (Scanning & Nested-Virt)
NODEPOOL_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="ccc_auto",
        title="Automatically create a compatible node pool using Custom Compute Class (Recommended)",
        description="Applies Custom Compute Class manifest with n2-standard-48, Spot fallback, and nested virtualization enabled.",
        icon="⚡",
        tip="Applies manifests/workerpool-ccc.yaml. Modifiable anytime.",
        shortcut_key="1",
    ),
    OptionItem(
        id="ccc_manual_gcloud",
        title="Create a compatible node pool manually via gcloud",
        description="Generates gcloud container node-pools create command with --enable-nested-virtualization.",
        icon="🛠️",
        tip="For custom enterprise security policies.",
        shortcut_key="2",
    ),
    OptionItem(
        id="ccc_different_cluster",
        title="Choose a different cluster",
        description="Return to Step 2 to select another cluster context from your kubeconfig.",
        icon="🔄",
        tip="Switch cluster context.",
        shortcut_key="3",
    ),
]

# Step 6: WorkerPool Autoscaling Options (HPA & CapacityBuffer)
AUTOSCALING_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="auto_hpa_buffer",
        title="Automatically configure HPA & CapacityBuffer with sensible defaults (Recommended)",
        description="Applies OneHPA (min=10, max=100) and fixed-replica-buffer (3 standby replicas) for instant <100ms agent session injection.",
        icon="⚡",
        tip="Applies manifests/workerpool-autoscaling.yaml. Modifiable anytime.",
        shortcut_key="1",
    ),
    OptionItem(
        id="manual_hpa",
        title="Configure autoscaling manually via kubectl",
        description="Export template manifests to customize scaling metrics, CPU/memory thresholds, and buffer headroom.",
        icon="🛠️",
        tip="Custom metrics & thresholds.",
        shortcut_key="2",
    ),
    OptionItem(
        id="skip_autoscaling",
        title="Skip autoscaling configuration",
        description="Keep fixed worker pool replica count without horizontal dynamic scaling.",
        icon="⏭️",
        tip="Fixed worker count.",
        shortcut_key="3",
    ),
]

# Step 7: Confirm & Deploy Substrate WorkerPool
DEPLOY_WP_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="deploy_yes_default",
        title="Yes, deploy default Substrate WorkerPool [default-worker-pool] (Recommended)",
        description="Bootstraps 10 warm worker sandboxes with microVM isolation and instant actor attachment in [substrate-system].",
        icon="🚀",
        tip="Instant warm agent capacity.",
        shortcut_key="1",
    ),
    OptionItem(
        id="deploy_customize",
        title="Customize WorkerPool specifications",
        description="Review and customize memory limits, vCPU allocations, and container sandbox isolation drivers.",
        icon="⚙️",
        tip="Custom resources & quotas.",
        shortcut_key="2",
    ),
]

CLUSTER_OPTIONS = AVAILABLE_CLUSTERS
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
    is_cluster_step: bool = False
    is_option_step: bool = False
    yaml_notice: Optional[str] = None


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
        next_action_label="Get Started [Enter ↵] →",
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
        done_message="Prerequisites verified. Let's select your target cluster next.",
        next_action_label="Connect your cluster [Enter ↵] →",
    ),
    OnboardingStep.CONNECT_CLUSTER: StepMetadata(
        step_num=2,
        title="Connect your cluster",
        heading="Select Cluster & Verify Substrate Control Plane",
        description="Choose a cluster from your active kubeconfig. We'll verify its provider type, Kubernetes version, and probe for existing Substrate components in real-time.",
        real_command="kubectl config get-contexts && kubectl get ns substrate-system",
        checklist_title="Verifying selected cluster & control plane...",
        checklist_items=[
            "Cluster API Reachability: Connected to [gke_enterprise_us-central1_prod]",
            "Cluster Provider Verified: Google Kubernetes Engine (GKE v1.31.1)",
            "Node Fleet Capacity: 12 ready nodes (96 vCPUs, hardware nested-virt enabled)",
            "Control Plane Status: Checked [substrate-system] — Clean cluster ready for install",
        ],
        done_message="Cluster verified & clean! Now let's complete the Private GA agreement.",
        next_action_label="Private GA Agreement [Enter ↵] →",
        is_cluster_step=True,
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
        done_message="Substrate control plane is active! Next, let's configure the worker pool node fleet.",
        next_action_label="Set up WorkerPool [Enter ↵] →",
    ),
    OnboardingStep.COMPATIBLE_NODEPOOL: StepMetadata(
        step_num=5,
        title="Compatible Node Pool",
        heading="Set up Compatible WorkerPool Node Fleet",
        description="Scanning cluster node pools for hardware nested virtualization (KVM/microVM). If no compatible pool is found, configure one via Custom Compute Class (CCC).",
        real_command="kubectl apply -f manifests/workerpool-ccc.yaml",
        checklist_title="Configuring compatible node pool...",
        checklist_items=[
            "Scanning existing node pools: No hardware nested-virt pool detected",
            "Applying Custom Compute Class manifest [agent-spot-ccc] (n2-standard-48, KVM enabled)",
            "Configuring Spot fallback & capacity reservation",
            "Compatible node pool ready for high-density agent sandboxing",
        ],
        done_message="Compatible node pool configured! You can modify & re-apply manifests/workerpool-ccc.yaml anytime.",
        next_action_label="Configure Autoscaling [Enter ↵] →",
        is_option_step=True,
        yaml_notice="💡 Tip: You can modify and re-apply the Custom Compute Class YAML manifest later at any time (e.g. manifests/workerpool-ccc.yaml).",
    ),
    OnboardingStep.CONFIG_AUTOSCALING: StepMetadata(
        step_num=6,
        title="Configure Autoscaling",
        heading="Configure WorkerPool Autoscaling (HPA & CapacityBuffer)",
        description="Configure horizontal pod autoscaling and standby capacity buffers so your agent fleet can absorb sudden traffic surges with instant (<100ms) cold starts.",
        real_command="kubectl apply -f manifests/workerpool-autoscaling.yaml",
        checklist_title="Applying autoscaling & capacity buffer...",
        checklist_items=[
            "Applying HorizontalPodAutoscaler (OneHPA: minReplicas=10, maxReplicas=100)",
            "Applying CapacityBuffer (fixed-replica-buffer: 3 standby replicas via buffer.gke.io/standby-capacity)",
            "Standby buffer verified: Ready for instant (<100ms) agent session injection",
        ],
        done_message="Autoscaling active! You can modify & re-apply manifests/workerpool-autoscaling.yaml anytime.",
        next_action_label="Deploy WorkerPool [Enter ↵] →",
        is_option_step=True,
        yaml_notice="💡 Tip: You can modify and re-apply the HPA and CapacityBuffer YAML manifests later at any time (e.g. manifests/workerpool-autoscaling.yaml).",
    ),
    OnboardingStep.DEPLOY_WORKERPOOL: StepMetadata(
        step_num=7,
        title="Deploy WorkerPool",
        heading="Confirm & Deploy Substrate WorkerPool",
        description="Deploy the default Substrate WorkerPool into namespace [substrate-system] with pre-warmed agent sandboxes and microVM isolation.",
        real_command="kubectl apply -f manifests/default-workerpool.yaml",
        checklist_title="Deploying default Substrate WorkerPool...",
        checklist_items=[
            "Resolving worker sandbox image (gcr.io/ate-platform/worker:v1)",
            "Deploying WorkerPool CR [default-worker-pool] in namespace [substrate-system]",
            "Provisioning 10 warm worker sandboxes (3 standby buffer replicas active)",
            "WorkerPool is ready: 10/10 warm pods listening for agent execution turns",
        ],
        done_message="Default WorkerPool deployed! Now let's install the developer CLI.",
        next_action_label="Install the CLI [Enter ↵] →",
        is_option_step=True,
    ),
    OnboardingStep.INSTALL_CLI: StepMetadata(
        step_num=8,
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
        step_num=9,
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
        step_num=10,
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
        step_num=11,
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
        step_num=12,
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
    selected_cluster: str = "cluster_gke_prod"
    selected_nodepool_option: str = "ccc_auto"
    selected_autoscaling_option: str = "auto_hpa_buffer"
    selected_deploy_wp_option: str = "deploy_yes_default"
    cluster_provider: str = "Google Kubernetes Engine (GKE)"
    cluster_version: str = "v1.31.1-gke.1520000"
    control_plane_detected: bool = False
    customer_org: str = "Acme Corp"
    customer_email: str = "rajithal@enterprise.com"
    ga_token: str = "ga-sub-8f92a-live-contract"
    agreement_accepted: bool = True
    is_complete: bool = False
