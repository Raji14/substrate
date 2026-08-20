"""Left Navigation Sidebar Widget for the Substrate Onboarding Wizard.

Provides a persistent 6-step progress indicator and live cluster metadata panel.
"""

from __future__ import annotations
from typing import Optional
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Static
from rich.text import Text
from substrate_onboarding.config import OnboardingStep


STEP_ORDER = [
    (OnboardingStep.CLUSTER, "1. Cluster Detection"),
    (OnboardingStep.CONTROL_PLANE, "2. Control Plane"),
    (OnboardingStep.NODE_POOL, "3. Node Pool & CCC"),
    (OnboardingStep.AUTOSCALING, "4. Autoscaling (HPA)"),
    (OnboardingStep.DEPLOY_WORKERPOOL, "5. Deploy WorkerPool"),
    (OnboardingStep.LAUNCHPAD, "6. Launchpad & Verify"),
]

STEP_INDEX_MAP = {
    OnboardingStep.CLUSTER: 1,
    OnboardingStep.CONTROL_PLANE: 2,
    OnboardingStep.NODE_POOL: 3,
    OnboardingStep.AUTOSCALING: 4,
    OnboardingStep.DEPLOY_WORKERPOOL: 5,
    OnboardingStep.LAUNCHPAD: 6,
    OnboardingStep.COMPLETE: 6,
}


class SidebarNav(Widget):
    """Left navigation sidebar showing onboarding steps and live cluster context."""

    current_step: reactive[OnboardingStep] = reactive(OnboardingStep.CLUSTER)

    def __init__(
        self,
        current_step: OnboardingStep = OnboardingStep.CLUSTER,
        cluster_name: str = "demo-cluster",
        location: str = "us-central1-a",
        version: str = "v1.31.1-gke",
        namespace: str = "substrate-system",
        id: str = "sidebar-nav",
    ):
        super().__init__(id=id)
        self.current_step = current_step
        self.cluster_name = cluster_name
        self.location = location
        self.version = version
        self.namespace = namespace

    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar-container"):
            yield Static(self._render_sidebar_content(), id="sidebar-content")

    def _render_sidebar_content(self) -> Text:
        t = Text()

        # Sidebar Header
        t.append("╭─ 🧭 WIZARD STEPS ──────────╮\n", style="bold #8ab4f8")
        t.append("│                            │\n", style="#8ab4f8")

        curr_idx = STEP_INDEX_MAP.get(self.current_step, 1)

        for step_enum, step_label in STEP_ORDER:
            step_num = STEP_INDEX_MAP[step_enum]
            if step_num < curr_idx:
                icon = "✓"
                style_icon = "bold #81c995"
                style_text = "#81c995"
                prefix = f"  {icon} {step_label}"
            elif step_num == curr_idx:
                icon = "▶"
                style_icon = "bold #a8c7fa"
                style_text = "bold #ffffff on #0842a0"
                prefix = f"  {icon} {step_label}"
            else:
                icon = "○"
                style_icon = "#9aa0a6"
                style_text = "#9aa0a6"
                prefix = f"  {icon} {step_label}"

            t.append("│", style="#8ab4f8")
            if step_num == curr_idx:
                t.append(f" {icon} ", style=style_icon)
                t.append(f"{step_label.ljust(22)}", style=style_text)
            else:
                t.append(f" {icon} ", style=style_icon)
                t.append(f"{step_label.ljust(22)}", style=style_text)
            t.append("│\n", style="#8ab4f8")

        t.append("│                            │\n", style="#8ab4f8")
        t.append("├─ 📊 CLUSTER CONTEXT ───────┤\n", style="bold #8ab4f8")
        t.append("│                            │\n", style="#8ab4f8")

        meta_rows = [
            ("Cluster", self.cluster_name),
            ("Region", self.location),
            ("GKE K8s", self.version),
            ("Namespace", "substrate-sys"),
            ("Status", "Connected"),
        ]

        for k, v in meta_rows:
            t.append("│  ", style="#8ab4f8")
            t.append(f"{k.ljust(10)}: ", style="#9aa0a6")
            val_style = "bold #81c995" if k == "Status" else ("bold #8ab4f8" if k == "Cluster" else "#e3e3e3")
            t.append(f"{v.ljust(12)}", style=val_style)
            t.append("│\n", style="#8ab4f8")

        t.append("│                            │\n", style="#8ab4f8")
        t.append("╰────────────────────────────╯", style="bold #8ab4f8")
        return t

    def watch_current_step(self, step: OnboardingStep) -> None:
        try:
            content = self.query_one("#sidebar-content", Static)
            content.update(self._render_sidebar_content())
        except Exception:
            pass
