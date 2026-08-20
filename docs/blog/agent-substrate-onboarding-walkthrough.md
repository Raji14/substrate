# ⚡ Getting Started with Agent Substrate on GKE: An Engineer's Onboarding Guide

> **Release Phase**: Private General Availability (Private GA)  
> **Audience**: Platform Engineers, AI Infrastructure Leads, and Autonomous Agent Developers  
> **Target Environment**: Google Kubernetes Engine (GKE) & Enterprise Kubernetes (v1.28+)

---

## 🛠️ 1. Pre-requisites Checklist

Before beginning the Agent Substrate installation, ensure your local workstation and target Kubernetes cluster meet the following requirements:

### 💻 Local Workstation Tools
- **`kubectl`** (v1.28 or later): Configured with access to your target cluster (`kubectl version --client`).
- **`gcloud` CLI** (v450.0.0 or later): Authenticated with Google Cloud (`gcloud auth list` and `gcloud config get-value project`).
- **`python3`** (v3.10 or later) & **`pip`**: Required for CLI utilities and local management tools.
- **`docker`**, **`podman`**, or **`containerd`**: Local container runtime.
- **`git`**: Version control for cloning manifests and repositories.

### ☸️ Target Kubernetes Cluster
- **Cluster Version**: Kubernetes **v1.28+** (GKE Standard or GKE Enterprise recommended).
- **Administrative Privileges**: Active user or Service Account must have `cluster-admin` permissions to apply Custom Resource Definitions (CRDs), create the `substrate-system` namespace, and deploy cluster-wide controllers.
- **Hardware Nested Virtualization (`/dev/kvm`)**: Required for microVM sandboxing. Nodes must run on machine families that support nested virtualization (e.g., Google Cloud `n2-standard-48` or `c3-standard` series).
- **Network CNI**: Standard GKE Datapath V2 / Cilium eBPF or compatible CNI.
- **Private GA Token**: An authorized enterprise support agreement with Google Cloud.

---

## 🚀 2. Step-by-Step Onboarding & Installation Script

Follow the steps below to bootstrap the Agent Substrate control plane, provision compute classes, configure autoscaling, and deploy your initial worker fleet.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           INSTALLATION PIPELINE OVERVIEW                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. Preflight Verification ────► Validate local tooling & cluster reachability    │
│ 2. Cluster Context Target ────► Select active kubeconfig context & verify RBAC   │
│ 3. Control Plane Deploy   ────► Bootstrap Gateway, State DB & Substrate Manager  │
│ 4. Compute Class Provision────► Apply Custom Compute Class with KVM enabled      │
│ 5. Autoscaling Config     ────► Set up OneHPA & CapacityBuffer standby capacity  │
│ 6. WorkerPool Deployment  ────► Deploy default warm microVM sandboxes (10 nodes) │
│ 7. Latency Verification   ────► Execute end-to-end cold-start test turn (<100ms) │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Preflight Verification

Verify your workstation dependencies and cluster connectivity:

```bash
# Verify CLI binaries
which kubectl docker python3 gcloud || { echo "Missing required binary in PATH"; exit 1; }

# Verify active Kubernetes cluster connection
kubectl cluster-info
```

---

### Step 2: Target Cluster Context & Namespace Setup

Ensure your active context points to your target cluster and create the dedicated system namespace:

```bash
# Verify active context
kubectl config current-context

# Create the dedicated Agent Substrate namespace
kubectl create namespace substrate-system --dry-run=client -o yaml | kubectl apply -f -
```

---

### Step 3: Deploy the Agent Substrate Control Plane

Apply the core control plane components: the gRPC API Gateway (listening on `:8080`), Valkey metadata state store, eBPF network router, and Substrate CustomResourceDefinitions:

```bash
kubectl apply -f manifests/substrate-control-plane.yaml
```

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
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: substrate-state-db
  namespace: substrate-system
spec:
  serviceName: substrate-state-db
  replicas: 1
  selector:
    matchLabels:
      app: substrate-state-db
  template:
    metadata:
      labels:
        app: substrate-state-db
    spec:
      containers:
      - name: valkey
        image: valkey/valkey:7.2
        ports:
        - containerPort: 6379
```

Verify control plane pods are ready:
```bash
kubectl wait --namespace substrate-system \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/name=substrate-gateway \
  --timeout=90s
