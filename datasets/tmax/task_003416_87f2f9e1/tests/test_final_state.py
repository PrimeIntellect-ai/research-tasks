# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import pytest

SCRIPT_PATH = "/home/user/sanitizer.py"
CLEAN_DIR = "/app/verifier/clean_logs"
EVIL_DIR = "/app/verifier/evil_logs"

def run_sanitizer(input_dir, output_dir):
    assert os.path.exists(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"
    cmd = ["python3", SCRIPT_PATH, "--input_dir", input_dir, "--output_dir", output_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_adversarial_corpora():
    if not os.path.exists(CLEAN_DIR) or not os.path.exists(EVIL_DIR):
        pytest.fail("Corpus directories are missing.")

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Run sanitizer on clean corpus
        run_sanitizer(CLEAN_DIR, clean_out)

        # Run sanitizer on evil corpus
        run_sanitizer(EVIL_DIR, evil_out)

        clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.log')]
        evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.log')]

        clean_modified = []
        evil_bypassed = []

        # Check clean corpus
        for fname in clean_files:
            orig_path = os.path.join(CLEAN_DIR, fname)
            out_path = os.path.join(clean_out, fname)

            if not os.path.exists(out_path):
                clean_modified.append(fname)
                continue

            with open(orig_path, 'r', encoding='utf-8') as f:
                orig_lines = f.readlines()
            with open(out_path, 'r', encoding='utf-8') as f:
                out_lines = f.readlines()

            if orig_lines != out_lines:
                clean_modified.append(fname)

        # Check evil corpus
        for fname in evil_files:
            orig_path = os.path.join(EVIL_DIR, fname)
            out_path = os.path.join(evil_out, fname)

            if not os.path.exists(out_path):
                # File completely dropped, which is fine (all lines dropped)
                continue

            with open(orig_path, 'r', encoding='utf-8') as f:
                orig_lines = f.readlines()
            with open(out_path, 'r', encoding='utf-8') as f:
                out_lines = f.readlines()

            # For evil2.log, only the last line is actually evil (the 5th line triggers the rule)
            # The prompt says "A log line MUST BE DROPPED... if it meets ANY...". 
            # In evil1.log and evil3.log, all lines meet the criteria.
            # In evil2.log, only the 5th line meets the criteria. Wait, the prompt says "100% of lines in the evil corpus must be dropped (resulting in empty or correctly filtered files)." Actually, the prompt says "100% of lines in the evil corpus must be dropped". Wait, the truth says "evil2.log" has 5 lines, but only the 5th line should be dropped. 
            # Let's check the exact wording: "Pass Criterion: 100% of lines in the clean corpus must be preserved in the output. 100% of lines in the evil corpus must be dropped (resulting in empty or correctly filtered files)." This implies that any line that is specifically evil should be dropped. But wait, in evil2.log, lines 1-4 are NOT evil. They don't meet the criteria (less than 5 requests). So they should be preserved!
            # Let me re-read the prompt: "Any log line that does not trigger the above rules must be preserved exactly as it was in the output file."
            # So evil2.log should preserve lines 1-4.
            # Let's write a custom checker for the evil logs based on the rules, or just check that the specific evil lines are dropped.
            # Actually, the prompt says "100% of lines in the evil corpus must be dropped (resulting in empty or correctly filtered files)." This might mean the evil files contain ONLY evil lines, or we should just check that the final output doesn't contain the evil lines.
            # Let's check what lines are in evil files.
            # evil1: 1710000015500 (attack), 1710000088000 (attack). Both dropped.
            # evil2: 1710000040000 to 1710000044000. Line 5 is dropped. Lines 1-4 are preserved.
            # evil3: 1710000060000 (mixed), 1710000061000 (mixed). Both dropped.

            # Since the instructions say "Iterate over every file in the evil corpus ... assert the agent's solution rejects/transforms each one according to the criterion", we should check that the specific evil lines are gone.

            # Let's check for the presence of known evil lines in the output.
            evil_lines_present = False
            for line in out_lines:
                if "attack" in line.lower() and "userB" in line: evil_lines_present = True
                if "userC" in line: evil_lines_present = True
                if "dropped because stddev" in line: evil_lines_present = True
                if "Paypаl" in line or "admіn" in line: evil_lines_present = True

            if evil_lines_present:
                evil_bypassed.append(fname)

        errors = []
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

        if errors:
            pytest.fail(" | ".join(errors))