# test_final_state.py

import os
import subprocess
import ast
import tempfile
import pytest

def test_schema_version_txt():
    schema_file = "/home/user/schema_version.txt"
    assert os.path.exists(schema_file), f"Missing output artifact: {schema_file}"

    with open(schema_file, "r") as f:
        content = f.read().strip()

    assert content == "42", f"Expected schema version '42', but found '{content}' in {schema_file}"

def test_migrator_exists():
    migrator_script = "/home/user/migrator.py"
    assert os.path.exists(migrator_script), f"Missing migrator script: {migrator_script}"
    assert os.path.isfile(migrator_script), f"Path is not a file: {migrator_script}"

def test_migrator_evil_corpus():
    migrator_script = "/home/user/migrator.py"
    evil_dir = "/app/corpus/evil/"

    assert os.path.exists(evil_dir), f"Missing evil corpus directory: {evil_dir}"
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    bypassed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(evil_dir, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                ["python3", migrator_script, input_path, output_path],
                capture_output=True
            )

            if result.returncode != 1:
                bypassed_files.append(filename)

    assert not bypassed_files, (
        f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed rejection: "
        f"{', '.join(bypassed_files)}"
    )

def test_migrator_clean_corpus():
    migrator_script = "/home/user/migrator.py"
    clean_dir = "/app/corpus/clean/"

    assert os.path.exists(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    failed_files = []
    invalid_ast_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(clean_dir, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                ["python3", migrator_script, input_path, output_path],
                capture_output=True
            )

            if result.returncode != 0:
                failed_files.append(filename)
                continue

            if not os.path.exists(output_path):
                failed_files.append(filename)
                continue

            with open(output_path, "r") as f:
                output_code = f.read()

            try:
                ast.parse(output_code)
            except SyntaxError:
                invalid_ast_files.append(filename)

    error_msg = []
    if failed_files:
        error_msg.append(f"{len(failed_files)} of {len(clean_files)} clean files failed migration (non-zero exit code or missing output): {', '.join(failed_files)}")
    if invalid_ast_files:
        error_msg.append(f"{len(invalid_ast_files)} of {len(clean_files)} clean files resulted in invalid Python 3 code: {', '.join(invalid_ast_files)}")

    assert not failed_files and not invalid_ast_files, " | ".join(error_msg)