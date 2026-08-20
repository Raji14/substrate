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

---

## 🧭 Section 3: The 12-Step Interactive Journey

- **Step 1**: Check your setup (`which docker && which kubectl && which python3`)
- **Step 2**: Connect your cluster (Side-by-Side: Cluster Selector `[1-4]` & Verification Probe)
- **Step 3**: Private GA Agreement (`atectl auth register --customer="Acme Corp" --token="ga-sub-****"`)
- **Step 4**: Turn on Substrate (`kubectl apply -f manifests/substrate-control-plane.yaml`)
- **Step 5**: Compatible Node Pool (Scan node pools, Auto CCC vs Manual gcloud vs Different cluster; `manifests/workerpool-ccc.yaml` notice)
- **Step 6**: Configure Autoscaling (Auto HPA min=10 max=100 & CapacityBuffer=3 standby; `manifests/workerpool-autoscaling.yaml` notice)
- **Step 7**: Deploy WorkerPool (Confirm & deploy default Substrate WorkerPool with 10 warm replicas)
- **Step 8**: Install the CLI (`go install ./cmd/atectl || curl -sSL https://ate.dev/atectl | sh`)
- **Step 9**: First actor (`atectl actor create my-first-actor --template=default-agent`)
- **Step 10**: Send a request (`atectl actor execute my-first-actor --prompt="..."`)
- **Step 11**: Pause & resume (`atectl actor suspend && resume` with 0% CPU suspend)
- **Step 12**: Scale it up (`atectl create workerpools production-fleet --workers=20`)
