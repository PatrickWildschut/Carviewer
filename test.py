import subprocess
import os

env = os.environ.copy()
env["DISPLAY"] = ":0"
env["XAUTHORITY"] = "/home/patrick/.Xauthority"

result = subprocess.run([input()], capture_output=True, text=True, check=True)

print(result)