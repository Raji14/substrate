# Antigravity & Agent Substrate: Interactive Onboarding Journey Design Guide

This design guide outlines the architectural blueprint, UX philosophy, and execution model for the interactive onboarding journey built for **Antigravity** utilizing **Agent Substrate on Google Kubernetes Engine (GKE)**. 

Alongside this guide, you will find `antigravity_onboarding.py`—a fully executable, high-fidelity Python terminal simulation that demonstrates this onboarding journey in practice. It translates complex Kubernetes actions into a gamified, real-time command-line interface (CLI) inspired by the best aspects of modern developer tools.

---

## 1. Executive Context & Source Analysis

To scale next-generation autonomous agents and reinforcement learning (RL) sandboxes, the Google DeepMind team developed **Antigravity**, a leading agent framework designed to scale complex multi-step workflows [35, 46]. In production, scaling these workloads on standard container infrastructure is economically unviable because productivity, personal, and coding agents spend up to **90–95% of their time idle** waiting for human input, wasting valuable CPU and memory resources [29, 32, 42].

**Agent Substrate on GKE** addresses this bottleneck by introducing a high-density, low-latency execution plane that achieves a **10X increase in session density** and slashes idle compute costs by up to **90%** [31, 32, 36]. It accomplishes this through a lightweight control plane and a state-of-the-art **suspend-and-resume data plane**, checkpointing an agent's memory and filesystem state to disk when idle and resuming it in milliseconds upon a wake event [30, 36, 43].

### Strategic Shift in Deployment
Historically, GKE infrastructure relied on managed add-ons. However, meeting the needs of rapid AI iteration cycles required a major pivot:
* **Open-Source Self-Installation**: By delivering core Substrate components via open-source installation scripts (`ate.dev/install.sh | bash`), engineering teams bypass traditional cloud bureaucracy [1, 3]. This allows developers to inspect, customize, and extend their agent control planes at the speed of the open-source community [61].
* **The "Pierceable Abstraction" Model**: The onboarding experience must cater to two distinct personas:
  1. *AI Engineers (Zero-K8s Experience)*: Must be able to define agent templates (`ActorTemplate`) and execute sessions without writing raw Kubernetes YAML or using `kubectl` [60].
  2. *Platform Engineers (K8s Experts)*: Retain full declarative control using Custom Resource Definitions (CRDs) like `WorkerPool` to configure scaling, security, and hardware topology [60, 61].

---

## 2. Onboarding UX Philosophy: Inspired by Claude Code

The terminal onboarding journey is designed around the terminal user interface (TUI) principles that developers love [95]:

| UX Element | Implementation in Antigravity Onboarding Journey | Key Benefit |
| :--- | :--- | :--- |
| **Zero "Fluff" & Text Focus** | Minimalist borders, unicode-enhanced lists, and dense information layouts. Employs clean ANSI colors without bloated GUIs [95]. | Extreme focus on code and direct actions; high screen-space efficiency [95]. |
| **Short Feedback Loops** | The "prompt ➔ instant execution ➔ immediate result" cycle mimics engaging game loops [95, 96]. Every CLI action has a clear, colored confirmation. | Keeps developers in an active flow state; builds confidence in the system [95]. |
| **Visible Progress (The "Fog of War" Effect)** | Rather than displaying a static loading text, the script draws a real-time, interactive grid of cluster pods pre-warming [95, 96]. | Satisfies the developer's desire to "reveal the map," making the AI infrastructure visible [96]. |
| **Playful Companion ("Newton")** | Introduced a witty, supportive, and conversational virtual flight instructor named **Newton** [96]. | Humans learn better through peer interaction; the humor breaks the density of GKE configurations [96]. |
| **Progressive Disclosure** | Heavy YAML manifests, REST API payloads, and advanced network policies are hidden behind interactive choices or presented only when relevant [97, 98]. | Prevents context window overload; allows beginners to start fast and experts to dive deep [97]. |

---

## 3. Detailed Walkthrough of the Onboarding Flow

The companion script, `antigravity_onboarding.py`, implements a 5-step interactive journey. Each step corresponds directly to a technical primitive in the GKE Agent Substrate architecture.

