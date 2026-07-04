# test_final_state.py

import os
import subprocess
import random
import pytest

def test_hetatm_count():
    pdb_path = "/app/target.pdb"
    output_path = "/home/user/hetatm_count.txt"

    assert os.path.isfile(pdb_path), f"Missing {pdb_path}"
    assert os.path.isfile(output_path), f"Missing {output_path}"

    expected_count = 0
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("HETATM"):
                expected_count += 1

    with open(output_path, 'r') as f:
        student_count_str = f.read().strip()

    assert student_count_str == str(expected_count), f"Expected HETATM count to be {expected_count}, but got {student_count_str}"

def test_frame_brightness_csv():
    video_path = "/app/spectroscopy_run.mp4"
    output_path = "/home/user/frame_brightness.csv"

    assert os.path.isfile(video_path), f"Missing {video_path}"
    assert os.path.isfile(output_path), f"Missing {output_path}"

    # Get video resolution
    ffprobe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", video_path
    ]
    res_output = subprocess.check_output(ffprobe_cmd, text=True).strip()
    width, height = map(int, res_output.split('x'))
    frame_size = width * height

    # Extract raw grayscale frames
    ffmpeg_cmd = [
        "ffmpeg", "-i", video_path,
        "-f", "image2pipe", "-pix_fmt", "gray", "-vcodec", "rawvideo", "-"
    ]
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw_video, _ = process.communicate()

    expected_csv_lines = []
    num_frames = len(raw_video) // frame_size
    for i in range(num_frames):
        frame_bytes = raw_video[i * frame_size : (i + 1) * frame_size]
        avg_brightness = sum(frame_bytes) / frame_size
        expected_csv_lines.append(f"{i},{avg_brightness:.1f}")

    with open(output_path, 'r') as f:
        student_lines = [line.strip() for line in f if line.strip()]

    assert len(student_lines) == len(expected_csv_lines), f"Expected {len(expected_csv_lines)} lines in CSV, got {len(student_lines)}"

    for i, (expected, student) in enumerate(zip(expected_csv_lines, student_lines)):
        assert student == expected, f"Mismatch at frame {i}: expected '{expected}', got '{student}'"

def test_fast_mc_sim_fuzzing():
    agent_script = "/home/user/fast_mc_sim.sh"
    oracle_bin = "/app/oracle_mc_sim"

    assert os.path.isfile(agent_script), f"Missing script at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Script at {agent_script} is not executable"
    assert os.path.isfile(oracle_bin), f"Missing oracle binary at {oracle_bin}"

    random.seed(42)
    num_iterations = 500

    for i in range(num_iterations):
        length = random.randint(10, 500)
        dna = "".join(random.choices(['A', 'C', 'G', 'T'], k=length))
        K = random.randint(10, 100)

        oracle_proc = subprocess.run([oracle_bin, dna, str(K)], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_script, dna, str(K)], capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {dna} {K}"
        assert agent_proc.returncode == 0, f"Agent script failed on input: {dna} {K}. Error: {agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Fuzzing mismatch on iteration {i+1}!\n"
            f"Input DNA: {dna}\n"
            f"Input K: {K}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )