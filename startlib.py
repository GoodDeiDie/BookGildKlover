import os
import subprocess
import sys

print("Нажми Enter чтобы запустить...")
input()

while (True):
    process = subprocess.Popen([sys.executable, "lib.py"])
    process.wait()