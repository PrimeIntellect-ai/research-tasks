# test_final_state.py
import os
import shutil
import tempfile
import subprocess
import json

def test_part1_audio_extraction():
    root_info_path = "/home/user/root_info.txt"
    assert os.path.isfile(root_info_path), f"File missing: {root_info_path}"

    with open(root_info_path, "r") as f:
        content = f.read().strip()

    expected_content = "Root: Gamma, Score: 82"
    assert content == expected_content, f"Expected '{expected_content}', but got '{content}'"

def test_part2_adversarial_graph_filter():
    script_path = "/home/user/graph_filter.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"

    clean_corpus_dir = "/app/corpus/clean"
    evil_corpus_dir = "/app/corpus/evil"

    clean_files = os.listdir(clean_corpus_dir) if os.path.isdir(clean_corpus_dir) else []
    evil_files = os.listdir(evil_corpus_dir) if os.path.isdir(evil_corpus_dir) else []

    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        # Copy clean files
        for f in clean_files:
            shutil.copy(os.path.join(clean_corpus_dir, f), os.path.join(input_dir, f"clean_{f}"))

        # Copy evil files
        for f in evil_files:
            shutil.copy(os.path.join(evil_corpus_dir, f), os.path.join(input_dir, f"evil_{f}"))

        # Run the agent's script
        result = subprocess.run(
            ["python3", script_path, input_dir, output_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

        output_files = set(os.listdir(output_dir))

        # Check clean files
        clean_modified = []
        for f in clean_files:
            target_name = f"clean_{f}"
            if target_name not in output_files:
                clean_modified.append(target_name)
            else:
                # Compare content
                with open(os.path.join(clean_corpus_dir, f), "r") as orig_f:
                    orig_data = json.load(orig_f)
                with open(os.path.join(output_dir, target_name), "r") as out_f:
                    try:
                        out_data = json.load(out_f)
                        if orig_data != out_data:
                            clean_modified.append(target_name)
                    except json.JSONDecodeError:
                        clean_modified.append(target_name)

        # Check evil files
        evil_bypassed = []
        for f in evil_files:
            target_name = f"evil_{f}"
            if target_name in output_files:
                evil_bypassed.append(target_name)

        errors = []
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified or missing: {', '.join(clean_modified)}")

        if errors:
            assert False, " | ".join(errors)