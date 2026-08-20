"""Configuration schemas, options, and state models for Agent Substrate Onboarding.

Derived from the Agent Substrate Onboarding Specification & Day-0 Script.
Structured as a 6-step wizard with left-sidebar navigation on Google Kubernetes Engine (GKE).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class OnboardingStep(str, Enum):
    CLUSTER = "cluster"                  # Step 1: Cluster Detection & Verification
    CONTROL_PLANE = "control_plane"      # Step 2: Control Plane Installation
    NODE_POOL = "node_pool"              # Step 3: Node Pool & CCC Hardware Nested-Virt
    AUTOSCALING = "autoscaling"          # Step 4: WorkerPool Autoscaling & CapacityBuffer
    DEPLOY_WORKERPOOL = "deploy_wp"      # Step 5: Deploy Default WorkerPool
    LAUNCHPAD = "launchpad"              # Step 6: Live Verification & Operations Runbook

    # Backward compatibility aliases
    WELCOME = "cluster"
    DOCTOR = "control_plane"
    QUESTIONNAIRE = "node_pool"
    AUTH = "autoscaling"
    SUMMARY = "launchpad"
    COMPLETE = "complete"


@dataclass
class OptionItem:
    id: str
    title: str
    description: str
    icon: str
    tip: str


# Step 1: Available GKE Clusters in Kubeconfig
CLUSTER_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="demo_cluster_us_central1",
        title="gke_demo_project_us-central1-a_demo-cluster (Recommended)",
        description="GKE v1.31.1-gke.1520000 in us-central1-a (Target: demo-cluster)",
        icon="🌐",
        tip="Connects to the primary GKE development cluster in us-central1-a.",
    ),
    OptionItem(
        id="staging_cluster_us_west1",
        title="gke_demo_project_us-west1-b_staging-cluster",
        description="GKE v1.31.0 in us-west1-b (Target: staging-cluster)",
        icon="🧪",
        tip="Staging cluster with multi-zone standby nodes.",
    ),
    OptionItem(
        id="analytics_cluster_eu_west1",
        title="gke_demo_project_europe-west1-c_analytics-cluster",
        description="GKE v1.30.4 in europe-west1-c (Target: analytics-cluster)",
        icon="📊",
        tip="Europe analytics cluster with high-memory nodes.",
    ),
]

# Step 3: Node Pool & Hardware Isolation (Custom Compute Class)
NODEPOOL_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="ccc_auto",
        title="Automatically create a compatible Node Pool using Custom Compute Class (Recommended)",
        description="Applies Custom Compute Class manifest (agent-spot-ccc) with n2-standard-48, Spot fallback, and nested-virt",
        icon="⚡",
        tip="Provisions an optimal GKE node pool with hardware nested virtualization (KVM) for microVM isolation.",
    ),
    OptionItem(
        id="gcloud_manual",
        title="Create a compatible Node Pool manually via gcloud",
        description="Run 'gcloud container node-pools create --enable-nested-virtualization' in another terminal",
        icon="🛠️",
        tip="Manual gcloud CLI configuration for custom VPCs and security policies.",
    ),
    OptionItem(
        id="switch_cluster",
        title="Choose a different cluster",
        description="Return to Step 1 and select another active Kubernetes cluster",
        icon="🔄",
        tip="Switch cluster context without losing installation progress.",
    ),
]

# Step 4: Autoscaling & Capacity Buffer Configuration
AUTOSCALING_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="auto_hpa_buffer",
        title="Automatically configure HPA & CapacityBuffer with sensible defaults (Recommended)",
        description="Applies OneHPA (min=10, max=100) and fixed-replica-buffer (3 standby pods via buffer.gke.io)",
        icon="⚡",
        tip="Maintains pre-warmed standby worker pods for instant (<100ms) agent session injection.",
    ),
    OptionItem(
        id="kubectl_manual",
        title="Configure Autoscaling manually via kubectl",
        description="Apply custom HorizontalPodAutoscaler and CapacityBuffer manifests later",
        icon="📄",
        tip="Use custom metrics or external Prometheus triggers for scaling.",
    ),
    OptionItem(
        id="skip_autoscaling",
        title="Skip autoscaling configuration",
        description="Run fixed worker pool size without automatic pod scaling",
        icon="⏭️",
        tip="Suitable for local development or fixed-capacity evaluation.",
    ),
]

# Step 5: Deploy Default WorkerPool
DEPLOY_WP_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="deploy_default_yes",
        title="Yes, deploy default WorkerPool [default-worker-pool] (Recommended)",
        description="10 standby replicas, microVM sandbox isolation, 10% warm headroom in namespace [substrate-system]",
        icon="🚀",
        tip="Deploys the production execution layer ready for agent container injection.",
    ),
    OptionItem(
        id="deploy_default_no",
        title="No, skip default WorkerPool deployment",
        description="Only install the control plane; configure worker pools later via atectl CLI",
        icon="⏹️",
        tip="Control plane will be deployed without worker instances.",
    ),
]


@dataclass
class CheckResult:
    name: str
    category: str = "System"
    status: str = "pending"  # "pending", "running", "ok", "warning", "failed"
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
    current_step: OnboardingStep = OnboardingStep.CLUSTER
    installation_mode: str = "quickstart"  # "quickstart", "advanced"
    selected_cluster: str = "demo-cluster"
    cluster_context: str = "gke_demo_project_us-central1-a_demo-cluster"
    cluster_location: str = "us-central1-a"
    cluster_version: str = "v1.31.1-gke.1520000"
    namespace: str = "substrate-system"
    nodepool_mode: str = "ccc_auto"
    machine_type: str = "n2-standard-48"
    nested_virt: bool = True
    autoscaling_mode: str = "auto_hpa_buffer"
    min_replicas: int = 10
    max_replicas: int = 100
    standby_replicas: int = 3
    deploy_workerpool: bool = True
    workerpool_name: str = "default-worker-pool"
    isolation_type: str = "microvm"
    is_complete: bool = False

    def to_summary_dict(self) -> Dict[str, str]:
        return {
            "Target Cluster": f"{self.selected_cluster} ({self.cluster_location})",
            "GKE Version": self.cluster_version,
            "Control Plane Namespace": self.namespace,
            "Node Pool Compute": f"{self.machine_type} (Nested-Virt: {'Enabled' if self.nested_virt else 'Disabled'})",
            "Autoscaling Policy": f"OneHPA ({self.min_replicas}–{self.max_replicas} pods) + {self.standby_replicas} Standby Buffer",
            "Default WorkerPool": f"{self.workerpool_name} ({self.isolation_type} sandbox, 10 ready)",
            "Control Plane Status": "Healthy (Gateway listening on :8080)",
        }
