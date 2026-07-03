# test_final_state.py
import math
import os
import pytest

def simulate_trajectory(Cd, vx0, vy0, frames=300, dt=1.0/60.0):
    x, y = 0.0, 0.0
    vx, vy = vx0, vy0
    trajectory = []
    for _ in range(frames):
        trajectory.append((x, y))
        v_mag = math.sqrt(vx**2 + vy**2)
        ax = -Cd * v_mag * vx
        ay = 9.81 - Cd * v_mag * vy
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
    return trajectory

def test_optimized_params_mse():
    params_file = "/home/user/optimized_params.txt"
    assert os.path.exists(params_file), f"File {params_file} does not exist."

    with open(params_file, 'r') as f:
        content = f.read().strip()

    try:
        params = content.split(',')
        Cd_pred, vx0_pred, vy0_pred = map(float, params)
    except Exception as e:
        pytest.fail(f"Could not parse {params_file}. Expected 3 comma-separated floats. Error: {e}")

    gt_traj = simulate_trajectory(0.05, 15.0, -20.0)
    pred_traj = simulate_trajectory(Cd_pred, vx0_pred, vy0_pred)

    mse = 0.0
    for (gt_x, gt_y), (p_x, p_y) in zip(gt_traj, pred_traj):
        px_gt_x, px_gt_y = gt_x * 100, gt_y * 100
        px_p_x, px_p_y = p_x * 100, p_y * 100
        mse += (px_gt_x - px_p_x)**2 + (px_gt_y - px_p_y)**2
    mse /= len(gt_traj)

    assert mse <= 10.0, f"MSE is {mse:.2f}, which is greater than the threshold of 10.0"