# test_final_state.py

import os
import subprocess

SCRIPT_PATH = "/home/user/fast_bootstrap.sh"
FASTA_PATH = "/home/user/input.fasta"

def test_script_exists_and_executable():
    """Verify the script exists and has executable permissions."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def get_expected_output(fasta_path, seed):
    """Compute the expected output using the golden logic."""
    lengths_cmd = f"gawk '/^>/ {{if (seqlen>0) print seqlen; seqlen=0; next}} {{seqlen+=length($0)}} END {{if(seqlen>0) print seqlen}}' {fasta_path}"
    lengths_out = subprocess.check_output(lengths_cmd, shell=True, text=True)

    with open("/tmp/test_lengths.txt", "w") as f:
        f.write(lengths_out)

    gawk_script = f"""
    BEGIN {{
        srand({seed})
    }}
    {{
        len[NR]=$1
    }}
    END {{
        n = NR
        sum_orig = 0
        for(i=1; i<=n; i++) sum_orig += len[i]
        orig_mean = sum_orig / n
        printf "Original Mean: %.2f\\n", orig_mean

        for(b=1; b<=1000; b++) {{
            sum = 0
            for(i=1; i<=n; i++) {{
                idx = int(rand() * n) + 1
                sum += len[idx]
            }}
            print (sum / n) > "/tmp/test_boot_means_{seed}.txt"
        }}
    }}
    """

    with open(f"/tmp/test_gawk_{seed}.awk", "w") as f:
        f.write(gawk_script)

    cmd1 = f"gawk -f /tmp/test_gawk_{seed}.awk /tmp/test_lengths.txt"
    out1 = subprocess.check_output(cmd1, shell=True, text=True)

    cmd2 = f"sort -n /tmp/test_boot_means_{seed}.txt | awk 'NR==25 {{lower=$1}} NR==975 {{upper=$1}} END {{printf \"95%% CI: %.2f to %.2f\\n\", lower, upper}}'"
    out2 = subprocess.check_output(cmd2, shell=True, text=True)

    return out1.strip() + "\n" + out2.strip()

def test_script_output_seed_123():
    """Test the script output with seed 123."""
    expected = get_expected_output(FASTA_PATH, 123)

    result = subprocess.run([SCRIPT_PATH, FASTA_PATH, "123"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    actual = result.stdout.strip()
    assert actual == expected, f"Output mismatch for seed 123.\nExpected:\n{expected}\nActual:\n{actual}"

def test_script_output_seed_42():
    """Test the script output with seed 42 to ensure reproducibility and no hardcoded values."""
    expected = get_expected_output(FASTA_PATH, 42)

    result = subprocess.run([SCRIPT_PATH, FASTA_PATH, "42"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    actual = result.stdout.strip()
    assert actual == expected, f"Output mismatch for seed 42.\nExpected:\n{expected}\nActual:\n{actual}"