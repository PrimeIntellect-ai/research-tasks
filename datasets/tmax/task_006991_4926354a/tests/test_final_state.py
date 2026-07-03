# test_final_state.py

import os
import subprocess

def get_expected_metric():
    script = """
    join -t, -1 1 -2 1 <(sort -t, -k1,1 /home/user/features.csv) <(sort -t, -k1,1 /home/user/targets.csv) > /tmp/joined_truth.csv
    total=$(wc -l < /tmp/joined_truth.csv)
    train_n=$((total * 80 / 100))
    shuf --random-source=/home/user/seed.dat /tmp/joined_truth.csv > /tmp/shuffled_truth.csv
    head -n "$train_n" /tmp/shuffled_truth.csv > /tmp/train_truth.csv
    tail -n +$((train_n + 1)) /tmp/shuffled_truth.csv > /tmp/test_truth.csv

    mean_truth=$(awk -F, '$2 != "" {sum+=$2; count++} END {print sum/count}' /tmp/train_truth.csv)

    awk -F, -v m="$mean_truth" 'BEGIN{OFS=","} {if($2=="") $2=m; print $0}' /tmp/test_truth.csv > /tmp/test_imputed_truth.csv
    awk -F, '$2 > 50 {sum+=$3; count++} END {if(count>0) print sum/count; else print 0}' /tmp/test_imputed_truth.csv
    """
    result = subprocess.run(["bash", "-c", script], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def test_metric_is_correct():
    metric_path = "/home/user/metric.txt"
    assert os.path.isfile(metric_path), f"Missing file: {metric_path}. Did you run the modified pipeline.sh script?"

    with open(metric_path, "r") as f:
        actual_metric = f.read().strip()

    expected_metric = get_expected_metric()

    assert actual_metric == expected_metric, (
        f"Metric mismatch. Expected '{expected_metric}', but got '{actual_metric}'. "
        "Ensure that the mean is calculated ONLY from the training set, and used to impute missing values in both sets."
    )