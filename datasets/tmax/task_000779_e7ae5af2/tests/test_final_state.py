# test_final_state.py
import json
import os
import pytest

def test_audit_report_accuracy():
    submission_path = "/home/user/audit_report.json"
    truth_path = "/app/truth.json"

    assert os.path.exists(submission_path), f"Submission file not found at {submission_path}"
    assert os.path.exists(truth_path), f"Truth file not found at {truth_path}"

    try:
        with open(submission_path, "r") as f:
            submission = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not parse submission JSON at {submission_path}: {e}")

    try:
        with open(truth_path, "r") as f:
            truth = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not parse truth JSON at {truth_path}: {e}")

    score = 0
    total = len(truth) * 4 # 4 fields per server

    for server, t_data in truth.items():
        s_data = None
        # Allow case-insensitive matching for server names due to transcription variance
        for k in submission.keys():
            if server.lower() in k.lower():
                s_data = submission[k]
                break

        if s_data:
            if s_data.get("certificate_file") == t_data["certificate_file"]: 
                score += 1

            s_fingerprint = str(s_data.get("full_sha256_fingerprint", "")).lower()
            t_fingerprint_suffix = t_data["full_sha256_fingerprint"][-4:].lower()
            if s_fingerprint.endswith(t_fingerprint_suffix): 
                score += 1

            if s_data.get("chain_valid") == t_data["chain_valid"]: 
                score += 1

            try:
                if int(s_data.get("cwe_id", 0)) == t_data["cwe_id"]: 
                    score += 1
            except (ValueError, TypeError):
                pass

    accuracy = score / total
    assert accuracy >= 0.85, f"Accuracy {accuracy:.2f} is below the threshold of 0.85 (Score: {score}/{total}). Please ensure server names, certificates, fingerprints, chain validity, and CWE IDs are correctly identified."