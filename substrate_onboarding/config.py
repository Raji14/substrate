"""Configuration schemas, options, and state models for Agent Substrate Onboarding.

Derived from the Agent Substrate PRFAQ and hack/install-ate.sh.
Designed around the "Pierceable Abstraction" model for Platform Engineers and AI Engineers.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class OnboardingStep(str, Enum):
    WELCOME = "welcome"
    QUESTIONNAIRE = "questionnaire"
    DOCTOR = "doctor"
    AUTH = "auth"
    SUMMARY = "summary"
    COMPLETE = "complete"


@dataclass
class OptionItem:
    id: str
    title: str
    description: str
    icon: str
    tip: str


# Step 1: Workload Architecture & Persona Target (PRFAQ Pierceable Abstraction)
TRACK_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="autonomous_swarm",
        title="Platform Engineer — Fleet WorkerPools",
        description="Provision fungible, pre-warmed GKE worker pools with microVM/gVisor isolation & autoscaling",
        icon="🛠️",
        tip="Runs 'atectl create workerpools' with capacity buffers, Custom Compute Classes (CCC), and Spot optimization.",
    ),
    OptionItem(
        id="interactive_sandbox",
        title="AI Engineer — No-YAML Agent Deployment",
        description="Deploy ActorTemplates (OCI images) and multiplex sessions without touching Kubernetes YAML",
        icon="🤖",
        tip="Runs 'atectl create template' linking OCI images to worker pools with real-time actor suspend/resume.",
    ),
    OptionItem(
        id="platform_admin",
        title="Full-Stack Platform & Autonomous Swarms",
        description="End-to-end setup: WorkerPool fleets, ActorTemplates, Envoy dataplane, and observability",
        icon="⚡",
        tip="Full infrastructure and actor multiplexing lifecycle for 50+ concurrent autonomous agents per node.",
    ),
    OptionItem(
        id="local_microvm",
        title="Local Dev & Rapid MicroVM Prototyping",
        description="Fast iteration on macOS/Linux using Docker, Colima, or Kind clusters (--setup-csi)",
        icon="💻",
        tip="Configures lightweight process cgroups, local port-forwards, and mock cloud storage.",
    ),
]

# Step 2: Dataplane Router & WorkerPool Topology
DATAPLANE_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="envoy_redis",
        title="MicroVM WorkerPool + Envoy Dataplane (Recommended)",
        description="100 pre-warmed workers (Cloud Hypervisor), Envoy proxy, and Redis state store",
        icon="⚡",
        tip="Applies --isolation=microvm --workers=100 --atenet-router=envoy --store-backend=redis for sub-50ms resume.",
    ),
    OptionItem(
        id="agentgateway_redis",
        title="gVisor WorkerPool + Agent Gateway Router",
        description="Hardened userspace syscall sandboxing with dynamic TLS and stream multiplexing",
        icon="🛡️",
        tip="Applies --isolation=gvisor --atenet-router=agentgateway --store-backend=redis for stream-based routing.",
    ),
    OptionItem(
        id="envoy_postgres",
        title="Enterprise Multi-Tenant Fleet + PostgreSQL",
        description="Relational persistence for multi-tenant audit logs, RBAC, and durable actor state",
        icon="🐘",
        tip="Applies --store-backend=postgres with automated mTLS credential bundle verification.",
    ),
]

# Step 3: Optimization & Isolation Sandbox Runtime
SANDBOX_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="gvisor",
        title="Local SSD Image Pre-caching (RL & Large Models)",
        description="Pre-warm heavy environment images onto Local SSDs to eliminate image pull delays",
        icon="⚡",
        tip="Enables 'atectl precache image' for instant zero-delay rollouts across worker nodes.",
    ),
    OptionItem(
        id="microvm",
        title="Cloud Hypervisor MicroVM (Hardware Virtualized)",
        description="Hardware-virtualized microVM isolation with nested virtualization on N2/C3/C4 nodes",
        icon="🛡️",
        tip="Configures --isolation=microvm for sub-200ms cold boots and strict hardware boundaries.",
    ),
    OptionItem(
        id="gcs_snapshots",
        title="GCS Snapshot Checkpointing (L2 Storage)",
        description="Persistent GCS bucket for microVM memory/disk state suspend and resume",
        icon="🪣",
        tip="Enables zero-downtime state persistence when workers suspend during LLM idle time.",
    ),
]

# Developer Tooling Presets
EDITOR_OPTIONS: List[OptionItem] = [
    OptionItem(
        id="cursor",
        title="Cursor / Windsurf AI IDE",
        description="Optimized AI editor with .cursorrules, context indexing, and Substrate CLI bindings",
        icon="⚡",
        tip="Installs .cursorrules and configures atectl terminal shortcuts.",
    ),
    OptionItem(
        id="vscode",
        title="Visual Studio Code",
        description="Modular editor with Kubernetes, Docker, and Python extension presets",
        icon="🟦",
        tip="Sets up .vscode/settings.json and recommended Kubernetes extension packs.",
    ),
    OptionItem(
        id="neovim",
        title="Neovim / Vim",
        description="Modal editing with Treesitter, Lua configs, and substrate-lsp bindings",
        icon="🟩",
        tip="Configures LSP snippets and telescope commands for substrate actor inspection.",
    ),
    OptionItem(
        id="terminal_cli",
        title="Terminal / atectl CLI",
        description="Direct atectl, kubectl, and headless agent automation workflows",
        icon="💻",
        tip="Configures environment variables, shell auto-completions, and PATH exports.",
    ),
]

# Backward compatibility alias
SNAPSHOT_OPTIONS = SANDBOX_OPTIONS


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
    current_step: OnboardingStep = OnboardingStep.WELCOME
    track: str = "autonomous_swarm"
    dataplane: str = "envoy_redis"
    sandbox_tier: str = "gvisor"
    editor: str = "cursor"
    storage_bucket: str = "my-substrate-snapshots"
    auth_mode: str = "api_key"  # "api_key", "oauth", "skipped"
    api_key_masked: str = ""
    api_key_raw: str = ""
    gke_cluster: str = "gke-agent-cluster"
    cluster_location: str = "us-central1-a"
    project_id: str = "gcp-agent-platform-prod"
    doctor_results: Dict[str, CheckResult] = field(default_factory=dict)
    preflight_results: Dict[str, CheckResult] = field(default_factory=dict)
    is_complete: bool = False

    def get_track_item(self) -> OptionItem:
        for item in TRACK_OPTIONS:
            if item.id == self.track:
                return item
        return TRACK_OPTIONS[0]

    def get_dataplane_item(self) -> OptionItem:
        for item in DATAPLANE_OPTIONS:
            if item.id == self.dataplane:
                return item
        return DATAPLANE_OPTIONS[0]

    def get_sandbox_item(self) -> OptionItem:
        for item in SANDBOX_OPTIONS:
            if item.id == self.sandbox_tier:
                return item
        return SANDBOX_OPTIONS[0]

    def get_editor_item(self) -> OptionItem:
        for item in EDITOR_OPTIONS:
            if item.id == self.editor:
                return item
        return EDITOR_OPTIONS[0]

    def to_summary_dict(self) -> Dict[str, str]:
        track_item = self.get_track_item()
        dataplane_item = self.get_dataplane_item()
        sandbox_item = self.get_sandbox_item()
        editor_item = self.get_editor_item()

        results = self.doctor_results or self.preflight_results
        ok_checks = sum(1 for r in results.values() if r.status == "ok")
        total_checks = len(results) if results else 6

        return {
            "Persona & Target": f"{track_item.icon} {track_item.title}",
            "WorkerPool Topology": f"{dataplane_item.icon} {dataplane_item.title}",
            "Optimization & Runtime": f"{sandbox_item.icon} {sandbox_item.title}",
            "Developer Tooling": f"{editor_item.icon} {editor_item.title}",
            "Authentication Mode": (
                f"API Key ({self.api_key_masked})"
                if self.auth_mode == "api_key" and self.api_key_masked
                else ("Google IAP (Authenticated)" if self.auth_mode == "oauth" else "Local Dev Mode")
            ),
            "GKE Cluster Target": f"{self.gke_cluster} ({self.cluster_location})",
            "Pre-Flight Health": f"{ok_checks}/{total_checks} Diagnostics Passed (Healthy)",
        }
