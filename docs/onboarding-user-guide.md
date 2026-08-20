# ⚡ Agent Substrate: Private GA Onboarding Guide & UX Specifications

> **Release Phase**: Private General Availability (Private GA)  
> **Target Platform**: Pre-existing Kubernetes Clusters (GKE, EKS, AKS, OpenShift, On-Prem, or Local Sandbox)  
> **Audience**: Platform Engineers, AI Infrastructure Leads, and Autonomous Agent Developers  
> **Available Interfaces**: Interactive Web Simulator (`./open_simulator.sh`), Terminal Application (`python3 onboard.py`), and CLI (`atectl`)

---

## 🧭 Section 1: Critical User Journeys (CUJs) & Installation Tracks

### 🏢 Key Enterprise Architectural Decisions

1. **Two Streamlined Installation Choices**:
   - **🚀 Quickstart**: Automatic cluster detection & default configuration (Recommended). Automatically verifies active `kubeconfig` cluster and applies standard sensible defaults in seconds.
   - **⚙️ Advanced**: Custom installation with `kubectl`. Allows platform engineers to tailor Custom Compute Classes (CCC), microVM sandboxing drivers, and resource quotas.
2. **Pre-existing Cluster Requirement (Portability & Anti-Lock-In)**:
   - Users bring their pre-configured Kubernetes cluster (GKE, EKS, AKS, OpenShift, or on-prem) ensuring total infrastructure portability without vendor lock-in.
3. **Gated Access for Private General Availability (GA)**:
   - Gated customer registration and explicit contractual acknowledgment that **production support and enterprise SLAs require an executed agreement with Google Cloud**.
4. **Post-Installation WorkerPool Fleet Configuration**:
   - **Compatible Node Pool (Hardware Nested Virtualization)**: Scans cluster node pools; if missing nested-virt, options are presented: (1) Auto Custom Compute Class (CCC), (2) Manual gcloud, (3) Choose different cluster. Users can modify and re-apply YAML manifests (`manifests/workerpool-ccc.yaml`) at any time.
   - **WorkerPool Autoscaling (HPA & CapacityBuffer)**: Options: (1) Auto HPA OneHPA (min=10, max=100) & CapacityBuffer (3 standby replicas via `buffer.gke.io/standby-capacity`), (2) Manual kubectl, (3) Skip autoscaling. Users can modify and re-apply YAML manifests (`manifests/workerpool-autoscaling.yaml`) at any time.
   - **Confirm & Deploy Default Substrate WorkerPool**: Confirm and bootstrap 10 warm worker sandboxes with microVM isolation.

---

## 🎨 Section 2: The Agent Substrate Welcome Screen & Wonder Visualizations

### 🌟 Step 0: Welcome Screen (Hero Entrypoint)

The Welcome Screen features the glowing **Agent Substrate** ASCII Art logo with Google 4-color gradient palette, streaming typewriter description, core capabilities card, and 2 streamlined installation tracks.

![Step 0: Agent Substrate Welcome Screen](../demos/onboarding-tui/screenshots/step0_welcome.png)

#### 🎮 Keyboard Navigation Guide:
- **`[1]` / `[2]`**: Quick select Quickstart or Advanced track
- **`[Enter ↵]`**: Confirm selection & advance to the next step
- **`[↑ / ↓]`**: Navigate between choices
- **`[b]`**: Go back to previous step
- **`[F1]`**: Open global help overlay and command legend

---

## 🧭 Section 3: The 12-Step Interactive Journey

