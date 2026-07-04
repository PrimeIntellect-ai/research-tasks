# test_final_state.py
import os
import subprocess
import random
import csv

def test_directories_exist():
    assert os.path.isdir("/home/user/experiment_artifacts/frames"), "Frames directory missing"
    assert os.path.isdir("/home/user/scripts"), "Scripts directory missing"

def test_frames_extracted():
    for i in range(1, 21):
        frame_path = f"/home/user/experiment_artifacts/frames/frame_{i:02d}.pgm"
        assert os.path.isfile(frame_path), f"Missing frame {frame_path}"

def read_pgm_block_avg(filepath, x, y, w, h):
    with open(filepath, 'rb') as f:
        header = f.readline().decode('ascii').strip()
        assert header == 'P5', f"Expected P5 PGM, got {header}"

        # skip comments
        while True:
            pos = f.tell()
            line = f.readline()
            if not line.startswith(b'#'):
                f.seek(pos)
                break

        dims = f.readline().decode('ascii').split()
        width, height = int(dims[0]), int(dims[1])
        maxval = int(f.readline().decode('ascii').strip())

        data = f.read()

    sum_val = 0
    for row in range(y, y+h):
        for col in range(x, x+w):
            sum_val += data[row * width + col]

    return sum_val / (w * h)

def test_sensor_data_csv():
    csv_path = "/home/user/experiment_artifacts/sensor_data.csv"
    assert os.path.isfile(csv_path), "sensor_data.csv missing"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 21, f"Expected 21 rows in CSV, got {len(rows)}"
    assert rows[0] == ['frame', 'sensor_x', 'sensor_y'], "Incorrect CSV header"

    for i in range(1, 21):
        frame_id = rows[i][0]
        assert f"frame_{i:02d}" in frame_id, f"Unexpected frame ID {frame_id} in row {i}"

        frame_path = f"/home/user/experiment_artifacts/frames/frame_{i:02d}.pgm"

        # Read PGM to find dimensions
        with open(frame_path, 'rb') as f:
            f.readline()
            while True:
                pos = f.tell()
                line = f.readline()
                if not line.startswith(b'#'):
                    f.seek(pos)
                    break
            dims = f.readline().decode('ascii').split()
            width, height = int(dims[0]), int(dims[1])

        expected_x = read_pgm_block_avg(frame_path, 0, 0, 50, 50)
        expected_y = read_pgm_block_avg(frame_path, width - 50, height - 50, 50, 50)

        val_x = float(rows[i][1])
        val_y = float(rows[i][2])

        assert abs(val_x - expected_x) < 1.0, f"Row {i} sensor_x mismatch: expected {expected_x}, got {val_x}"
        assert abs(val_y - expected_y) < 1.0, f"Row {i} sensor_y mismatch: expected {expected_y}, got {val_y}"

def test_calc_cov_fuzz_equivalence():
    agent_script = "/home/user/scripts/calc_cov.sh"
    oracle_script = "/app/oracle_calc_cov.sh"

    assert os.path.isfile(agent_script), f"Missing {agent_script}"
    assert os.access(agent_script, os.X_OK), f"{agent_script} is not executable"

    random.seed(42)

    for _ in range(200):
        k = random.randint(5, 50)
        args = [str(random.randint(0, 255)) for _ in range(2 * k)]

        oracle_cmd = ["bash", oracle_script] + args
        agent_cmd = ["bash", agent_script] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on args: {' '.join(args)}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, f"Mismatch on args: {' '.join(args)}\nExpected: {oracle_out}\nGot: {agent_out}"