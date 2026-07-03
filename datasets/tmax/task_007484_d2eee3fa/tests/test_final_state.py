# test_final_state.py
import os
import re

def test_diffusion_directory_exists():
    """Check that the diffusion directory was created."""
    assert os.path.isdir("/home/user/diffusion"), "/home/user/diffusion directory is missing."

def test_source_files_exist():
    """Check that the C++ source and bash script exist."""
    assert os.path.isfile("/home/user/diffusion/mc_diffusion.cpp"), "mc_diffusion.cpp is missing."
    assert os.path.isfile("/home/user/diffusion/test_convergence.sh"), "test_convergence.sh is missing."

def test_executable_exists():
    """Check that the C++ program was compiled into an executable."""
    exe_path = "/home/user/diffusion/mc_diffusion"
    assert os.path.isfile(exe_path), "Compiled executable mc_diffusion is missing."
    assert os.access(exe_path, os.X_OK), "mc_diffusion is not executable."

def test_convergence_log():
    """Check the contents of convergence.log for correctness and convergence."""
    log_path = "/home/user/diffusion/convergence.log"
    assert os.path.isfile(log_path), "convergence.log is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in convergence.log, found {len(lines)}."

    pattern = re.compile(r"^MSD:\s*([0-9.]+),\s*CI:\s*\[([0-9.]+),\s*([0-9.]+)\]$")

    widths = []
    for i, line in enumerate(lines):
        match = pattern.match(line)
        assert match, f"Line {i+1} does not match expected format: {line}"

        msd = float(match.group(1))
        lower = float(match.group(2))
        upper = float(match.group(3))

        assert 200 <= msd <= 400, f"Line {i+1} MSD ({msd}) is not near the expected value of 300."
        assert lower <= msd <= upper, f"Line {i+1} MSD ({msd}) is not within CI [{lower}, {upper}]."

        widths.append(upper - lower)

    # Check that CI width strictly decreases as N increases (100 -> 1000 -> 10000)
    assert widths[0] > widths[1], f"CI width did not decrease from N=100 ({widths[0]}) to N=1000 ({widths[1]})."
    assert widths[1] > widths[2], f"CI width did not decrease from N=1000 ({widths[1]}) to N=10000 ({widths[2]})."