```

---

### Step 4: Provision the Nested-Virt Custom Compute Class (CCC)

Agent Substrate relies on hardware nested virtualization (`/dev/kvm`) to deliver secure microVM sandboxes with sub-100ms startup times.

Apply the GKE Custom Compute Class manifest:

```bash
kubectl apply -f manifests/workerpool-ccc.yaml
```

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

*Alternatively, if managing node pools via `gcloud`:*
```bash
gcloud container node-pools create agent-spot-pool \
  --cluster=<YOUR_CLUSTER_NAME> \
  --region=<YOUR_REGION> \
  --machine-type=n2-standard-48 \
  --enable-nested-virtualization \
  --spot \
  --num-nodes=3
```

---

### Step 5: Configure High-Density Autoscaling & Standby Buffer

To absorb bursty agent traffic without cold-start spikes, pair **HorizontalPodAutoscaler** with **GKE CapacityBuffer**:

```bash
kubectl apply -f manifests/workerpool-autoscaling.yaml
```

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

### Step 6: Deploy the Default Substrate WorkerPool

Deploy the default warm worker fleet into `substrate-system`:

```bash
kubectl apply -f manifests/default-workerpool.yaml
```

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

Verify that the worker pool has initialized:
```bash
kubectl get workerpools -n substrate-system
```

---

### Step 7: Verify Installation with an End-to-End Cold-Start Turn

Run an automated validation test to verify that the control plane, state DB, eBPF router, and warm worker microVMs are functioning within sub-100ms parameters:

```bash
# Install or run the atectl CLI utility
atectl actor test-turn --workerpool=default-worker-pool
```

```
[TELEMETRY VALIDATION]
✓ Step 1: MicroVM Allocation  ➔ default-worker-pool-8f4b (14ms)
✓ Step 2: Prompt Dispatch     ➔ payload delivered to sandbox (22ms)
✓ Step 3: Execution Response  ➔ 200 OK acknowledged (12ms)
------------------------------------------------------------
Total Round-Trip: 48ms (<100ms verified)
Status: READY FOR PRODUCTION WORKLOADS
```

---

## ⚡ 3. What You Can Achieve Once Installation Is Complete

With Agent Substrate running on your GKE cluster, your infrastructure is primed for production autonomous agent workloads:

### 🏎️ 1. Ultra-Low Latency Cold Starts (<50ms)
- **Traditional Kubernetes**: Spinning up a dedicated pod per agent takes **15–45 seconds**.
- **Agent Substrate**: MicroVM execution sessions attach to warm standby workers in **<50ms**, making multi-agent reasoning and user-facing interactive turns seamless.

### 💰 2. 90%+ Memory Savings via Zero-Cost Suspension
- When autonomous agents are idle (waiting for human approval, multi-second LLM streaming, or external API responses), Substrate takes an instant memory snapshot and suspends the microVM.
- **CPU consumption drops to 0%**, and memory footprint drops to **<64MB per idle session**, eliminating compute waste during idle periods.

### 📈 3. 100+ Agent Sessions per Physical Node
- Decoupling logical **Actors** from physical **Workers** enables heavy multiplexing. You can pack **over 100 concurrent or dormant agent sessions** onto a single GKE node without degrading performance.

### 🛡️ 4. Hardware-Level Isolation & Security
- Workloads execute within hardware-isolated microVMs (`/dev/kvm`), ensuring strict tenant and agent isolation even when running untrusted tool-use scripts.

### ⚙️ 5. Declarative GitOps Management
- Complete infrastructure transparency: manage your clusters, autoscaling policies, worker pools, and compute classes via standard Kubernetes YAML and GitOps pipelines (ArgoCD, Flux, or Config Sync).

---

## 💻 Developer Quickstart Reference

```bash
# 1. Create an isolated agent session
atectl actor create my-agent --template=default-agent

# 2. Execute a turn
atectl actor execute my-agent --prompt="Generate infrastructure test suite"

# 3. Suspend session (0% CPU cost)
atectl actor suspend my-agent

# 4. Resume instantly upon next webhook or event
atectl actor resume my-agent

# 5. Inspect cluster worker pools and active sessions
atectl get workerpools
```

---

## 💡 Teardown & Uninstall Instructions

Clean up all Substrate resources at any time with:

```bash
kubectl delete -f manifests/default-workerpool.yaml
kubectl delete -f manifests/workerpool-autoscaling.yaml
kubectl delete -f manifests/workerpool-ccc.yaml
kubectl delete -f manifests/substrate-control-plane.yaml
```