### Step 1: GKE Cluster Connection & Isolation Boundary Check
* **Technical Action**: The script queries the local `kubecontext` to scan for active GKE clusters.
* **Primitive Alignment**: To run high-performance **MicroVM isolation via Cloud Hypervisor (CHV)**, GKE nodes must support nested virtualization (e.g., N2, C3, or C4 instances) [55, 76]. If the user selects a cluster lacking nested virtualization (like a test cluster running on non-nested GCE shapes), the onboarding flow dynamically degrades to **gVisor userspace syscall isolation** [55, 76].
* **UX Treatment**: Newton guides the user through selecting their target cluster.

### Step 2: Bootstrapping the Core Controllers
* **Technical Action**: Downloading and placing the `atectl` CLI binary, followed by registering the core Substrate CRDs (`workerpools.ate.dev`, `actortemplates.ate.dev`, and `actors.ate.dev`) [63, 67].
* **Primitive Alignment**: Demonstrates how Substrate integrates cleanly with standard GKE and Kubernetes API-servers without imposing upstream K8s changes [58].
* **UX Treatment**: Beautiful animated spinners track binary installation and CRD registration, providing explicit feedback for each resource.

### Step 3: Provisioning the Worker Pool
* **Technical Action**: Setting up a pre-warmed fleet of Kubernetes pods ("Workers") that sit in standby, ready to inject active agent sessions ("Actors") [66].
* **Primitive Alignment**: Decouples the **Infrastructure Layer** (physical Node Pools managed by standard GCP tools or Custom Compute Classes) from the **Agent Layer** (pre-warmed worker pods holding network, storage mounts, and security boundaries active) [64, 65, 71].
* **UX Treatment**: Newton explains the difference between Node Pools and Worker Pools. The script then prompts the user for worker capacity and displays an animated, live ASCII-grid topology map showing the worker pods transitioning from *Initializing* `⚙` to *Standby* `█`.

### Step 4: Deploying an Actor Template & Latency Testing
* **Technical Action**: Defining an `ActorTemplate` pointing to a pre-built OCI agent container image, followed by a live suspend/resume loop test [70].
* **Primitive Alignment**: Tests the performance of the local data plane L1 Local NVMe SSD snapshot cache (target <200ms) versus the L2 GCS fallback store [43, 56, 93].
* **UX Treatment**: Displays actual simulated commands (`atectl create template`) and triggers a visual speed-test that compares cold start latency (~900ms) with suspend (~40ms) and warm-cache resume (~120ms) speeds.

### Step 5: Platform & SDK Integration
* **Technical Action**: Exposing how application-level code interacts with GKE Substrate.
* **Primitive Alignment**: Teaches developers how to route end-user hooks (e.g., from Slack or Telegram gateways) by invoking `POST /v1/atespaces/{space}/actors/{id}/execute` [84]. Crucially, it highlights how the agent harness emits an explicit `/idle` signal upon turn completion, triggering immediate GCS checkpointing and freeing host CPU/RAM [84, 85].
* **UX Treatment**: Renders a clean, syntax-highlighted Python code snippet demonstrating these exact endpoints in a high-contrast container block.

---

## 4. How to Run the Companion Onboarding Script

To experience this onboarding journey firsthand, you can run the provided script in your terminal environment.

### Interactive Mode (Recommended)
This mode provides the full visual layout, typewriter narrations from Newton, real-time spinner delays, and animated grid topologies:
```bash
python3 /workspace/scratch/antigravity_onboarding.py
```

### Headless / Automation Mode
If you want to run this in a continuous integration (CI) pipeline, non-interactive shell, or within automated testing setups, pass the `--headless` flag. This runs the script instantly with default parameters and removes thread sleeping/spinner delays:
```bash
python3 /workspace/scratch/antigravity_onboarding.py --headless
```

---

## 5. Summary of Key Substrate Commands for Post-Onboarding

Once the onboarding journey is complete, the user can manage their high-density agent fleets with the following standard commands:

* **`atectl status`**
  Queries the global metadata registry and local clusters to show the status of registered templates, active worker pools, and cluster health [16, 60, 63].
* **`atectl top workers`**
  Monitors node-level memory overcommit and cache-miss rates. Essential for platform leads managing density economics [88].
* **`atectl list actors`**
  Lists all active, suspended, and suspending user sessions in the registry, showcasing the density multipliers [43, 75].
* **`atectl logs <actor-id>`**
  Streams correlation traces of host sandbox lifecycle events mapped to OpenTelemetry spans, perfect for workload debugging [89].
