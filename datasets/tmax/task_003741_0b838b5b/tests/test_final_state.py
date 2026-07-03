# test_final_state.py

import os
import subprocess
import tempfile
import ast
import pytest

SCRIPT_PATH = "/home/user/sanitize.py"
CLEAN_CORPUS = "/home/user/corpus/clean"
EVIL_CORPUS = "/home/user/corpus/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "Evil corpus is empty."

    bypassed = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for evil_file in evil_files:
            input_path = os.path.join(EVIL_CORPUS, evil_file)
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--input", input_path, "--outdir", temp_dir],
                capture_output=True
            )

            output_file = os.path.join(temp_dir, f"{os.path.splitext(evil_file)[0]}.html")

            if result.returncode != 1 or os.path.exists(output_file):
                bypassed.append(evil_file)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "Clean corpus is empty."

    modified = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for clean_file in clean_files:
            input_path = os.path.join(CLEAN_CORPUS, clean_file)
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--input", input_path, "--outdir", temp_dir],
                capture_output=True
            )

            output_file = os.path.join(temp_dir, f"{os.path.splitext(clean_file)[0]}.html")

            if result.returncode != 0 or not os.path.exists(output_file):
                modified.append(clean_file)

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified/failed: {', '.join(modified)}"

def test_atomic_writes_ast():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    found_atomic = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ("rename", "replace") and getattr(node.func.value, "id", "") == "os":
                    found_atomic = True
                    break
            elif isinstance(node.func, ast.Name):
                if node.func.id in ("rename", "replace"):
                    found_atomic = True
                    break
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if "tempfile" in alias.name:
                    found_atomic = True
                    break

    assert found_atomic, "Could not verify atomic writes: no os.rename/os.replace or tempfile usage found in AST."