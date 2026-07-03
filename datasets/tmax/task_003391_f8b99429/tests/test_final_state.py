# test_final_state.py

import os
import subprocess
import json
import shutil

def test_manage_storage_accuracy():
    """
    Generate mock QCOW2 files, run the agent's script, and verify the generated fstab.
    """
    script_path = "/home/user/manage_storage.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    test_dir = "/tmp/test_vms"
    os.makedirs(test_dir, exist_ok=True)

    threshold = 81.4

    # Generate 20 mock QCOW2 files to test the logic efficiently
    # (100 would take longer, 20 is sufficient to test the threshold and sorting)
    for i in range(20):
        filename = f"vm_{i:03d}.qcow2"
        filepath = os.path.join(test_dir, filename)
        if not os.path.exists(filepath):
            subprocess.run(["qemu-img", "create", "-f", "qcow2", filepath, "1M"], check=True, capture_output=True)
            # Write varying amounts of data to simulate different utilizations
            if i % 3 == 0:
                subprocess.run(["qemu-io", "-c", "write 0 900k", filepath], check=True, capture_output=True)
            elif i % 3 == 1:
                subprocess.run(["qemu-io", "-c", "write 0 800k", filepath], check=True, capture_output=True)
            else:
                subprocess.run(["qemu-io", "-c", "write 0 100k", filepath], check=True, capture_output=True)

    expected_valid = []
    files = sorted([f for f in os.listdir(test_dir) if f.endswith('.qcow2')])

    for filename in files:
        filepath = os.path.join(test_dir, filename)
        res = subprocess.run(["qemu-img", "info", "--output=json", filepath], capture_output=True, text=True, check=True)
        info = json.loads(res.stdout)
        utilization = (info["actual-size"] / info["virtual-size"]) * 100

        if utilization < threshold:
            expected_valid.append(filename)

    # Run agent script
    fstab_path = "/home/user/fstab_generated"
    if os.path.exists(fstab_path):
        os.remove(fstab_path)

    res = subprocess.run(["python3", script_path, test_dir], capture_output=True, text=True)
    assert res.returncode == 0, f"Script failed with error:\n{res.stderr}\nOutput:\n{res.stdout}"

    assert os.path.exists(fstab_path), f"{fstab_path} was not generated."

    with open(fstab_path, "r") as f:
        generated_lines = [line.strip() for line in f if line.strip()]

    expected_lines = []
    for idx, filename in enumerate(expected_valid):
        name_no_ext = os.path.splitext(filename)[0]
        expected_lines.append(f"/dev/nbd{idx} /mnt/services/{name_no_ext} ext4 defaults,usrquota 0 2")

    # Calculate accuracy
    correct_lines = 0
    for exp, gen in zip(expected_lines, generated_lines):
        if exp == gen:
            correct_lines += 1

    accuracy = 1.0 if expected_lines == generated_lines else 0.0

    assert expected_lines == generated_lines, (
        f"Generated fstab does not match expected.\n"
        f"Accuracy: {accuracy} (Threshold: 1.0)\n"
        f"Expected {len(expected_lines)} lines, got {len(generated_lines)} lines.\n"
        f"Expected first line: {expected_lines[0] if expected_lines else 'None'}\n"
        f"Generated first line: {generated_lines[0] if generated_lines else 'None'}"
    )