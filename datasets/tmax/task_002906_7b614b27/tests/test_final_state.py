# test_final_state.py
import os
import subprocess
import tempfile
from pathlib import Path
import numpy as np

def test_extracted_signal():
    """Validates that the extracted signal file has 100 lines of correct average intensities."""
    signal_file = Path("/home/user/extracted_signal.txt")
    assert signal_file.exists(), f"Extracted signal file missing: {signal_file}"

    with open(signal_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 100, f"Expected exactly 100 lines in {signal_file}, found {len(lines)}."

    # Recompute the expected average intensities using ffmpeg to dump raw grayscale video
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_bin_path = os.path.join(tmpdir, "raw.bin")
        subprocess.check_call([
            "ffmpeg", "-y", "-i", "/app/sequencer_run.mp4",
            "-f", "rawvideo", "-pix_fmt", "gray", raw_bin_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        with open(raw_bin_path, "rb") as f:
            raw_data = f.read()

    # Video is 100 frames of 100x100 pixels
    frame_size = 100 * 100
    assert len(raw_data) == 100 * frame_size, "Unexpected raw video size."

    expected_means = []
    for i in range(100):
        frame_data = raw_data[i * frame_size : (i + 1) * frame_size]
        mean_val = sum(frame_data) / frame_size
        expected_means.append(mean_val)

    for idx, (actual_str, expected) in enumerate(zip(lines, expected_means)):
        try:
            actual = float(actual_str)
        except ValueError:
            assert False, f"Line {idx+1} is not a valid float: '{actual_str}'"

        assert abs(actual - expected) < 1.0, (
            f"Intensity mismatch at frame {idx+1}: expected approx {expected:.2f}, got {actual:.2f}"
        )

def test_kl_divergence_fuzz():
    """Fuzz tests the agent's bash script against the oracle binary for equivalence."""
    script_path = "/home/user/kl_divergence.sh"
    oracle_path = "/app/oracle_kl"

    assert os.path.exists(script_path), f"Agent script missing: {script_path}"
    assert os.path.exists(oracle_path), f"Oracle binary missing: {oracle_path}"

    np.random.seed(42)

    for i in range(100):
        n = np.random.randint(10, 101)
        p = np.random.randint(0, 1001, size=n)
        q = np.random.randint(0, 1001, size=n)

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write('\n'.join(map(str, p)) + '\n')
            f1_name = f1.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write('\n'.join(map(str, q)) + '\n')
            f2_name = f2.name

        try:
            oracle_out = subprocess.check_output([oracle_path, f1_name, f2_name], text=True).strip()
            agent_out = subprocess.check_output(["bash", script_path, f1_name, f2_name], text=True).strip()

            assert oracle_out == agent_out, (
                f"Mismatch on fuzz iteration {i+1} (N={n}).\n"
                f"Oracle output: '{oracle_out}'\n"
                f"Agent output:  '{agent_out}'\n"
                f"Input P: {p[:5]}... (first 5 elements)\n"
                f"Input Q: {q[:5]}... (first 5 elements)"
            )
        finally:
            if os.path.exists(f1_name):
                os.remove(f1_name)
            if os.path.exists(f2_name):
                os.remove(f2_name)