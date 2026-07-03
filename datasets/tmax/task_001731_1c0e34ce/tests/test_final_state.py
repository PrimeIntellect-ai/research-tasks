# test_final_state.py
import os
import subprocess
import tempfile
import json

def test_part1_keyframe_count():
    count_file = "/home/user/keyframe_count.txt"
    assert os.path.exists(count_file), f"Task 1 failed: {count_file} does not exist"
    with open(count_file, "r") as f:
        content = f.read().strip()
    assert content == "14", f"Task 1 failed: Expected keyframe count 14, but got '{content}'"

def test_part2_adversarial_filtering():
    script_path = "/home/user/sanitize_graphs.sh"
    assert os.path.exists(script_path), f"Task 2 failed: {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Task 2 failed: {script_path} is not executable"

    clean_corpus_dir = "/app/corpora/clean/"
    evil_corpus_dir = "/app/corpora/evil/"

    with tempfile.TemporaryDirectory() as temp_out_clean, tempfile.TemporaryDirectory() as temp_out_evil:
        # Run agent's script on clean corpus
        subprocess.run([script_path, clean_corpus_dir, temp_out_clean], check=False)

        # Run agent's script on evil corpus
        subprocess.run([script_path, evil_corpus_dir, temp_out_evil], check=False)

        clean_input_files = set(f for f in os.listdir(clean_corpus_dir) if f.endswith('.json'))
        clean_output_files = set(f for f in os.listdir(temp_out_clean) if f.endswith('.json'))

        evil_input_files = set(f for f in os.listdir(evil_corpus_dir) if f.endswith('.json'))
        evil_output_files = set(f for f in os.listdir(temp_out_evil) if f.endswith('.json'))

        clean_modified = []
        for f in clean_input_files:
            if f not in clean_output_files:
                clean_modified.append(f)
            else:
                # Check if content was preserved
                with open(os.path.join(clean_corpus_dir, f)) as f1, open(os.path.join(temp_out_clean, f)) as f2:
                    if f1.read() != f2.read():
                        clean_modified.append(f)

        evil_bypassed = list(evil_output_files)

        errors = []
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {len(evil_input_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            errors.append(f"{len(clean_modified)} of {len(clean_input_files)} clean modified/rejected: {', '.join(clean_modified)}")

        assert not errors, "Adversarial corpus failure: " + " | ".join(errors)

def test_part3_convert_script():
    script_path = "/home/user/convert.sh"
    assert os.path.exists(script_path), f"Task 3 failed: {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Task 3 failed: {script_path} is not executable"

    sample_json = {
        "nodes": [
            {"id": "n1"},
            {"id": "n2"},
            {"id": "n3"}
        ],
        "edges": [
            {"source": "n1", "target": "n2", "weight": 5},
            {"source": "n2", "target": "n3", "weight": 10}
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        json.dump(sample_json, tmp)
        tmp_path = tmp.name

    try:
        # Remove output files if they exist to ensure we are testing the current run
        for out_file in ["/home/user/export_relational.csv", "/home/user/export_document.jsonl", "/home/user/export_graph.dot"]:
            if os.path.exists(out_file):
                os.remove(out_file)

        subprocess.run([script_path, tmp_path], check=False)

        assert os.path.exists("/home/user/export_relational.csv"), "Task 3 failed: /home/user/export_relational.csv was not created"
        assert os.path.exists("/home/user/export_document.jsonl"), "Task 3 failed: /home/user/export_document.jsonl was not created"
        assert os.path.exists("/home/user/export_graph.dot"), "Task 3 failed: /home/user/export_graph.dot was not created"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)