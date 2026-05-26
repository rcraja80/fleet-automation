#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

IGNORE_PREFIXES = ("tmpfs", "devtmpfs", "overlay", "proc", "sysfs", "cgroup", "nsfs", "squashfs", "ramfs")
THRESHOLD = 80
REPORT_FILE = Path("fs_report.json")

def main():
    out = subprocess.check_output(["df", "-P"], text=True).splitlines()[1:]
    alerts = []
    seen = set()

    for line in out:
        cols = line.split()
        if len(cols) < 6:
            continue
        fs, used_pct, mount = cols[0], cols[4], cols[5]
        if fs.startswith(IGNORE_PREFIXES) or mount in seen:
            continue
        seen.add(mount)
        try:
            pct = int(used_pct.rstrip("%"))
        except ValueError:
            continue
        if pct > THRESHOLD:
            alerts.append({"filesystem": fs, "mount": mount, "usage": pct})

    result = {"threshold": THRESHOLD, "count": len(alerts), "alerts": alerts}
    text = json.dumps(result, indent=2)
    REPORT_FILE.write_text(text)
    print(text)
    return 2 if alerts else 0

if __name__ == "__main__":
    sys.exit(main())
