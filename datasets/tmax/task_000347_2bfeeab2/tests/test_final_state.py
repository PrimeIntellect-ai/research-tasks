# test_final_state.py
import os
import subprocess
import tempfile
import random
import shutil
import pytest

FILTER_SCRIPT = "/home/user/filter_pdbs.py"
CALC_SCRIPT = "/home/user/calc_com.py"
CLEAN_CORPUS = "/app/tests/corpus/clean"
EVIL_CORPUS = "/app/tests/corpus/evil"

def run_filter_script(input_dir, output_dir):
    try:
        # Assuming the student created a venv at /home/user/venv
        python_bin = "/home/user/venv/bin/python"
        if not os.path.exists(python_bin):
            python_bin = "python3"
        subprocess.run(
            [python_bin, FILTER_SCRIPT, input_dir, output_dir],
            check=True,
            capture_output=True,
            text=True,
            timeout=60
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"filter_pdbs.py failed: {e.stderr}")

def test_filter_pdbs_clean_corpus():
    assert os.path.isfile(FILTER_SCRIPT), f"Missing {FILTER_SCRIPT}"

    with tempfile.TemporaryDirectory() as out_dir:
        run_filter_script(CLEAN_CORPUS, out_dir)

        expected_files = set(os.listdir(CLEAN_CORPUS))
        actual_files = set(os.listdir(out_dir))

        missing = expected_files - actual_files
        assert not missing, f"{len(missing)} of {len(expected_files)} clean files were incorrectly rejected: {list(missing)[:5]}"

def test_filter_pdbs_evil_corpus():
    assert os.path.isfile(FILTER_SCRIPT), f"Missing {FILTER_SCRIPT}"

    with tempfile.TemporaryDirectory() as out_dir:
        run_filter_script(EVIL_CORPUS, out_dir)

        actual_files = set(os.listdir(out_dir))
        expected_files = set(os.listdir(EVIL_CORPUS))

        assert not actual_files, f"{len(actual_files)} of {len(expected_files)} evil files bypassed the filter: {list(actual_files)[:5]}"

def test_calc_com_determinism():
    assert os.path.isfile(CALC_SCRIPT), f"Missing {CALC_SCRIPT}"

    # Generate a dummy PDB file with 10,000 atoms
    lines = []
    for i in range(1, 10001):
        x, y, z = random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100)
        # Standard PDB ATOM format (simplified)
        lines.append(f"ATOM  {i:5d}  CA  ALA A   1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C  \n")

    python_bin = "/home/user/venv/bin/python"
    if not os.path.exists(python_bin):
        python_bin = "python3"

    outputs = []
    with tempfile.TemporaryDirectory() as tmpdir:
        pdb_path = os.path.join(tmpdir, "test.pdb")

        for _ in range(10):
            random.shuffle(lines)
            with open(pdb_path, "w") as f:
                f.writelines(lines)

            try:
                res = subprocess.run(
                    [python_bin, CALC_SCRIPT, pdb_path],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                outputs.append(res.stdout.strip())
            except subprocess.CalledProcessError as e:
                pytest.fail(f"calc_com.py failed: {e.stderr}")

    # Check that all outputs are identical
    unique_outputs = set(outputs)
    assert len(unique_outputs) == 1, f"calc_com.py is not deterministic. Got multiple different outputs for shuffled coordinates: {list(unique_outputs)}"