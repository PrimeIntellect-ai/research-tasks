# test_final_state.py

import os
import glob
import subprocess
import pytest

def get_script_path():
    scripts = glob.glob("/home/user/validate_backup.*")
    if not scripts:
        return None
    # Prefer executable ones
    executable_scripts = [s for s in scripts if os.path.isfile(s) and os.access(s, os.X_OK)]
    if executable_scripts:
        return executable_scripts[0]
    return scripts[0]

def run_script(script_path, file_path):
    if not os.access(script_path, os.X_OK):
        if script_path.endswith(".py"):
            return subprocess.run(["python3", script_path, file_path], capture_output=True)
        elif script_path.endswith(".sh"):
            return subprocess.run(["bash", script_path, file_path], capture_output=True)
        elif script_path.endswith(".js"):
            return subprocess.run(["node", script_path, file_path], capture_output=True)
    return subprocess.run([script_path, file_path], capture_output=True)

def test_clean_corpus_accepted():
    script_path = get_script_path()
    assert script_path is not None, "Executable script /home/user/validate_backup.* not found."

    clean_dir = "/app/corpus/clean/"
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, f"No clean JSON files found in {clean_dir}."

    failed_files = []
    for f in clean_files:
        result = run_script(script_path, f)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files rejected: {failed_files}"

def test_evil_corpus_rejected():
    script_path = get_script_path()
    assert script_path is not None, "Executable script /home/user/validate_backup.* not found."

    evil_dir = "/app/corpus/evil/"
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, f"No evil JSON files found in {evil_dir}."

    failed_files = []
    for f in evil_files:
        result = run_script(script_path, f)
        if result.returncode == 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {failed_files}"

def test_backup_schema_sql():
    schema_path = "/home/user/backup_schema.sql"
    assert os.path.isfile(schema_path), f"Schema file {schema_path} is missing."

    with open(schema_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    assert "create table" in content, "No CREATE TABLE statement found in the schema file."
    assert "index" in content, "No INDEX statement found in the schema file to optimize querying."