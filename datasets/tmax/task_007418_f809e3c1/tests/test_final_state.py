# test_final_state.py
import os

def test_wal_summary_contents():
    summary_path = "/home/user/wal_summary.txt"
    assert os.path.exists(summary_path), f"Summary file missing: {summary_path}"

    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "/home/user/dataset/file_a.wal: 4\n"
        "/home/user/dataset/subdir1/file_b.wal: 13\n"
        "/home/user/dataset/subdir1/subdir2/file_d.wal: 1\n"
        "/home/user/dataset/subdir3/file_c.wal: 0"
    )

    assert content == expected_content, (
        f"Content of {summary_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\nGot:\n{content}"
    )