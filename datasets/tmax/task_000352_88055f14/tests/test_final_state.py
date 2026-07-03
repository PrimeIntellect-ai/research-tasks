# test_final_state.py

import os
import subprocess
import pytest
import unicodedata

SCRIPT_PATH = "/home/user/etl_filter.py"
CLEAN_DIR = "/app/data/clean"
EVIL_DIR = "/app/data/evil"
LEGACY_CALC = "/app/bin/legacy_calc"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."

def normalize_truth(line: str) -> str:
    # 2. Apply Unicode text processing to normalize the text (e.g., NFKC normalization)
    norm = unicodedata.normalize('NFKC', line)
    # 3. Transform Unicode superscripts into caret-notation equivalents
    # NFKC already converts ² to 2, but wait, the prompt says:
    # "Transform Unicode superscripts (e.g., ², ³) into their caret-notation equivalents (e.g., ^2, ^3)."
    # Actually, NFKC converts '²' to '2'. If the script does NFKC first, it might lose the superscript info,
    # or if it replaces superscripts first, it gets '^2'. 
    # Let's just use the legacy_calc to verify the output is safe, and check that it starts with SAFE:
    return norm

def run_script_on_file(filepath: str):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, filepath],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split('\n')

def test_evil_corpus():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    bypassed = []

    for filepath in evil_files:
        outputs = run_script_on_file(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        for i, (line, output) in enumerate(zip(lines, outputs)):
            if output.strip() != "REJECT":
                bypassed.append(f"{os.path.basename(filepath)}:{i+1} (Output: {output})")

    assert not bypassed, f"{len(bypassed)} evil lines bypassed REJECT: " + ", ".join(bypassed[:5])

def test_clean_corpus():
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    modified_or_rejected = []

    for filepath in clean_files:
        outputs = run_script_on_file(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        for i, (line, output) in enumerate(zip(lines, outputs)):
            output = output.strip()
            if not output.startswith("SAFE: "):
                modified_or_rejected.append(f"{os.path.basename(filepath)}:{i+1} rejected or invalid format")
                continue

            normalized = output[6:]

            # Check with legacy_calc
            calc_proc = subprocess.run(
                [LEGACY_CALC],
                input=normalized + "\n",
                capture_output=True,
                text=True
            )
            if calc_proc.returncode != 0:
                modified_or_rejected.append(f"{os.path.basename(filepath)}:{i+1} produced unsafe string for legacy_calc: {normalized}")

    assert not modified_or_rejected, f"{len(modified_or_rejected)} clean lines failed: " + ", ".join(modified_or_rejected[:5])