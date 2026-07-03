# test_final_state.py

import os
import numpy as np
import cv2

def test_best_sim_mode_similarity():
    video_path = '/app/thermal_diffusion.mp4'
    agent_output_path = '/home/user/best_sim_mode.npy'

    assert os.path.exists(video_path), f"Video file missing: {video_path}"
    assert os.path.exists(agent_output_path), f"Agent output missing: {agent_output_path}"

    # Compute Ground Truth Reference
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret: 
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray.flatten() / 255.0)
    cap.release()

    assert len(frames) > 0, "Video contains no frames."

    X = np.column_stack(frames)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    u_ref = U[:, 0]
    u_ref = u_ref / np.linalg.norm(u_ref)

    # Load Agent Output
    try:
        u_agent = np.load(agent_output_path).flatten()
        u_agent = u_agent / np.linalg.norm(u_agent)
        similarity = np.abs(np.dot(u_ref, u_agent))
    except Exception as e:
        assert False, f"Failed to load or process {agent_output_path}: {e}"

    assert similarity >= 0.95, f"Similarity {similarity:.4f} is below threshold 0.95"

def test_best_d_file_exists():
    d_path = '/home/user/best_D.txt'
    assert os.path.exists(d_path), f"Output file missing: {d_path}"
    assert os.path.isfile(d_path), f"Path {d_path} is not a file."

    with open(d_path, 'r') as f:
        content = f.read().strip()
    assert len(content) > 0, f"File {d_path} is empty."

    try:
        float(content)
    except ValueError:
        assert False, f"File {d_path} does not contain a valid float."

def test_cpp_mesh_size_updated():
    cpp_path = "/home/user/sim_src/heat_solver.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "#define N 64" in content, "The mesh size was not updated to '#define N 64' in heat_solver.cpp."