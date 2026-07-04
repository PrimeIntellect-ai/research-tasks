# test_final_state.py

import os
import glob
import json
import subprocess
import shutil
import pytest

SCRIPT_PATH = "/home/user/process_configs.py"
CLEAN_CORPUS_DIR = "/app/data/corpus/clean"
EVIL_CORPUS_DIR = "/app/data/corpus/evil"
EVAL_CLEAN_DIR = "/tmp/eval_clean"
EVAL_EVIL_DIR = "/tmp/eval_evil"
EXPECTED_LOAD_FACTOR = 0.85

@pytest.fixture(scope="session", autouse=True)
def run_agent_script():
    """Runs the agent's script on both corpora before running assertions."""
    assert os.path.exists(SCRIPT_PATH), f"Agent script not found at {SCRIPT_PATH}"

    # Prepare output directories
    for d in [EVAL_CLEAN_DIR, EVAL_EVIL_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    # Run on clean corpus
    clean_cmd = ["python3", SCRIPT_PATH, "--input-dir", CLEAN_CORPUS_DIR, "--output-dir", EVAL_CLEAN_DIR]
    clean_proc = subprocess.run(clean_cmd, capture_output=True, text=True)
    assert clean_proc.returncode == 0, f"Script failed on clean corpus. Stderr: {clean_proc.stderr}"

    # Run on evil corpus
    evil_cmd = ["python3", SCRIPT_PATH, "--input-dir", EVIL_CORPUS_DIR, "--output-dir", EVAL_EVIL_DIR]
    evil_proc = subprocess.run(evil_cmd, capture_output=True, text=True)
    assert evil_proc.returncode == 0, f"Script failed on evil corpus. Stderr: {evil_proc.stderr}"

def test_evil_corpus_rejected():
    evil_input_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))
    evil_output_files = glob.glob(os.path.join(EVAL_EVIL_DIR, "*.json"))

    bypassed_files = [os.path.basename(f) for f in evil_output_files]

    assert len(evil_output_files) == 0, (
        f"{len(evil_output_files)} of {len(evil_input_files)} evil files bypassed the filter: "
        f"{', '.join(bypassed_files)}"
    )

def test_clean_corpus_accepted_and_imputed():
    clean_input_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    clean_output_files = glob.glob(os.path.join(EVAL_CLEAN_DIR, "*.json"))

    input_basenames = set(os.path.basename(f) for f in clean_input_files)
    output_basenames = set(os.path.basename(f) for f in clean_output_files)

    missing_files = input_basenames - output_basenames
    assert not missing_files, (
        f"{len(missing_files)} of {len(clean_input_files)} clean files were incorrectly rejected: "
        f"{', '.join(missing_files)}"
    )

    # Check imputation logic
    invalid_imputations = []

    for basename in output_basenames:
        input_path = os.path.join(CLEAN_CORPUS_DIR, basename)
        output_path = os.path.join(EVAL_CLEAN_DIR, basename)

        with open(input_path, 'r') as f:
            input_data = json.load(f)
        with open(output_path, 'r') as f:
            output_data = json.load(f)

        input_dict = {rec["record_id"]: rec for rec in input_data}
        output_dict = {rec["record_id"]: rec for rec in output_data}

        for record_id, in_rec in input_dict.items():
            out_rec = output_dict.get(record_id)
            if not out_rec:
                invalid_imputations.append(f"{basename}: missing record {record_id}")
                continue

            if in_rec["load_factor"] is None:
                if out_rec.get("load_factor") != EXPECTED_LOAD_FACTOR:
                    invalid_imputations.append(
                        f"{basename}: record {record_id} load_factor not imputed correctly. "
                        f"Expected {EXPECTED_LOAD_FACTOR}, got {out_rec.get('load_factor')}"
                    )
            else:
                if out_rec.get("load_factor") != in_rec["load_factor"]:
                    invalid_imputations.append(
                        f"{basename}: record {record_id} load_factor modified incorrectly. "
                        f"Expected {in_rec['load_factor']}, got {out_rec.get('load_factor')}"
                    )

    assert not invalid_imputations, (
        f"Found {len(invalid_imputations)} imputation errors in clean files:\n" + 
        "\n".join(invalid_imputations[:10]) + 
        ("\n..." if len(invalid_imputations) > 10 else "")
    )