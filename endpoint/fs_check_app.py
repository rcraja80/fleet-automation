from fastapi import FastAPI
from pathlib import Path
import json
import subprocess

app = FastAPI(title="FS Monitoring API")
THRESHOLD = 80
IGNORE_PREFIXES = ("tmpfs", "devtmpfs", "overlay", "proc", "sysfs", "cgroup", "nsfs", "squashfs", "ramfs")

def should_ignore(fs, mount):
    if fs.startswith(IGNORE_PREFIXES):
        return True
    if fs.startswith("/dev/loop"):
        return True
    if "/var/lib/snapd/snap/" in mount:
        return True
    return False

def scan_filesystems():
    out = subprocess.check_output(["df", "-P"], text=True).splitlines()[1:]
    alerts = []

    for line in out:
        cols = line.split()
        if len(cols) < 6:
            continue
        fs, used_pct, mount = cols[0], cols[4], cols[5]
        if should_ignore(fs, mount):
            continue
        try:
            pct = int(used_pct.rstrip("%"))
        except ValueError:
            continue
        if pct > THRESHOLD:
            alerts.append({
                "filesystem": fs,
                "mount": mount,
                "usage": pct
            })

    result = {
        "threshold": THRESHOLD,
        "count": len(alerts),
        "alerts": alerts
    }

    Path("fs_report.json").write_text(json.dumps(result, indent=2))
    return result

@app.get("/")
def root():
    return {"message": "FS Monitoring API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/fs-check")
def fs_check():
    return scan_filesystems()

@app.get("/report")
def report():
    p = Path("fs_report.json")
    if not p.exists():
        return {"error": "report not generated yet"}
    return json.loads(p.read_text())
