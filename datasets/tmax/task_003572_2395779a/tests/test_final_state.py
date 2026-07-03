# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_networkx_perturbation_fixed():
    unweighted_path = "/app/networkx-source/networkx/algorithms/shortest_paths/unweighted.py"
    assert os.path.isfile(unweighted_path), f"File {unweighted_path} is missing."

    with open(unweighted_path, "r") as f:
        content = f.read()

    assert "cutoff -= 1" not in content, f"The deliberate perturbation 'cutoff -= 1' is still present in {unweighted_path}."

def test_detector_script_exists():
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script {detector_path} does not exist."

def test_detector_evil_corpus():
    detector_path = "/home/user/detector.py"
    evil_path = "/home/user/corpora/evil/"

    evil_dbs = glob.glob(os.path.join(evil_path, "*.db")) + glob.glob(os.path.join(evil_path, "*.sqlite"))
    assert len(evil_dbs) > 0, f"No databases found in {evil_path}."

    failed_dbs = []
    for db in evil_dbs:
        env = os.environ.copy()
        env["PYTHONPATH"] = "/app/networkx-source" + (":" + env["PYTHONPATH"] if "PYTHONPATH" in env else "")
        result = subprocess.run(["python3", detector_path, db], capture_output=True, text=True, env=env)
        output = result.stdout.strip()
        if output != "EVIL":
            failed_dbs.append((os.path.basename(db), output))

    if failed_dbs:
        pytest.fail(f"{len(failed_dbs)} of {len(evil_dbs)} evil bypassed. Offending files: " + 
                    ", ".join([f"{name} (output: {out})" for name, out in failed_dbs]))

def test_detector_clean_corpus():
    detector_path = "/home/user/detector.py"
    clean_path = "/home/user/corpora/clean/"

    clean_dbs = glob.glob(os.path.join(clean_path, "*.db")) + glob.glob(os.path.join(clean_path, "*.sqlite"))
    assert len(clean_dbs) > 0, f"No databases found in {clean_path}."

    failed_dbs = []
    for db in clean_dbs:
        env = os.environ.copy()
        env["PYTHONPATH"] = "/app/networkx-source" + (":" + env["PYTHONPATH"] if "PYTHONPATH" in env else "")
        result = subprocess.run(["python3", detector_path, db], capture_output=True, text=True, env=env)
        output = result.stdout.strip()
        if output != "CLEAN":
            failed_dbs.append((os.path.basename(db), output))

    if failed_dbs:
        pytest.fail(f"{len(failed_dbs)} of {len(clean_dbs)} clean modified/flagged. Offending files: " + 
                    ", ".join([f"{name} (output: {out})" for name, out in failed_dbs]))