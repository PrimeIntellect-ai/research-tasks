# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/simulate_mc.sh"
RESULTS_PATH = "/home/user/results.txt"
TEST_PDB_PATH = "/tmp/test.pdb"

def setup_module(module):
    # Generate the test PDB file
    pdb_content = """ATOM      1  N   MET A   1      27.340  24.430   2.952  1.00 50.00           N  
ATOM      2  CA  MET A   1      26.266  25.413   2.842  1.00 50.00           C  
ATOM      3  C   MET A   1      26.913  26.639   2.231  1.00 50.00           C  
ATOM      4  O   MET A   1      27.886  26.463   1.498  1.00 50.00           O  
ATOM      5  CB  MET A   1      25.112  24.880   2.039  1.00 50.00           C  
"""
    with open(TEST_PDB_PATH, "w") as f:
        f.write(pdb_content)

def get_expected_results():
    # We use an embedded awk script that strictly follows the task requirements
    # to derive the expected output.
    awk_script = r"""
    BEGIN {
        minX = 1e9; maxX = -1e9;
        minY = 1e9; maxY = -1e9;
        minZ = 1e9; maxZ = -1e9;
    }
    /^ATOM  / {
        x = substr($0, 31, 8) + 0;
        y = substr($0, 39, 8) + 0;
        z = substr($0, 47, 8) + 0;

        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
        if (z < minZ) minZ = z;
        if (z > maxZ) maxZ = z;

        xs[NR] = x; ys[NR] = y; zs[NR] = z;
    }
    END {
        if (maxX == minX) { minX -= 0.1; maxX += 0.1; }
        if (maxY == minY) { minY -= 0.1; maxY += 0.1; }
        if (maxZ == minZ) { minZ -= 0.1; maxZ += 0.1; }

        for (i in xs) {
            x = xs[i]; y = ys[i]; z = zs[i];

            ix = int(5 * (x - minX) / (maxX - minX));
            if (ix == 5) ix = 4;

            iy = int(5 * (y - minY) / (maxY - minY));
            if (iy == 5) iy = 4;

            iz = int(5 * (z - minZ) / (maxZ - minZ));
            if (iz == 5) iz = 4;

            occupied[ix "," iy "," iz] = 1;
        }

        occ_count = 0;
        for (k in occupied) occ_count++;

        srand(42);
        hits = 0;
        for (n=0; n<1000; n++) {
            rx = minX + rand() * (maxX - minX);
            ry = minY + rand() * (maxY - minY);
            rz = minZ + rand() * (maxZ - minZ);

            ix = int(5 * (rx - minX) / (maxX - minX));
            if (ix == 5) ix = 4;
            iy = int(5 * (ry - minY) / (maxY - minY));
            if (iy == 5) iy = 4;
            iz = int(5 * (rz - minZ) / (maxZ - minZ));
            if (iz == 5) iz = 4;

            if ((ix "," iy "," iz) in occupied) {
                hits++;
            }
        }

        printf "Occupied Cells: %d\n", occ_count;
        printf "MC Hit Ratio: %.3f\n", hits / 1000;
    }
    """
    cmd = ["awk", awk_script, TEST_PDB_PATH]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # Remove results file if it exists to ensure a fresh run
    if os.path.exists(RESULTS_PATH):
        os.remove(RESULTS_PATH)

    # Run the user's script
    result = subprocess.run([SCRIPT_PATH, TEST_PDB_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.exists(RESULTS_PATH), f"Results file {RESULTS_PATH} was not created."

    with open(RESULTS_PATH, "r") as f:
        actual_content = f.read().strip()

    expected_content = get_expected_results()

    # We allow slight formatting differences in the float output, so we parse it
    actual_lines = actual_content.splitlines()
    expected_lines = expected_content.splitlines()

    assert len(actual_lines) == 2, f"Expected exactly 2 lines in {RESULTS_PATH}, got {len(actual_lines)}."

    actual_occ = actual_lines[0].split(":")[-1].strip()
    expected_occ = expected_lines[0].split(":")[-1].strip()
    assert actual_occ == expected_occ, f"Occupied Cells count mismatch. Expected {expected_occ}, got {actual_occ}."

    actual_ratio = float(actual_lines[1].split(":")[-1].strip())
    expected_ratio = float(expected_lines[1].split(":")[-1].strip())

    assert abs(actual_ratio - expected_ratio) < 1e-4, f"MC Hit Ratio mismatch. Expected {expected_ratio}, got {actual_ratio}."