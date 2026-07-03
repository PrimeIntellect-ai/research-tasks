# test_final_state.py
import os
import subprocess
import time
import pytest

def test_fixed_analyzer_performance_and_accuracy():
    script_path = "/home/user/fixed_analyzer.sh"
    audio_path = "/app/test_audio.wav"
    output_path = "/home/user/anomalies.txt"

    assert os.path.isfile(script_path), f"Missing fixed script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"
    assert os.path.isfile(audio_path), f"Missing audio file: {audio_path}"

    # Remove output file if it exists to ensure we are testing the new run
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the agent's script and measure time
    start_time = time.time()
    try:
        result = subprocess.run(
            [script_path, audio_path, output_path], 
            capture_output=True, 
            text=True, 
            timeout=10.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Execution time exceeded 10.0s (Timeout). Script is still too slow or looping.")
    end_time = time.time()

    execution_time = end_time - start_time

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"
    assert os.path.isfile(output_path), f"Script did not create output file: {output_path}"

    assert execution_time <= 2.0, f"Execution time {execution_time:.2f}s exceeded threshold of 2.0s"

    # Compute ground truth using the exact mathematical specification
    golden_script = """
sox /app/test_audio.wav -t dat - resample 100 | tail -n +3 | awk '
{
    time[NR] = $1;
    val[NR] = $2 < 0 ? -$2 : $2; # absolute amplitude
    sum = 0;
    count = 0;
    for (i = 0; i < 10; i++) {
        if (NR - i > 0) {
            sum += val[NR - i];
            count++;
        }
    }
    smooth[NR] = sum / count;
    global_sum += smooth[NR];
}
END {
    mean = global_sum / NR;
    sq_diff_sum = 0;
    for (i = 1; i <= NR; i++) {
        sq_diff_sum += (smooth[i] - mean)^2;
    }
    stddev = sqrt(sq_diff_sum / NR);
    threshold = mean + 3 * stddev;

    for (i = 1; i <= NR; i++) {
        if (smooth[i] > threshold) {
            printf "%.2f\\n", time[i];
        }
    }
}'
"""
    golden_result = subprocess.run(golden_script, shell=True, capture_output=True, text=True)
    assert golden_result.returncode == 0, "Failed to compute ground truth anomalies."

    golden_anomalies = set(golden_result.stdout.strip().split('\n'))
    golden_anomalies.discard('')

    with open(output_path, 'r') as f:
        agent_anomalies = set(f.read().strip().split('\n'))
    agent_anomalies.discard('')

    # Compute F1 Score
    true_positives = len(golden_anomalies.intersection(agent_anomalies))
    false_positives = len(agent_anomalies - golden_anomalies)
    false_negatives = len(golden_anomalies - agent_anomalies)

    if true_positives == 0:
        f1_score = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1_score = 2 * (precision * recall) / (precision + recall)

    assert f1_score >= 0.99, f"F1-score {f1_score:.4f} is below threshold of 0.99. Agent detected {len(agent_anomalies)} anomalies, Expected {len(golden_anomalies)}."