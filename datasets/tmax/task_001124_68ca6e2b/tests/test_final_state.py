# test_final_state.py
import os
import subprocess
import random
import tempfile
import pytest

def test_frames_extracted():
    """Check that frames have been extracted to /home/user/frames with correct size."""
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Frames directory missing: {frames_dir}"

    files = [f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".bin")]
    assert len(files) >= 2, "At least two frames should have been extracted."

    for f in files:
        path = os.path.join(frames_dir, f)
        assert os.path.getsize(path) == 4096, f"Frame {f} is not exactly 4096 bytes."

def test_fuzz_equivalence():
    """Fuzz equivalence test: compare agent's hasher with oracle hasher on random inputs."""
    agent_bin = "/home/user/frame_hasher"
    oracle_bin = "/app/oracle_hasher"

    assert os.path.isfile(agent_bin), f"Agent binary missing: {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary not executable: {agent_bin}"
    assert os.path.isfile(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "input1.bin")
        file2 = os.path.join(tmpdir, "input2.bin")

        for i in range(500):
            data1 = bytes([random.randint(0, 255) for _ in range(4096)])
            data2 = bytes([random.randint(0, 255) for _ in range(4096)])

            with open(file1, "wb") as f1, open(file2, "wb") as f2:
                f1.write(data1)
                f2.write(data2)

            agent_proc = subprocess.run([agent_bin, file1, file2], capture_output=True, text=True)
            oracle_proc = subprocess.run([oracle_bin, file1, file2], capture_output=True, text=True)

            assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on iteration {i}"
            assert agent_proc.stdout == oracle_proc.stdout, f"Output mismatch on iteration {i}.\nOracle:\n{oracle_proc.stdout}\nAgent:\n{agent_proc.stdout}"

def test_sample_output():
    """Check that sample_output.txt exists and matches the oracle output for frame_001.bin and frame_002.bin."""
    sample_out = "/home/user/sample_output.txt"
    assert os.path.isfile(sample_out), f"Sample output missing: {sample_out}"

    frame1 = "/home/user/frames/frame_001.bin"
    frame2 = "/home/user/frames/frame_002.bin"

    assert os.path.isfile(frame1), f"Missing {frame1}"
    assert os.path.isfile(frame2), f"Missing {frame2}"

    oracle_bin = "/app/oracle_hasher"
    oracle_proc = subprocess.run([oracle_bin, frame1, frame2], capture_output=True, text=True)

    with open(sample_out, "r") as f:
        student_out = f.read()

    assert student_out.strip() == oracle_proc.stdout.strip(), "Sample output content does not match expected oracle output."