```
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Substrate                      Step 5 of 12                                                             │
│ Getting set up                 Set up Compatible WorkerPool Node Fleet                                  │
│ ────────────────────────────── Scanning cluster node pools for hardware nested virtualization. If no    │
│ 4 of 12 steps                  compatible pool is found, configure one via Custom Compute Class (CCC).  │
│                                                                                                         │
│ ✓ Check your setup             ┌─ Choose configuration option (Press [1-3]): ──────────────────────────┐│
│ ✓ Connect your cluster         │ ▶ [1] ⚡ Automatically create a compatible node pool using CCC (Rec.) ││
│ ✓ Private GA Agreement         │ ○ [2] 🛠️ Create a compatible node pool manually via gcloud             ││
│ ✓ Turn on Substrate            │ ○ [3] 🔄 Choose a different cluster                                   ││
│ 5 Compatible Node Pool         └───────────────────────────────────────────────────────────────────────┘│
│ 6 Configure Autoscaling                                                                                 │
│ 7 Deploy WorkerPool            ┌─ 💡 Note ─────────────────────────────────────────────────────────────┐│
│ 8 Install the CLI              │  You can modify and re-apply the CCC YAML manifest later at any time  ││
│ 9 First actor                  │  (e.g. manifests/workerpool-ccc.yaml).                                 ││
│ 10 Send a request              └───────────────────────────────────────────────────────────────────────┘│
│ 11 Pause & resume                                                                                       │
│ 12 Scale it up                                      [ ← Back [b] ]  [ Configure Autoscaling [Enter ↵] ] │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

### 1️⃣ Step 1: Check your setup
- **Command**: `which docker && which kubectl && which python3`
- **Checklist**: Container runtime, Python 3.10+, kubectl in PATH.

### 2️⃣ Step 2: Connect your cluster (Side-by-Side Verification)
- **Side-by-Side Layout**:
  - **Left**: Cluster selector (`[1-4]`) with GKE, EKS, AKS, Kind.
  - **Right**: Live verification card & control plane probe status in `[substrate-system]`.

### 3️⃣ Step 3: Private GA Agreement (Gated Access & Support Terms)
- **Command**: `atectl auth register --customer="Acme Corp" --token="ga-sub-8f92a-live-contract"`
- **Terms**: Explicit acknowledgment that production support requires an executed agreement with Google Cloud.

### 4️⃣ Step 4: Turn on Substrate (Control Plane Installation)
- **Command**: `kubectl apply -f manifests/substrate-control-plane.yaml`
- **Actions**: CRDs, Valkey state store, Gateway, eBPF router in `[substrate-system]`.

### 5️⃣ Step 5: Compatible Node Pool (Hardware Nested Virtualization)
- **Options**:
  1. `[1] (Recommended)`: **Automatically create a compatible node pool using Custom Compute Class** (`manifests/workerpool-ccc.yaml`)
  2. `[2]`: **Create a compatible node pool manually via gcloud**
  3. `[3]`: **Choose a different cluster**
- **Note**: Modifiable anytime via `manifests/workerpool-ccc.yaml`.

### 6️⃣ Step 6: WorkerPool Autoscaling (HPA & CapacityBuffer)
- **Options**:
  1. `[1] (Recommended)`: **Automatically configure HPA & CapacityBuffer with sensible defaults**
     - OneHPA: minReplicas=10, maxReplicas=100
     - CapacityBuffer: 3 standby replicas via `buffer.gke.io/standby-capacity`
     - Standby buffer ready for instant (<100ms) agent session injection
  2. `[2]`: **Configure autoscaling manually via kubectl**
  3. `[3]`: **Skip autoscaling configuration**
- **Note**: Modifiable anytime via `manifests/workerpool-autoscaling.yaml`.

### 7️⃣ Step 7: Confirm & Deploy Substrate WorkerPool
- **Options**:
  1. `[1] (Recommended)`: **Yes, deploy default Substrate WorkerPool [default-worker-pool]** (10 warm pods, microVM sandboxes)
  2. `[2]`: **Customize WorkerPool specifications**

### 8️⃣ Step 8: Install the CLI (`atectl`)
- **Command**: `go install ./cmd/atectl || curl -sSL https://ate.dev/atectl | sh`

### 9️⃣ Step 9: First actor (No-YAML Template Launch)
- **Command**: `atectl actor create my-first-actor --template=default-agent`

### 🔟 Step 10: Send a request (Streaming Execution & Benchmark)
- **Command**: `atectl actor execute my-first-actor --prompt="..."`
- **Benchmark**: Turn Latency: 82ms │ TTFT: 14ms │ Throughput: 120 tok/s

### 1️⃣1️⃣ Step 11: Pause & resume (0% Idle CPU)
- **Command**: `atectl actor suspend my-first-actor && atectl actor resume my-first-actor`
- **Benchmark**: Suspend 38ms (0% CPU) ➔ Resume 115ms

### 1️⃣2️⃣ Step 12: Scale it up & Fleet Inspection
- **Command**: `atectl create workerpools production-fleet --workers=20 --isolation=microvm`
