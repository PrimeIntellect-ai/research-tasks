# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/simulate_walk.sh"
NETWORK_PATH = "/home/user/ppi_network.tsv"

AWK_REF = r"""BEGIN {
    FS="\t"
    if (seed != "") srand(seed)
}
{
    src = $1; dst = $2; weight = $3
    edges[src][dst] = weight
    nodes[src] = 1
    nodes[dst] = 1
}
END {
    curr = start
    for (step=1; step<=1000; step++) {
        has_out = 0
        max_score = -1
        best_dst = ""

        # Sort destination nodes to guarantee identical rand() sequence matching
        n_dst = asorti(edges[curr], sorted_dsts)
        if (n_dst > 0) {
            has_out = 1
            for (i=1; i<=n_dst; i++) {
                v = sorted_dsts[i]
                r = rand()
                score = edges[curr][v] * r

                if (score > max_score) {
                    max_score = score
                    best_dst = v
                } else if (score == max_score) {
                    if (best_dst == "" || v < best_dst) {
                        best_dst = v
                    }
                }
            }
            curr = best_dst
        }
        visits[curr]++
    }

    n_vis = asorti(visits, sorted_visits)
    for (i=1; i<=n_vis; i++) {
        p = sorted_visits[i]
        count = visits[p]
        bars = ""
        num_bars = int(count / 10)
        for (b=0; b<num_bars; b++) bars = bars "="
        printf "%s [%d] : %s\n", p, count, bars
    }
}
"""

def get_expected_output(start: str, seed: str) -> str:
    """Run the canonical awk reference script to get the exact expected output."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(AWK_REF)
        ref_path = f.name

    try:
        cmd = ["awk", "-v", f"start={start}", "-v", f"seed={seed}", "-f", ref_path, NETWORK_PATH]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    finally:
        os.remove(ref_path)

def test_script_exists_and_executable():
    """Check that the student's script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Missing required script: {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable (chmod +x)."

@pytest.mark.parametrize("start, seed", [
    ("A", "42"),
    ("E", "100"),
    ("C", "999")
])
def test_simulation_output(start, seed):
    """Test that the student's script produces the exact expected output for given inputs."""
    expected = get_expected_output(start, seed)

    cmd = [SCRIPT_PATH, start, seed]
    res = subprocess.run(cmd, capture_output=True, text=True)

    assert res.returncode == 0, f"Script failed (return code {res.returncode}) for start={start}, seed={seed}.\nStderr: {res.stderr}"

    actual = res.stdout.strip()
    assert actual == expected, (
        f"Output mismatch for start={start}, seed={seed}.\n"
        f"Expected:\n{expected}\n\n"
        f"Actual:\n{actual}"
    )