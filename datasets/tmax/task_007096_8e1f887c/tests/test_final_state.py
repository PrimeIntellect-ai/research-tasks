# test_final_state.py
import os

def test_script_exists_and_executable():
    path = "/home/user/publish.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_script_uses_flock():
    path = "/home/user/publish.sh"
    with open(path, "r") as f:
        content = f.read()
    assert "flock" in content, "The script does not use 'flock' as required."

def test_markdown_contents():
    doc1_v1 = "/home/user/releases/v1.0/doc1.md"
    doc1_v2 = "/home/user/releases/v1.1/doc1.md"

    assert os.path.isfile(doc1_v1), f"{doc1_v1} does not exist."
    assert os.path.isfile(doc1_v2), f"{doc1_v2} does not exist."

    with open(doc1_v1, "r") as f:
        lines1 = f.read().strip().split('\n')
    assert lines1[-1] == "Status: PUBLISHED", f"{doc1_v1} does not end with 'Status: PUBLISHED'"

    with open(doc1_v2, "r") as f:
        content2 = f.read()
        lines2 = content2.strip().split('\n')
    assert lines2[-1] == "Status: PUBLISHED", f"{doc1_v2} does not end with 'Status: PUBLISHED'"
    assert "Extra line" in content2, f"{doc1_v2} does not contain 'Extra line'"

def test_hardlinks():
    img1_v1 = "/home/user/releases/v1.0/img1.png"
    img1_v2 = "/home/user/releases/v1.1/img1.png"

    assert os.path.isfile(img1_v1), f"{img1_v1} does not exist."
    assert os.path.isfile(img1_v2), f"{img1_v2} does not exist."

    stat1 = os.stat(img1_v1)
    stat2 = os.stat(img1_v2)

    assert stat1.st_ino == stat2.st_ino, f"{img1_v1} and {img1_v2} are not hardlinked (different inodes)."

def test_img2_exists():
    img2_v1 = "/home/user/releases/v1.0/img2.png"
    img2_v2 = "/home/user/releases/v1.1/img2.png"

    assert not os.path.exists(img2_v1), f"{img2_v1} should not exist in v1.0 release."
    assert os.path.isfile(img2_v2), f"{img2_v2} does not exist in v1.1 release."

def test_symlink_latest():
    latest = "/home/user/releases/latest"
    assert os.path.islink(latest), f"{latest} is not a symlink."

    target = os.path.realpath(latest)
    expected_target = "/home/user/releases/v1.1"

    assert target == expected_target, f"Symlink {latest} points to {target}, expected {expected_target}."