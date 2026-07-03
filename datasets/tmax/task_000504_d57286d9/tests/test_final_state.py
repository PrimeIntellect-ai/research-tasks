# test_final_state.py
import os
import math
import subprocess
import stat

def get_expected_results():
    results = []
    plot_lines = []

    for N in range(10000, 100001, 10000):
        seed = 42
        inside = 0
        for i in range(N):
            coords = []
            for j in range(3):
                seed = (1103515245 * seed + 12345) % 2147483648
                val = (seed / 2147483648.0) * 2.0 - 1.0
                coords.append(val)
            if coords[0]**2 + coords[1]**2 + coords[2]**2 < 1.0:
                inside += 1

        vol = 8.0 * inside / N
        error = abs(vol - 4.188790204786)
        results.append(f"{N} {error:.6f}")

        stars = int(math.floor(error * 500))
        plot_lines.append(f"{N:>6} | " + "*" * stars)

    return "\n".join(results) + "\n", "\n".join(plot_lines) + "\n"

def test_files_exist():
    assert os.path.isfile("/home/user/mc_sphere.c"), "/home/user/mc_sphere.c does not exist."
    assert os.path.isfile("/home/user/run_experiment.sh"), "/home/user/run_experiment.sh does not exist."

def test_script_executable():
    st = os.stat("/home/user/run_experiment.sh")
    assert bool(st.st_mode & stat.S_IXUSR), "/home/user/run_experiment.sh is not executable."

def test_experiment_results():
    # Remove previous outputs to ensure we are testing the script's actual execution
    if os.path.exists("/home/user/mc_errors.txt"):
        os.remove("/home/user/mc_errors.txt")
    if os.path.exists("/home/user/error_plot.txt"):
        os.remove("/home/user/error_plot.txt")

    # Run the script
    result = subprocess.run(["/home/user/run_experiment.sh"], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"run_experiment.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

    # Check output files exist
    assert os.path.isfile("/home/user/mc_errors.txt"), "/home/user/mc_errors.txt was not created."
    assert os.path.isfile("/home/user/error_plot.txt"), "/home/user/error_plot.txt was not created."

    # Read output files
    with open("/home/user/mc_errors.txt", "r") as f:
        mc_errors = f.read()

    with open("/home/user/error_plot.txt", "r") as f:
        error_plot = f.read()

    expected_errors, expected_plot = get_expected_results()

    assert mc_errors.strip() == expected_errors.strip(), f"Contents of mc_errors.txt do not match expected results.\nExpected:\n{expected_errors}\nGot:\n{mc_errors}"
    assert error_plot.rstrip() == expected_plot.rstrip(), f"Contents of error_plot.txt do not match expected results.\nExpected:\n{expected_plot}\nGot:\n{error_plot}"