# test_final_state.py

import os
import subprocess
import pytest

def test_jaccard_similarity():
    agent_file = "/home/user/top_100_anomalies.csv"
    assert os.path.exists(agent_file), f"Agent output file missing at {agent_file}"

    # Generate truth dynamically using the specified procedure
    bash_script = """
    grep -v "|DEBUG_" /home/user/raw_logs.txt | \\
    sort -t'|' -k2,2 -k1,1 | \\
    awk -F'|' '
      BEGIN { OFS="\\t" }
      {
        if ($2 != last_user) {
          if (last_user != "") {
            print last_user, acts
          }
          last_user = $2
          last_act = $3
          acts = $3
        } else {
          if ($3 != last_act) {
            acts = acts "," $3
            last_act = $3
          }
        }
      }
      END {
        if (last_user != "") print last_user, acts
      }
    ' | /app/anomaly_scorer | sort -k2,2nr -k1,1 | head -n 100 | tr '\\t' ','
    """

    result = subprocess.run(bash_script, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compute truth: {result.stderr}"

    truth_lines = result.stdout.strip().split('\n')
    truth_users = set()
    for line in truth_lines:
        if line:
            truth_users.add(line.split(',')[0])

    agent_users = set()
    with open(agent_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if parts:
                agent_users.add(parts[0])

    intersection = len(truth_users.intersection(agent_users))
    union = len(truth_users.union(agent_users))
    jaccard = intersection / union if union > 0 else 0

    assert jaccard >= 0.99, f"Jaccard similarity {jaccard:.4f} is less than threshold 0.99. Intersection: {intersection}, Union: {union}."