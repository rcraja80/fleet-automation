# FS Monitoring Endpoint

This project provides a small FastAPI service that checks filesystem usage on the local machine and returns the result as JSON.

## What it does
- Checks disk usage with `df -P`.
- Ignores pseudo filesystems and snap loop mounts.
- Reports only real filesystems above the threshold.
- Saves the latest report to `fs_report.json`.

## Files
- `fs_check_app.py` - FastAPI application.
- `requirements.txt` - Python dependencies.
- `fs_report.json` - Generated report file after calling `/fs-check`.

## Endpoints
- `/` - Basic status message.
- `/health` - Health check endpoint.
- `/fs-check` - Runs the filesystem scan and returns JSON.
- `/report` - Reads the last generated report from `fs_report.json`.

## Local run
```bash
pip install -r requirements.txt
uvicorn fs_check_app:app --reload
```

## Test in browser
Open these URLs in your browser:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/fs-check
- http://127.0.0.1:8000/report
