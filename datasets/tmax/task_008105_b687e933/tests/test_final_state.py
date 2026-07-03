# test_final_state.py

import os
import subprocess

def test_run_mc_sh_exists():
    """Verify that the bash script run_mc.sh was created."""
    assert os.path.isfile("/home/user/run_mc.sh"), "/home/user/run_mc.sh does not exist."

def test_histogram_txt_exists():
    """Verify that the histogram.txt file was generated."""
    assert os.path.isfile("/home/user/histogram.txt"), "/home/user/histogram.txt does not exist."

def test_histogram_content():
    """Verify that the histogram.txt contains the correct output based on bash's RANDOM."""
    # Recompute the expected output using bash to ensure exact match with bash's LCG
    bash_script = """
    RANDOM=12345
    declare -A counts
    for i in {1..10000}; do
      val=$(( 12 + (RANDOM % 7) ))
      ((counts[$val]++))
    done

    for val in {12..18}; do
      c=${counts[$val]:-0}
      stars=$(( c / 50 ))
      # Generate a string of stars
      star_str=""
      for ((j=0; j<stars; j++)); do
          star_str="${star_str}*"
      done
      printf "%d: %s\\n" "$val" "$star_str"
    done
    """

    result = subprocess.run(["bash", "-c", bash_script], capture_output=True, text=True)
    expected_output = result.stdout.strip()

    with open("/home/user/histogram.txt", "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Contents of /home/user/histogram.txt do not match the expected output.\n"
        f"Expected:\n{expected_output}\n\nGot:\n{actual_output}"
    )