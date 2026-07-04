# test_final_state.py
import os
import subprocess
import glob
import tempfile
import json

def test_adversarial_corpus():
    script_path = '/home/user/curator.py'
    assert os.path.isfile(script_path), f"Agent script not found at {script_path}"

    clean_files = sorted(glob.glob('/app/corpus/clean/*.artx'))
    evil_files = sorted(glob.glob('/app/corpus/evil/*.artx'))

    assert len(clean_files) > 0, "No clean files found in /app/corpus/clean/"
    assert len(evil_files) > 0, "No evil files found in /app/corpus/evil/"

    clean_failed = []
    evil_failed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test clean files
        for clean_file in clean_files:
            basename = os.path.basename(clean_file)
            out_file = os.path.join(tmpdir, basename + '.json')
            result = subprocess.run(['python3', script_path, clean_file, out_file], capture_output=True)

            if result.returncode != 0:
                clean_failed.append(basename)
            elif not os.path.isfile(out_file):
                clean_failed.append(f"{basename} (no output file)")
            else:
                try:
                    with open(out_file, 'r') as f:
                        data = json.load(f)
                    if "artifact_id" not in data:
                        clean_failed.append(f"{basename} (missing artifact_id)")
                except json.JSONDecodeError:
                    clean_failed.append(f"{basename} (invalid json format)")

        # Test evil files
        for evil_file in evil_files:
            basename = os.path.basename(evil_file)
            out_file = os.path.join(tmpdir, basename + '.json')
            result = subprocess.run(['python3', script_path, evil_file, out_file], capture_output=True)

            if result.returncode == 0:
                evil_failed.append(basename)
            elif os.path.isfile(out_file):
                evil_failed.append(f"{basename} (created output file despite failure)")

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/failed: {', '.join(clean_failed)}")

    assert not error_messages, " | ".join(error_messages)