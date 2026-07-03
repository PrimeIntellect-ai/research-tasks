# test_final_state.py
import os
import subprocess
import pytest

def test_telemetry_filter():
    app_dir = "/home/user/telemetry_filter"
    assert os.path.isdir(app_dir), f"Directory {app_dir} does not exist. Did you create the cargo project?"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')])
    evil_files = sorted([os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')])

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    # Pre-build to avoid intermingled stdout/stderr from cargo if they didn't build it
    build_res = subprocess.run(["cargo", "build", "--release"], cwd=app_dir, capture_output=True, text=True)
    assert build_res.returncode == 0, f"Cargo build failed:\n{build_res.stderr}"

    failed_clean = []
    for fp in clean_files:
        res = subprocess.run(
            ["cargo", "run", "--release", "--", fp],
            cwd=app_dir,
            capture_output=True,
            text=True
        )
        out = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else ""
        if out != "VALID":
            failed_clean.append(os.path.basename(fp))

    failed_evil = []
    for fp in evil_files:
        res = subprocess.run(
            ["cargo", "run", "--release", "--", fp],
            cwd=app_dir,
            capture_output=True,
            text=True
        )
        out = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else ""
        if out != "INVALID":
            failed_evil.append(os.path.basename(fp))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    if errors:
        pytest.fail(" | ".join(errors))