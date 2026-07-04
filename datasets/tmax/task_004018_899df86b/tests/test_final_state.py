# test_final_state.py

import os
import re
import math
import pstats
import pytest

def compute_expected_energy():
    """Recomputes the expected Lennard-Jones potential energy using the standard library."""
    atoms = []
    with open('/home/user/protein_frame.pdb', 'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                name = line[12:16].strip()
                if name == "CA":
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    atoms.append((x, y, z))

    # We use a list to collect energies to sum them up similarly to numpy (though float addition order may slightly affect the last decimal)
    # The tolerance will account for minor floating point differences.
    energies = []
    n = len(atoms)
    for i in range(n):
        xi, yi, zi = atoms[i]
        for j in range(i + 1, n):
            xj, yj, zj = atoms[j]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            r2 = dx*dx + dy*dy + dz*dz
            r6 = r2 * r2 * r2
            if r6 > 0:
                e = (1.0 / (r6 * r6)) - (1.0 / r6)
                energies.append(e)

    # Summing up
    return math.fsum(energies)

def test_energy_result_file():
    """Check that energy_result.txt exists and is formatted to 8 decimal places."""
    result_path = "/home/user/energy_result.txt"
    assert os.path.isfile(result_path), f"Missing file: {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert re.match(r'^-?\d+\.\d{8}$', content), f"Energy result '{content}' is not formatted to exactly 8 decimal places."

def test_energy_value():
    """Check that the calculated energy is correct."""
    result_path = "/home/user/energy_result.txt"
    assert os.path.isfile(result_path), f"Missing file: {result_path}"

    with open(result_path, 'r') as f:
        student_val = float(f.read().strip())

    expected_val = compute_expected_energy()

    # Allow a small tolerance for floating point accumulation differences
    assert math.isclose(student_val, expected_val, rel_tol=1e-5, abs_tol=1e-5), \
        f"Calculated energy {student_val} does not match expected energy {expected_val}."

def test_profile_exists():
    """Check that profile.prof exists and is a valid pstats file."""
    profile_path = "/home/user/profile.prof"
    assert os.path.isfile(profile_path), f"Missing profiling output: {profile_path}"

    try:
        stats = pstats.Stats(profile_path)
        assert stats.total_calls > 0 or len(stats.stats) > 0, "Profile file is empty or invalid."
    except Exception as e:
        pytest.fail(f"Failed to parse {profile_path} as a pstats file: {e}")

def test_script_updated():
    """Check that md_analysis.py has been updated to remove threading and use numpy."""
    script_path = "/home/user/md_analysis.py"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    assert "concurrent.futures" not in content, "Script still contains concurrent.futures."
    assert "ThreadPoolExecutor" not in content, "Script still contains ThreadPoolExecutor."
    assert "import numpy" in content or "from numpy" in content, "Script does not appear to import numpy."