# ⚡ Scaling Autonomous AI Workloads: An Onboarding Walkthrough for Agent Substrate on GKE

> **Author**: Agent Substrate Engineering Team  
> **Release Phase**: Private General Availability (Private GA)  
> **Target Audience**: Platform Engineers, AI Infrastructure Leads, and Autonomous Agent Developers  
> **Try the Interactive Simulator**: `./demos/onboarding-tui/open_simulator.sh`

---

## 🚀 The Autonomous Agent Problem: Why Kubernetes Alone Isn’t Enough

Over the past year, enterprise AI teams transitioning from single-prompt LLM wrappers to **autonomous multi-agent loops** (like coding assistants, automated research swarms, and data pipeline orchestrators) have encountered a fundamental infrastructure barrier:

> **Traditional Kubernetes Pod scheduling was architected for long-running microservices, not bursty, stateful, and predominantly idle AI agents.**

When running thousands of agent sessions on standard Kubernetes:
1. **Cold Starts are Painful**: Booting a fresh Pod with its container runtime and model libraries takes **15 to 45 seconds**—unacceptable for real-time user-facing turns.
2. **Idle Resource Waste**: Autonomous agents spend **85%–95% of their session time idle** (waiting on human feedback, external tool APIs, or multi-step reasoning). Reserving 4–8 GB of RAM and 2–4 CPUs per idle Pod quickly leads to astronomical cloud bills.
3. **Control-Plane Choke**: Rapidly spinning up, modifying, and destroying thousands of Pods per hour hammers the Kubernetes `etcd` control plane.

### 💡 Enter Agent Substrate

