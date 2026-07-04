# test_final_state.py
import os
import tarfile
import shutil

def test_clean_docs_tar_gz():
    agent_out = "/home/user/clean_docs.tar.gz"
    gt_dir = "/app/ground_truth_docs"
    extract_dir = "/tmp/eval_agent_docs"

    assert os.path.exists(agent_out), f"Expected output file not found: {agent_out}"

    try:
        with tarfile.open(agent_out, "r:gz") as tar:
            tar.extractall(path=extract_dir)
    except Exception as e:
        assert False, f"Failed to extract {agent_out}: {e}"

    matched_files = 0
    total_files = 0

    for root, dirs, files in os.walk(gt_dir):
        for f in files:
            total_files += 1
            gt_path = os.path.join(root, f)
            rel_path = os.path.relpath(gt_path, gt_dir)
            agent_path = os.path.join(extract_dir, "docs_raw", rel_path)

            if os.path.exists(agent_path):
                with open(gt_path, 'rb') as f1, open(agent_path, 'rb') as f2:
                    if f1.read() == f2.read():
                        matched_files += 1

    # Check for symlink loops
    loop_penalty = 0
    for root, dirs, files in os.walk(extract_dir):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if os.path.islink(dir_path):
                target = os.readlink(dir_path)
                # Simple check if it points to itself or parent
                if target in ['.', '..'] or os.path.abspath(os.path.join(root, target)) == os.path.abspath(root):
                    loop_penalty += 0.5

    score = (matched_files / total_files) if total_files > 0 else 0
    score -= loop_penalty

    assert score >= 0.95, f"Directory similarity score {score} is below threshold 0.95. Matched {matched_files}/{total_files} files."