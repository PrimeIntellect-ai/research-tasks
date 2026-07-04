# test_final_state.py
import os
import json
import stat

MANIFEST_PATH = "/home/user/artifact_manifest.csv"
MOCK_DIR = "/home/user/mock_artifacts"
REPORT_PATH = "/home/user/security_report.json"

def get_manifest_data():
    if not os.path.exists(MANIFEST_PATH):
        return []
    data = []
    with open(MANIFEST_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 3:
                data.append({
                    "artifact": parts[0],
                    "size": int(parts[1]),
                    "octal": parts[2]
                })
    return data

def test_mock_artifacts_directory_exists():
    assert os.path.isdir(MOCK_DIR), f"Directory {MOCK_DIR} does not exist."

def test_mock_artifacts_files_created_correctly():
    manifest_data = get_manifest_data()
    assert manifest_data, f"Manifest file {MANIFEST_PATH} is empty or missing."

    for item in manifest_data:
        file_path = os.path.join(MOCK_DIR, item["artifact"])
        assert os.path.isfile(file_path), f"Artifact file {file_path} was not created."

        # Check size
        actual_size = os.path.getsize(file_path)
        assert actual_size == item["size"], f"File {file_path} has size {actual_size}, expected {item['size']}."

        # Check permissions
        st = os.stat(file_path)
        actual_mode = stat.S_IMODE(st.st_mode)
        expected_mode = int(item["octal"], 8)
        assert actual_mode == expected_mode, f"File {file_path} has mode {oct(actual_mode)}, expected {oct(expected_mode)}."

def test_security_report_json():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {REPORT_PATH} is not valid JSON."

    assert isinstance(report_data, list), f"JSON root in {REPORT_PATH} must be a list."

    manifest_data = get_manifest_data()
    assert manifest_data, f"Manifest file {MANIFEST_PATH} is empty or missing."

    expected_scores = {}
    for item in manifest_data:
        size = item["size"]
        decimal_mode = int(item["octal"], 8)
        score = ((size ^ decimal_mode) * 13) % 97
        expected_scores[item["artifact"]] = score

    actual_scores = {}
    for entry in report_data:
        assert isinstance(entry, dict), f"Report entry {entry} is not a JSON object."
        assert "artifact" in entry, f"Report entry {entry} missing 'artifact' key."
        assert "score" in entry, f"Report entry {entry} missing 'score' key."
        actual_scores[entry["artifact"]] = entry["score"]

    for artifact, expected_score in expected_scores.items():
        assert artifact in actual_scores, f"Artifact '{artifact}' missing from security report."
        assert actual_scores[artifact] == expected_score, f"Artifact '{artifact}' has score {actual_scores[artifact]}, expected {expected_score}."