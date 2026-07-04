# test_final_state.py
import os
import shutil
import subprocess
import tempfile

def test_rust_bug_txt():
    bug_file = "/home/user/project/rust_bug.txt"
    assert os.path.isfile(bug_file), f"File {bug_file} does not exist."
    with open(bug_file, 'r') as f:
        content = f.read().lower()

    keywords = ["clone", "moved", "reference", "copy"]
    assert any(word in content for word in keywords), \
        f"{bug_file} does not contain a valid explanation of the ownership bug (missing expected keywords)."

def test_organizer_executable():
    organizer = "/home/user/project/organizer.sh"
    assert os.path.isfile(organizer), f"Script {organizer} does not exist."
    assert os.access(organizer, os.X_OK), f"Script {organizer} is not executable."

def test_test_organizer_executable_and_passes():
    test_script = "/home/user/project/test_organizer.sh"
    assert os.path.isfile(test_script), f"Test script {test_script} does not exist."
    assert os.access(test_script, os.X_OK), f"Test script {test_script} is not executable."

    result = subprocess.run([test_script], capture_output=True, text=True)
    assert result.returncode == 0, f"{test_script} failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_organizer_logic():
    organizer = "/home/user/project/organizer.sh"
    queues_dir = "/home/user/project/queues"

    # Clean queues dir
    if os.path.exists(queues_dir):
        shutil.rmtree(queues_dir)
    os.makedirs(queues_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create 7 files
        for c in "abcdefg":
            with open(os.path.join(temp_dir, f"file_{c}.txt"), 'w') as f:
                f.write("test")

        result = subprocess.run([organizer, temp_dir], capture_output=True, text=True)
        assert result.returncode == 0, f"{organizer} failed when tested independently.\nStderr: {result.stderr}"

        q1 = os.path.join(queues_dir, "queue_1")
        q2 = os.path.join(queues_dir, "queue_2")

        assert os.path.isdir(q1), "queue_1 was not created by organizer.sh."
        assert os.path.isdir(q2), "queue_2 was not created by organizer.sh."

        q1_files = os.listdir(q1)
        q2_files = os.listdir(q2)

        assert len(q1_files) == 5, f"queue_1 should have exactly 5 files, but has {len(q1_files)}."
        assert len(q2_files) == 2, f"queue_2 should have exactly 2 files, but has {len(q2_files)}."