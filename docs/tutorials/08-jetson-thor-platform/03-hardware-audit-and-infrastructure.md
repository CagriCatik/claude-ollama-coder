# Hardware Audit & Secure Infrastructure (M0–M1)

Before launching models or running agent containers, establish the baseline truth of the NVIDIA Jetson AGX Thor hardware and lock down the host infrastructure.

---

## 1. Phase M0 — Hardware & System Audit (Priority P0)

The goal of M0 is to inspect the system as-is, capturing kernel versions, CUDA support, available storage, and thermal baselines before modifying software.

### Diagnostic Execution Commands

Run the following inspection commands directly on the AGX Thor terminal:

```bash
# 1. Jetson Linux release & architecture
cat /etc/nv_tegra_release
uname -a
uname -m

# 2. GPU detection & driver status
nvidia-smi

# 3. Memory & NVMe storage capacity
free -h
lsblk -o NAME,SIZE,TYPE,MOUNTPOINTS
df -h

# 4. Docker & NVIDIA Container Runtime validation
docker --version
docker info | grep -i -A 5 runtimes

# 5. Network interfaces & IP addresses
ip -br addr
```

### Target Software Stack

NVIDIA's baseline documentation designates **JetPack 7.2.1 with Jetson Linux 39.2.1** as the reference release for the AGX Thor.

```text
Target Environment:
- SoC: NVIDIA Jetson AGX Thor (Blackwell Tensor Cores)
- CPU: ARM64 (aarch64) multi-core high-performance cluster
- Unified Memory: 128 GB LPDDR5X
- OS: Jetson Linux 39.2.1 (based on Ubuntu 24.04 LTS / JetPack 7.2.1)
- CUDA: 12.8+ / Compute Capability 10.x (Blackwell)
```

### Deliverables for Phase M0
1. `hardware_inventory.md`: Complete hardware inventory and serials.
2. `system_audit.json`: Machine-readable dump of `nvidia-smi --query-gpu`, `lscpu`, and `lsblk`.
3. `baseline_report.md`: Idle power consumption, baseline thermal readings, and free storage margin.

---

## 2. Phase M1 — Secure Infrastructure Setup (Priority P0)

Establish the AGX Thor as a hardened, reproducible AI compute server.

### 2.1 Persistent Storage Partitioning

All AI-related assets are separated from the root OS filesystem and mounted under `/srv/agentic/`:

```text
/srv/agentic/
├── config/             # Model, agent, and security policies (.yaml)
├── models/             # Weights survive container restarts
│   ├── ollama/         # GGUF model blobs
│   └── huggingface/    # Checkpoints for vLLM (Safetensors)
├── cache/              # KV-cache and prompt prefix caches
├── containers/         # Isolated Docker build contexts
├── logs/               # Structured inference and audit logs
├── benchmarks/         # Benchmark datasets and performance traces
├── backups/            # Configuration snapshots and task states
└── artifacts/          # Generated diffs, test logs, and reports
```

Create the directory structure with appropriate ownership:
```bash
sudo mkdir -p /srv/agentic/{config,models/ollama,models/huggingface,cache,containers,logs,benchmarks,backups,artifacts}
sudo chown -R $USER:$USER /srv/agentic
chmod -R 750 /srv/agentic
```

### 2.2 Docker & NVIDIA Container Runtime

Verify that the NVIDIA Container Runtime is configured as the default runtime for Docker:

```bash
docker info --format '{{json .Runtimes}}'
```

If `nvidia` is missing, configure `/etc/docker/daemon.json`:
```json
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "default-runtime": "nvidia"
}
```
Restart Docker:
```bash
sudo systemctl restart docker
```

> [!WARNING]
> Thor uses the **Blackwell GPU architecture**. Do not pull generic `linux/arm64` containers built for Jetson Orin (Ampere architecture). Always use container images tagged specifically for JetPack 7 / Thor.

### 2.3 Network Hardening & Zero-Trust Access

Apply strict firewall rules to prevent unauthenticated access:
1. **Public Exposure**: Zero open ports to the WAN.
2. **Inference Port**: Ollama (`11434`) and vLLM (`8000`) bind strictly to `127.0.0.1`.
3. **SSH Access**: Enforce ED25519 public-key authentication; disable password authentication and root login:
   ```ini
   # /etc/ssh/sshd_config.d/99-hardened.conf
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   X11Forwarding no
   ```
4. **Remote Access from Mac**: All connections traverse an SSH tunnel or a private Tailscale mesh.
