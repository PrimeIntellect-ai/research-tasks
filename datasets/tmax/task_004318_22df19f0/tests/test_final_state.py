# test_final_state.py
import os
import subprocess
import tempfile
import random
import numpy as np
from PIL import Image

def test_valid_frames_count():
    count_file = '/home/user/valid_frames.txt'
    assert os.path.exists(count_file), f"The file {count_file} does not exist."

    with open(count_file, 'r') as f:
        content = f.read().strip()

    assert content == '7', f"Expected '7' valid frames in {count_file}, but got '{content}'."

def test_analyze_frame_fuzz_equivalence():
    agent_script = '/home/user/analyze_frame.py'
    oracle_script = '/tmp/oracle_analyze_frame.py'

    assert os.path.exists(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} is missing."

    np.random.seed(42)
    random.seed(42)

    num_iterations = 100

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(num_iterations):
            # 30% flat/low-variance, 70% random noise
            is_flat = i < 30
            if is_flat:
                base_color = np.random.randint(0, 256)
                # Add low variance noise (std < 5.0)
                noise = np.random.normal(0, 2.0, (64, 64))
                arr = np.clip(base_color + noise, 0, 255).astype(np.uint8)
            else:
                arr = np.random.randint(0, 256, (64, 64), dtype=np.uint8)

            mode = random.choice(['L', 'RGB'])
            if mode == 'RGB':
                # Replicate grayscale values across 3 channels for RGB
                arr = np.stack([arr]*3, axis=-1)

            img = Image.fromarray(arr, mode=mode)
            img_path = os.path.join(tmpdir, f"test_{i}.png")
            img.save(img_path)

            agent_res = subprocess.run(
                ['python3', agent_script, img_path], 
                capture_output=True, text=True
            )
            oracle_res = subprocess.run(
                ['python3', oracle_script, img_path], 
                capture_output=True, text=True
            )

            assert agent_res.returncode == 0, f"Agent script failed on image {i}:\n{agent_res.stderr}"
            assert oracle_res.returncode == 0, f"Oracle script failed on image {i}:\n{oracle_res.stderr}"

            agent_out = agent_res.stdout.strip()
            oracle_out = oracle_res.stdout.strip()

            assert agent_out == oracle_out, (
                f"Output mismatch on image {i} (is_flat={is_flat}, mode={mode}).\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output:  {agent_out}"
            )