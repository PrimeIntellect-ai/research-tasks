# test_final_state.py
import os
import json

def test_json_output():
    json_path = "/home/user/config_inventory.json"
    assert os.path.isfile(json_path), f"Output file {json_path} is missing."

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    assert "clusters" in data, "JSON missing 'clusters' key."
    clusters = data["clusters"]
    assert isinstance(clusters, list), "'clusters' must be a list."
    assert len(clusters) == 3, f"Expected 3 clusters, found {len(clusters)}."

    # Expected clusters data
    expected_clusters = [
        {
            "representative": "beta.conf",
            "members": ["alpha.conf", "beta.conf"]
        },
        {
            "representative": "delta.cfg",
            "members": ["delta.cfg", "gamma.cfg"]
        },
        {
            "representative": "epsilon.cfg",
            "members": ["epsilon.cfg"]
        }
    ]

    # Check sorting as required by the specification
    representatives = [c.get("representative") for c in clusters]
    assert representatives == sorted(representatives), "Clusters are not sorted alphabetically by representative."

    for c in clusters:
        members = c.get("members", [])
        assert members == sorted(members), f"Members in cluster {c.get('representative')} are not sorted alphabetically."

    # Check exact match
    assert clusters == expected_clusters, f"Clusters do not match expected output. Got: {clusters}"

def test_log_output():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_reads = {
        "[READ] alpha.conf",
        "[READ] beta.conf",
        "[READ] gamma.cfg",
        "[READ] delta.cfg",
        "[READ] epsilon.cfg"
    }

    actual_reads = set(line for line in lines if line.startswith("[READ]"))
    missing_reads = expected_reads - actual_reads
    assert not missing_reads, f"Missing [READ] logs for: {missing_reads}"

    cluster_lines = [line for line in lines if line.startswith("[CLUSTER]")]
    assert len(cluster_lines) >= 1, "Missing [CLUSTER] log line."
    assert cluster_lines[-1] == "[CLUSTER] Found 3 clusters", f"Expected '[CLUSTER] Found 3 clusters' at the end of clustering, got '{cluster_lines[-1]}'."