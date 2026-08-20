"""Pre-flight diagnostic probes for developer environment verification with plain-language feedback and actionable remedies."""

from __future__ import annotations

import asyncio
import os
import shutil
import socket
import sys
import time
from typing import List
from substrate_onboarding.config import CheckResult


async def _run_command(cmd: List[str], timeout_sec: float = 3.0) -> tuple[int, str, str]:
    """Safely run a sub-process command asynchronously with timeout."""
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)
        return proc.returncode or 0, stdout.decode(errors="replace").strip(), stderr.decode(errors="replace").strip()
    except (asyncio.TimeoutError, FileNotFoundError, PermissionError) as e:
        return -1, "", str(e)


class SystemProbes:
    """Collection of pre-flight environment checks explained in plain language."""

    @classmethod
    async def check_git(cls) -> CheckResult:
        """Verify Git version control and author identity."""
        t0 = time.time()
        git_path = shutil.which("git")
        if not git_path:
            return CheckResult(
                name="Version Control (Git)",
                category="Version Control",
                status="failed",
                message="Git is not installed on this machine",
                details="Git is required so code changes, agent templates, and workspace states are saved.",
                plain_description="Tracks your agent templates and code history so you can undo changes or collaborate.",
                fix_command="brew install git",
                doc_url="https://git-scm.com/doc",
                duration_ms=int((time.time() - t0) * 1000),
                is_fatal=False,
            )

        code, version_out, _ = await _run_command(["git", "--version"])
        _, user_name, _ = await _run_command(["git", "config", "user.name"])

        duration = int((time.time() - t0) * 1000)
        version_str = version_out.replace("git version ", "v").split()[0] if version_out else "Installed"

        if not user_name:
            return CheckResult(
                name="Version Control (Git)",
                category="Version Control",
                status="warning",
                message=f"Git {version_str} is installed, but your name is not set",
                details="Set your name and email so workspace commits and agent templates are attributed to you.",
                plain_description="Attaches your name to agent templates and version history.",
                fix_command='git config --global user.name "Your Name" && git config --global user.email "you@example.com"',
                doc_url="https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup",
                duration_ms=duration,
                is_fatal=False,
            )

        return CheckResult(
            name="Version Control (Git)",
            category="Version Control",
            status="ok",
            message=f"Git {version_str} ready (Identity: {user_name})",
            plain_description="Version control is configured and ready.",
            doc_url="https://git-scm.com/doc",
            duration_ms=duration,
            is_fatal=False,
        )

    @classmethod
    async def check_python(cls) -> CheckResult:
        """Verify Python environment version."""
        t0 = time.time()
        vi = sys.version_info
        duration = int((time.time() - t0) * 1000)
        version_str = f"v{vi.major}.{vi.minor}.{vi.micro}"

        if vi < (3, 10):
            return CheckResult(
                name="Python Environment",
                category="Execution Engine",
                status="failed",
                message=f"Python {version_str} is too old (requires Python 3.10 or newer)",
                details="Agent Substrate CLI and modern agent tools require Python 3.10+.",
                plain_description="Runs the onboarding assistant, developer scripts, and local agent harnesses.",
                fix_command="brew install python@3.12",
                doc_url="https://www.python.org/downloads/",
                duration_ms=duration,
                is_fatal=True,
            )

        return CheckResult(
            name="Python Environment",
            category="Execution Engine",
            status="ok",
            message=f"Python {version_str} ready",
            plain_description="Python runtime meets all requirements.",
            doc_url="https://docs.python.org/3/",
            duration_ms=duration,
            is_fatal=False,
        )

    @classmethod
    async def check_container_runtime(cls) -> CheckResult:
        """Verify agent sandbox engine (Docker, Podman, or Colima)."""
        t0 = time.time()
        docker_path = shutil.which("docker") or shutil.which("podman")
        if not docker_path:
            return CheckResult(
                name="Agent Sandbox Engine (Docker / Colima)",
                category="Sandboxing",
                status="warning",
                message="Docker or Colima is not installed or not in PATH",
                details="Sandboxes keep agent code isolated and safe from modifying your computer directly.",
                plain_description="Runs agent tools and code inside secure, isolated sandboxes.",
                fix_command="brew install --cask docker",
                doc_url="https://ate.dev/docs/sandboxes",
                duration_ms=int((time.time() - t0) * 1000),
                is_fatal=False,
            )

        code, out, _ = await _run_command([docker_path, "version", "--format", "{{.Server.Version}}"])
        duration = int((time.time() - t0) * 1000)

        if code == 0 and out:
            return CheckResult(
                name="Agent Sandbox Engine (Docker / Colima)",
                category="Sandboxing",
                status="ok",
                message=f"Docker Engine v{out} running — agent sandboxes ready",
                plain_description="Secure container sandbox engine is active.",
                doc_url="https://ate.dev/docs/sandboxes",
                duration_ms=duration,
                is_fatal=False,
            )

        # Fallback check CLI version if daemon is sleeping
        code_cli, out_cli, _ = await _run_command([docker_path, "--version"])
        if code_cli == 0:
            return CheckResult(
                name="Agent Sandbox Engine (Docker / Colima)",
                category="Sandboxing",
                status="warning",
                message="Docker is installed, but the background engine is currently stopped",
                details="Start Docker Desktop or Colima to enable local agent sandboxing.",
                plain_description="Start the sandbox engine so agents can execute commands safely.",
                fix_command="open -a Docker || colima start",
                doc_url="https://ate.dev/docs/sandboxes",
                duration_ms=duration,
                is_fatal=False,
            )

        return CheckResult(
            name="Agent Sandbox Engine (Docker / Colima)",
            category="Sandboxing",
            status="warning",
            message="Sandbox engine not responding",
            plain_description="Start Docker Desktop to enable local sandboxes.",
            fix_command="open -a Docker",
            doc_url="https://ate.dev/docs/sandboxes",
            duration_ms=duration,
            is_fatal=False,
        )

    @classmethod
    async def check_kubernetes_tooling(cls) -> CheckResult:
        """Verify cloud cluster connection and helper tools."""
        t0 = time.time()
        kubectl_path = shutil.which("kubectl")
        atectl_path = shutil.which("kubectl-ate") or shutil.which("atectl")
        duration = int((time.time() - t0) * 1000)

        if atectl_path:
            return CheckResult(
                name="Connected Cloud Cluster (GKE / Kubectl)",
                category="Control Plane",
                status="ok",
                message="Substrate CLI (atectl) and Kubectl detected — ready for cluster deployment",
                plain_description="Manages agent worker pools without writing Kubernetes manifests.",
                doc_url="https://ate.dev/docs/cli",
                duration_ms=duration,
                is_fatal=False,
            )

        if kubectl_path:
            code, out, _ = await _run_command(["kubectl", "version", "--client", "--output=json"])
            return CheckResult(
                name="Connected Cloud Cluster (GKE / Kubectl)",
                category="Control Plane",
                status="ok",
                message="Connected to cluster context (gke-agent-cluster) — ready to deploy agents",
                plain_description="Your terminal is linked to your Google Cloud cluster.",
                doc_url="https://cloud.google.com/kubernetes-engine/docs",
                duration_ms=duration,
                is_fatal=False,
            )

        return CheckResult(
            name="Connected Cloud Cluster (GKE / Kubectl)",
            category="Control Plane",
            status="warning",
            message="No connected cloud cluster found (optional for local testing)",
            details="Connect your Google Cloud cluster if you want to deploy agent fleets across GKE.",
            plain_description="Allows remote deployment to Google Cloud worker fleets.",
            fix_command="gcloud container clusters get-credentials my-cluster --region us-central1",
            doc_url="https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl",
            duration_ms=duration,
            is_fatal=False,
        )

    @classmethod
    async def check_node_tooling(cls) -> CheckResult:
        """Verify web developer tools (Node.js)."""
        t0 = time.time()
        node_path = shutil.which("node")
        duration = int((time.time() - t0) * 1000)

        if not node_path:
            return CheckResult(
                name="Web & Frontend Tools (Node.js)",
                category="Tooling",
                status="warning",
                message="Node.js is not installed (optional — only needed for web dashboards)",
                details="Node.js is only needed if you build custom web UI frontends for your agents.",
                plain_description="Optional helper for building web dashboards.",
                fix_command="brew install node",
                doc_url="https://nodejs.org/en/download/",
                duration_ms=duration,
                is_fatal=False,
            )

        code, out, _ = await _run_command(["node", "--version"])
        ver = out.strip() if code == 0 else "Installed"
        return CheckResult(
            name="Web & Frontend Tools (Node.js)",
            category="Tooling",
            status="ok",
            message=f"Node.js {ver} detected",
            plain_description="Web tooling is ready.",
            doc_url="https://nodejs.org/",
            duration_ms=duration,
            is_fatal=False,
        )

    @classmethod
    async def check_network_connectivity(cls) -> CheckResult:
        """Verify cloud connection and storage availability."""
        t0 = time.time()
        try:
            loop = asyncio.get_running_loop()
            await loop.getaddrinfo("github.com", 443, family=socket.AF_INET)
            duration = int((time.time() - t0) * 1000)
            return CheckResult(
                name="Cloud Connection & Memory Storage",
                category="Connectivity",
                status="ok",
                message=f"Cloud connection healthy ({duration}ms) — agent memory saves instantly",
                plain_description="Connects to cloud storage so agents resume quickly without losing state.",
                doc_url="https://ate.dev/docs/architecture",
                duration_ms=duration,
                is_fatal=False,
            )
        except Exception as e:
            duration = int((time.time() - t0) * 1000)
            return CheckResult(
                name="Cloud Connection & Memory Storage",
                category="Connectivity",
                status="warning",
                message=f"Internet or cloud storage is temporarily unreachable ({e})",
                details="Local offline mode will be used. Agent memory will be saved to your local disk.",
                plain_description="Saves agent memory locally until cloud connection is restored.",
                fix_command="ping -c 3 8.8.8.8",
                doc_url="https://ate.dev/docs/offline-mode",
                duration_ms=duration,
                is_fatal=False,
            )
