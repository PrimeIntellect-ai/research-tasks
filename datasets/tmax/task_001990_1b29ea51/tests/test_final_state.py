# test_final_state.py
import json
import numpy as np
import subprocess
import os
import pytest

def test_rust_compiled():
    """Verify that the Rust project was compiled successfully."""
    assert os.path.exists("/home/user/video_processor/target/release/video_processor"), \
        "The Rust application was not compiled to /home/user/video_processor/target/release/video_processor"

def test_c_lib_compiled():
    """Verify that the C library was compiled into a shared object."""
    assert os.path.exists("/home/user/video_processor/c_src/libintensity.so"), \
        "The shared library libintensity.so was not generated in /home/user/video_processor/c_src"

def test_constants_encoding():
    """Verify that constants.rs is now valid UTF-8."""
    try:
        with open("/home/user/video_processor/src/constants.rs", "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError:
        pytest.fail("src/constants.rs is still not valid UTF-8")

def test_python_property_tests():
    """Verify that the Python property tests were written."""
    test_path = "/home/user/py_src/test_processor.py"
    assert os.path.exists(test_path), f"{test_path} is missing"

    with open(test_path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "The test file does not seem to use 'hypothesis'"
    assert "pytest" in content or "test_" in content, "The test file does not seem to be a pytest file"

def test_intensities_mse():
    """Compute the MSE between the agent's output and the ground truth, and assert it is <= 2.0."""
    output_path = "/home/user/output_intensities.json"
    assert os.path.exists(output_path), f"Output file {output_path} is missing"

    # Compute Ground Truth dynamically
    temp_dir = "/tmp/gt_frames"
    os.makedirs(temp_dir, exist_ok=True)
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", "/app/test_video.mp4", "-r", "5", 
            "-vf", "scale=320:240,format=gray", 
            "-f", "image2", "-c:v", "rawvideo", f"{temp_dir}/frame_%04d.raw"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to extract frames from /app/test_video.mp4 using ffmpeg")

    gt_intensities = []
    for file in sorted(os.listdir(temp_dir)):
        if file.endswith(".raw"):
            data = np.fromfile(os.path.join(temp_dir, file), dtype=np.uint8)
            gt_intensities.append(float(np.mean(data)))

    # Load Agent's Output
    try:
        with open(output_path, "r") as f:
            agent_intensities = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Output file {output_path} is not valid JSON")

    assert isinstance(agent_intensities, list), f"Output file {output_path} must contain a JSON array"

    # Calculate MSE
    min_len = min(len(gt_intensities), len(agent_intensities))
    assert min_len > 0, "No frames were processed or ground truth is empty"

    gt_arr = np.array(gt_intensities[:min_len])
    agent_arr = np.array(agent_intensities[:min_len])

    mse = np.mean((gt_arr - agent_arr) ** 2)

    # Penalty if lengths mismatch significantly
    if abs(len(gt_intensities) - len(agent_intensities)) > 2:
        mse += 1000.0

    assert mse <= 2.0, f"MSE is {mse}, which exceeds the threshold of 2.0"