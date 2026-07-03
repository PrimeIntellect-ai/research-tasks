# test_final_state.py
import os
import tarfile

def test_organizer_script_exists():
    script_path = "/home/user/organizer.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_completion_log():
    log_path = "/home/user/completion.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "DONE" in content, f"{log_path} does not contain the word 'DONE'."

def test_archives_exist():
    neuro_path = "/home/user/datasets/archives/neuro.tar.gz"
    vision_path = "/home/user/datasets/archives/vision.tar.gz"
    assert os.path.isfile(neuro_path), f"Archive {neuro_path} does not exist."
    assert os.path.isfile(vision_path), f"Archive {vision_path} does not exist."

def test_neuro_archive_contents():
    archive_path = "/home/user/datasets/archives/neuro.tar.gz"
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()

        data_a = [m for m in members if m.endswith("data_A.csv")]
        data_b = [m for m in members if m.endswith("data_B.csv")]

        assert data_a, "data_A.csv not found in neuro.tar.gz"
        assert data_b, "data_B.csv not found in neuro.tar.gz"

        f_a = tar.extractfile(data_a[0])
        assert f_a is not None, "Could not extract data_A.csv from neuro.tar.gz"
        assert b"DATA_A" in f_a.read(), "data_A.csv does not contain 'DATA_A'"

        f_b = tar.extractfile(data_b[0])
        assert f_b is not None, "Could not extract data_B.csv from neuro.tar.gz"
        assert b"DATA_B" in f_b.read(), "data_B.csv does not contain 'DATA_B'"

def test_vision_archive_contents():
    archive_path = "/home/user/datasets/archives/vision.tar.gz"
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()

        data_c = [m for m in members if m.endswith("data_C.csv")]
        assert data_c, "data_C.csv not found in vision.tar.gz"

        f_c = tar.extractfile(data_c[0])
        assert f_c is not None, "Could not extract data_C.csv from vision.tar.gz"
        assert b"DATA_C" in f_c.read(), "data_C.csv does not contain 'DATA_C'"

def test_hard_links_and_inodes():
    neuro_arch = "/home/user/datasets/archives/neuro.tar.gz"
    vision_arch = "/home/user/datasets/archives/vision.tar.gz"

    neuro_link1 = "/home/user/datasets/staging/neuro_run1.sym"
    neuro_link2 = "/home/user/datasets/staging/neuro_run2.sym"
    vision_link1 = "/home/user/datasets/staging/vision_run1.sym"

    links = [neuro_link1, neuro_link2, vision_link1]

    for link in links:
        assert os.path.exists(link), f"File {link} does not exist."
        assert not os.path.islink(link), f"File {link} is still a symbolic link, but should be a hard link."

    inode_neuro_arch = os.stat(neuro_arch).st_ino
    inode_neuro_link1 = os.stat(neuro_link1).st_ino
    inode_neuro_link2 = os.stat(neuro_link2).st_ino

    assert inode_neuro_arch == inode_neuro_link1, f"{neuro_link1} is not a hard link to {neuro_arch} (inodes differ)."
    assert inode_neuro_arch == inode_neuro_link2, f"{neuro_link2} is not a hard link to {neuro_arch} (inodes differ)."

    inode_vision_arch = os.stat(vision_arch).st_ino
    inode_vision_link1 = os.stat(vision_link1).st_ino

    assert inode_vision_arch == inode_vision_link1, f"{vision_link1} is not a hard link to {vision_arch} (inodes differ)."