import os
import subprocess
import sys

r = subprocess.run(
    ["bash", "backup.sh", os.path.expanduser("~/backup-test/data"),
     os.path.expanduser("~/backup-test/backups"), "3"],
    capture_output=True, text=True)
print("exit code:", r.returncode)
print(r.stdout)
if r.returncode != 0:
    print("stderr:", r.stderr)
    sys.exit(1)