**Agent Substrate** introduces a **pierceable, two-tier virtualization abstraction** built natively on top of Google Kubernetes Engine (GKE):
- **Actors** (your autonomous applications and agents) are decoupled from the underlying infrastructure.
- **Workers** (pre-warmed Kubernetes Pods running microVM sandboxes) stay warm in memory-efficient standby buffers.
- **Sub-100ms Cold Starts**: MicroVM execution sessions attach in **<50ms**, pause with **0% CPU consumption**, and resume instantly.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             AGENT SUBSTRATE ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   [ Developer / Agent SDK ] ──► [ atectl / gRPC API Gateway (:8080) ]            │
│                                              │                                   │
│                     ┌────────────────────────┴────────────────────────┐          │
│                     ▼                                                 ▼          │
│        [ Substrate Controller ]                            [ Valkey State DB ]   │
│         (eBPF Network Router)                               (Session Snapshots)  │
│                     │                                                 │          │
│                     ▼                                                 ▼          │
│        ┌─────────────────────────────────────────────────────────────────────┐   │
│        │                 GKE WORKERPOOL FLEET (Standby Buffer)               │   │
│        │  ┌─────────────────────────┐       ┌─────────────────────────┐      │   │
│        │  │  Pod 1: Warm microVM    │  ...  │  Pod N: Warm microVM    │      │   │
│        │  │  ┌───────────────────┐  │       │  ┌───────────────────┐  │      │   │
│        │  │  │ Actor Session A   │  │       │  │ Actor Session K   │  │      │   │
│        │  │  │ (Active: 14ms)    │  │       │  │ (Suspended: 0% CPU│  │      │   │
│        │  │  └───────────────────┘  │       │  └───────────────────┘  │      │   │
│        │  └─────────────────────────┘       └─────────────────────────┘      │   │
│        └─────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

In this post, we’ll walk through the **Private GA Onboarding Journey**—from cluster detection and Custom Compute Class provisioning to live cold-start verification.

---

## 🎬 The 7-Step Onboarding Journey

We designed the onboarding experience to be **Keyboard-First, Mouse-Friendly, and GitOps-Transparent**. Whether you run the native Textual TUI (`python3 onboard.py`) or the interactive web simulator (`./demos/onboarding-tui/open_simulator.sh`), here is the step-by-step walkthrough:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                ONBOARDING STAGES                                  │
├───────────────────────────────────────────────────────────────────────────────────┤
│  Step 0 ➔ Welcome Screen (Track Selection: Quickstart vs. Advanced GitOps)        │
│  Step 1 ➔ Check Setup (Preflight Doctor: Docker, Python 3.10+, Kubectl)          │
│  Step 2 ➔ Connect Cluster (Live Context Detection + GKE Private GA Terms)        │
│  Step 3 ➔ Turn on Substrate (Control Plane, Gateway, State DB, eBPF Router)      │
│  Step 4 ➔ Compatible Node Pool (Hardware Nested Virt KVM via CCC)                │
│  Step 5 ➔ Configure Autoscaling (OneHPA min=10, max=100 + CapacityBuffer)        │
│  Step 6 ➔ Deploy WorkerPool (Bootstrap 10 Warm MicroVM Sandboxes)                 │
│  Step 7 ➔ Installation Complete (Live In-TUI Cold-Start Latency Benchmark)        │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

### 🌟 Step 0: Welcome Screen & Track Selection

When launching the onboarding wizard, developers are greeted with a high-fidelity splash screen outlining Agent Substrate’s core guarantees:

```
                                    ⚡ AGENT SUBSTRATE
   High-density runtime with a pierceable abstraction for Platform Engineers & AI Developers
```

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│  CORE CAPABILITIES                                                                │
│  • Density Multiplier   : Up to 100 idle agent sessions per physical node         │
│  • Instant Turn Latency : <100ms cold start via pre-warmed microVM sandboxes      │
│  • Zero-Cost Suspend    : 0% CPU consumption during agent pauses & user thinking  │
│  • Clean Portability    : Native Kubernetes CRDs; zero proprietary vendor lock-in │
└───────────────────────────────────────────────────────────────────────────────────┘
```

#### Choose Your Onboarding Track:
- **[1] 🚀 Quickstart Track (Recommended)**: Automatically detects your active cluster context, applies standard Custom Compute Classes, and provisions a default 10-worker pool in under 60 seconds.
- **[2] ⚙️ Advanced Custom Track**: Step-by-step declarative customization allowing platform architects to inspect and customize YAML manifests for GitOps pipelines.

---

### 🔍 Step 1: Check Your Setup (Preflight Doctor)

Before touching your cluster, Substrate verifies your local workstation prerequisites asynchronously:

```bash
$ which docker && which python3 && which kubectl
```

```
  ✓ Container runtime detected (Docker / Podman / Containerd)
  ✓ Python 3.10+ runtime available
  ✓ Kubectl command utility ready in PATH
```

---

### 🌐 Step 2: Connect Cluster & Verify Control Plane

Substrate probes your active `kubeconfig` contexts in real time, validating Kubernetes API reachability, hardware virtualization compatibility, and existing namespace cleanliness:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│  SELECT TARGET CLUSTER                        CLUSTER CONTEXT VERIFICATION        │
│  [1] ● Google Kubernetes Engine (GKE v1.31)   Provider : GKE Enterprise [✓]       │
│  [2] ○ AWS Elastic Kubernetes Service (EKS)   Region   : us-central1 (Iowa)       │
│  [3] ○ Azure Kubernetes Service (AKS)         Capacity : 12 ready nodes (KVM ready│
│  [4] ○ Kind Local Development Sandbox         Probe    : [substrate-system] Clean │
└───────────────────────────────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Private GA Gated Access**: For enterprise production clusters on GKE, Substrate prompts you to acknowledge terms (`[a] Toggle Agreement`):
> `☑ I acknowledge that production support requires an explicit agreement with Google Cloud. [Verified ✓]`

---

### ⚡ Step 3: Turn on Substrate Control Plane

Substrate deploys its lightweight control plane into the `substrate-system` namespace. Platform engineers can click **`[</> Declarative Manifest]`** (or press **`[m]`**) to inspect the raw GitOps configuration before applying:

```yaml
# manifests/substrate-control-plane.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: substrate-system
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: substrate-gateway
  namespace: substrate-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: substrate-gateway
  template:
    metadata:
      labels:
        app.kubernetes.io/name: substrate-gateway
    spec:
      containers:
      - name: gateway
        image: gcr.io/gke-release/substrate/gateway:v1.0.0-ga
        ports:
        - containerPort: 8080
          name: grpc-api
```

---

### 🛠️ Step 4: Compatible Node Pool (Hardware Nested Virtualization)

High-density microVM sandboxing requires hardware nested virtualization (`/dev/kvm`). Substrate scans your node pools:
1. **Option 1 (Recommended)**: Automatically apply a GKE **Custom Compute Class (CCC)** manifest (`manifests/workerpool-ccc.yaml`) with `n2-standard-48` nodes and KVM enabled.
2. **Option 2**: Manual provisioning via `gcloud container node-pools create`.
3. **Option 3**: Target an existing virtualization-enabled node pool.

```yaml
# manifests/workerpool-ccc.yaml
apiVersion: compute.gke.io/v1
kind: CustomComputeClass
metadata:
  name: agent-spot-ccc
spec:
  machineType: n2-standard-48
  spot: true
  nodeTemplate:
    spec:
      nestedVirtualization: true
```

---

### 📈 Step 5: Configure WorkerPool Autoscaling (OneHPA & CapacityBuffer)

To eliminate cold-start spikes while optimizing spot capacity, Substrate pairs **HorizontalPodAutoscaler** with **GKE CapacityBuffer**:
- **OneHPA**: Automatically scales worker pods from **10 to 100** based on active actor queue depth.
- **CapacityBuffer**: Maintains **3 standby pre-warmed replicas** waiting to instantly absorb bursty agent creation requests.

```yaml
# manifests/workerpool-autoscaling.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: workerpool-hpa
  namespace: substrate-system
spec:
  scaleTargetRef:
    apiVersion: substrate.io/v1alpha1
    kind: WorkerPool
    name: default-worker-pool
  minReplicas: 10
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
apiVersion: buffer.gke.io/v1
kind: CapacityBuffer
metadata:
  name: fixed-replica-buffer
  namespace: substrate-system
spec:
  standbyReplicas: 3
```

---

### 📦 Step 6: Deploy Default WorkerPool

Substrate provisions your initial fleet of 10 warm microVM worker sandboxes:

```yaml
# manifests/default-workerpool.yaml
apiVersion: substrate.io/v1alpha1
kind: WorkerPool
metadata:
  name: default-worker-pool
  namespace: substrate-system
spec:
  replicas: 10
  computeClassName: agent-spot-ccc
  isolation: microvm
  warmBuffer: 3
```

---

### 🎉 Step 7: Installation Complete & Live Cold-Start Verification

Once the control plane and worker fleet report healthy, the wizard transitions into the celebratory completion dashboard. Rather than taking low latency for granted, you can trigger an **interactive live test turn** right from the TUI (`[t] Run Test Turn`):

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│  ⚡ LIVE COLD-START TEST TURN (Simulated sub-100ms Round-Trip)                    │
├───────────────────────────────────────────────────────────────────────────────────┤
│  ✓ 1. MicroVM Allocation: Warm worker assigned from default-worker-pool   [14ms]  │
│  ✓ 2. Agent Turn Dispatch: Prompt delivered to microVM sandbox            [22ms]  │
│  ✓ 3. Execution Response: Status verified and acknowledged                [12ms]  │
├───────────────────────────────────────────────────────────────────────────────────┤
│  🎉 Total Round-Trip: 48ms (<100ms cold-start target verified!)                   │
│  Output: {"status": "ready", "worker": "default-worker-pool-8f4b", "latency": 48}│
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Developer Quickstart: Managing Actors with `atectl`

Now that your GKE cluster is running Agent Substrate, here is how application engineers deploy and interact with autonomous agents using the `atectl` CLI:

### 1. Create Your First Actor Session
```bash
# Provision an isolated actor session from a standard template
atectl actor create my-first-agent \
  --template=default-agent \
  --workerpool=default-worker-pool

# Output:
# ✓ Actor "my-first-agent" created in 42ms (Worker: default-worker-pool-8f4b)
```

### 2. Send an Interactive Prompt / Tool Invocation
```bash
# Execute a turn against the actor session
atectl actor execute my-first-agent \
  --prompt="Analyze repository dependencies and generate test scaffolding."
```

### 3. Suspend & Resume with 0% CPU Consumption
```bash
# Suspend the actor when idle (takes a memory snapshot, frees CPU cores)
atectl actor suspend my-first-agent

# Resume instantly (<50ms) upon next incoming webhook or user message
atectl actor resume my-first-agent
```

### 4. Inspect Live Telemetry
```bash
# View active worker pools and capacity metrics
atectl get workerpools

# Stream data-plane logs and pause/resume telemetry
atectl logs workerpool/default-worker-pool --follow
```

---

## 📊 Benchmark: Standard Kubernetes vs. Agent Substrate

| Metric | Standard Kubernetes (1 Pod / Agent) | Agent Substrate on GKE | Improvement |
|---|---|---|---|
| **Cold Start Latency** | 15,000ms – 45,000ms | **< 50ms** | **~500x Faster** |
| **Idle Memory Footprint** | 4 – 8 GB / Agent | **< 64 MB / Agent** | **90%+ Memory Savings** |
| **Suspended CPU Cost** | Continuous core reservation | **0% CPU** (Memory Snapshot) | **Zero Idle Compute Waste** |
| **Cluster Density** | ~10–20 agents / Node | **100+ agents / Node** | **5x–10x Higher Density** |
| **Control Plane Load** | Heavy Pod churn (`etcd` pressure) | Steady WorkerPool (Zero churn) | **Rock-solid stability** |

---

## 💡 Cleanup & Teardown Reassurance

We believe in zero-friction evaluation. You can clean up Substrate resources at any time with standard declarative commands:

```bash
# Teardown Substrate control plane and worker pools
kubectl delete -f manifests/substrate-control-plane.yaml
kubectl delete -f manifests/default-workerpool.yaml

# Or using atectl CLI
atectl uninstall --purge
```

---

## 🚀 Get Started Today

Agent Substrate is available today under **Private General Availability (Private GA)** on Google Kubernetes Engine (GKE) and portable to any enterprise Kubernetes cluster.

- **Run the Interactive Simulator**:
  ```bash
  git clone https://github.com/agent-substrate/substrate.git
  cd substrate
  ./demos/onboarding-tui/open_simulator.sh
  ```
- **Launch the Native Terminal App**:
  ```bash
  python3 onboard.py
  ```
- **Join the Private GA Program**: Reach out to your Google Cloud account team or register your organization in `atectl auth register`.
