# test_final_state.py
import os
import subprocess
import math

def test_script_exists_and_executable():
    script_path = "/home/user/jsd_matrix.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def calc_jsd(p_counts, q_counts):
    p = [x + 0.01 for x in p_counts]
    q = [x + 0.01 for x in q_counts]
    sum_p = sum(p)
    sum_q = sum(q)
    p = [x / sum_p for x in p]
    q = [x / sum_q for x in q]
    m = [0.5 * (x + y) for x, y in zip(p, q)]

    kl_p = sum(x * math.log(x / y) for x, y in zip(p, m))
    kl_q = sum(x * math.log(x / y) for x, y in zip(q, m))

    return 0.5 * kl_p + 0.5 * kl_q

def test_script_logic():
    script_path = "/home/user/jsd_matrix.sh"
    test_csv_path = "/home/user/test_grading_data.csv"
    output_path = "/home/user/jsd_output.txt"

    # Create a test CSV with various edge cases
    csv_content = (
        "10,20,30,40\n"
        "10,20,30,40\n"
        "0,0,0,100\n"
        "5,25,30,40\n"
        "100,0,0,0\n"
        "0,0,0,0\n"
    )

    with open(test_csv_path, "w") as f:
        f.write(csv_content)

    # Remove output file if it exists to ensure we are checking fresh output
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the student's script
    result = subprocess.run([script_path, test_csv_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode} and error: {result.stderr}"

    assert os.path.isfile(output_path), f"Output file {output_path} was not created by the script."

    with open(output_path, "r") as f:
        output_lines = [line.strip() for line in f.readlines() if line.strip()]

    lines = csv_content.strip().split('\n')
    data = [[float(x) for x in line.split(',')] for line in lines]
    p_counts = data[0]

    expected_lines = []
    for i in range(1, len(data)):
        q_counts = data[i]
        jsd = calc_jsd(p_counts, q_counts)
        status = "VALID" if jsd <= 0.1 else "INVALID"
        expected_lines.append(f"Row_{i+1}: {jsd:.6f} {status}")

    assert len(output_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines of output, but got {len(output_lines)}."

    for i, (out_line, exp_line) in enumerate(zip(output_lines, expected_lines)):
        assert out_line == exp_line, f"Output mismatch at Row_{i+2}. Expected: '{exp_line}', Got: '{out_line}'"