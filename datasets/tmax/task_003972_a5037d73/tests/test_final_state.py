# test_final_state.py

import os
import subprocess
import pytest

def get_ground_truth(test_dir):
    """
    Re-derive the ground truth by checking the criteria for each file in the test directory:
    a) Valid 64-bit ELF executable
    b) Dynamically imports `system` or `popen`
    c) Contains the plaintext string `HTTP_USER_AGENT`
    """
    gt = set()
    if not os.path.isdir(test_dir):
        return gt

    for fname in os.listdir(test_dir):
        fpath = os.path.join(test_dir, fname)
        if not os.path.isfile(fpath):
            continue

        # a) Check if it is a valid 64-bit ELF
        try:
            with open(fpath, 'rb') as f:
                header = f.read(5)
                if header != b'\x7fELF\x02':
                    continue
        except Exception:
            continue

        # b) Check dynamic imports for system or popen
        try:
            dyn = subprocess.run(['readelf', '-W', '--dyn-syms', fpath], capture_output=True, text=True)
            # Look for system or popen in the dynamic symbols output
            if not (' system@' in dyn.stdout or ' popen@' in dyn.stdout or 
                    ' system ' in dyn.stdout or ' popen ' in dyn.stdout):
                continue
        except Exception:
            continue

        # c) Check for plaintext string HTTP_USER_AGENT
        try:
            strs = subprocess.run(['strings', fpath], capture_output=True, text=True)
            if 'HTTP_USER_AGENT' not in strs.stdout:
                continue
        except Exception:
            continue

        gt.add(fname)

    return gt

def test_evidence_extracted():
    evidence_dir = "/home/user/evidence"
    assert os.path.isdir(evidence_dir), f"Directory {evidence_dir} does not exist. Did you extract the evidence.zip file?"

    files = os.listdir(evidence_dir)
    assert len(files) > 0, f"Directory {evidence_dir} is empty. Evidence files were not extracted properly."

def test_scan_cgi_f1_score():
    agent_script = "/home/user/scan_cgi.sh"
    test_dir = "/app/hidden_test"

    assert os.path.isfile(agent_script), f"Script not found at {agent_script}"
    assert os.path.isdir(test_dir), f"Hidden test directory not found at {test_dir}"

    # Compute ground truth
    ground_truth_set = get_ground_truth(test_dir)
    assert len(ground_truth_set) > 0, "Ground truth set is empty. Check the hidden test directory setup."

    # Run agent script
    try:
        result = subprocess.run(['bash', agent_script, test_dir], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        pytest.fail("The script execution timed out after 60 seconds.")
    except Exception as e:
        pytest.fail(f"Failed to execute the script: {e}")

    # Parse predictions
    predicted = set(result.stdout.strip().split('\n'))
    predicted = {p.strip() for p in predicted if p.strip()}

    # Calculate metrics
    tp = len(predicted & ground_truth_set)
    fp = len(predicted - ground_truth_set)
    fn = len(ground_truth_set - predicted)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.95, (
        f"F1 Score {f1:.4f} is below the threshold of 0.95.\n"
        f"True Positives: {tp}, False Positives: {fp}, False Negatives: {fn}\n"
        f"Precision: {precision:.4f}, Recall: {recall:.4f}"
    )