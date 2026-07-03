# test_final_state.py
import os
import json
import math

def test_experiment_results_artifact():
    artifact_path = "/home/user/artifacts/experiment_results.json"
    assert os.path.isfile(artifact_path), f"Artifact file {artifact_path} does not exist."

    with open(artifact_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {artifact_path} is not valid JSON."

    # Validate schema presence
    expected_keys = {
        "variant_A_successes",
        "variant_A_failures",
        "variant_B_successes",
        "variant_B_failures",
        "prob_B_better_than_A",
        "benchmark_time_seconds",
        "omp_threads"
    }
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Missing keys in JSON: {missing_keys}"

    # Validate computed conversions
    assert results["variant_A_successes"] == 1, f"Expected 1 success for A, got {results['variant_A_successes']}"
    assert results["variant_A_failures"] == 3, f"Expected 3 failures for A, got {results['variant_A_failures']}"
    assert results["variant_B_successes"] == 2, f"Expected 2 successes for B, got {results['variant_B_successes']}"
    assert results["variant_B_failures"] == 2, f"Expected 2 failures for B, got {results['variant_B_failures']}"

    # Validate probability (with seed 42, 1M samples, expected is ~0.6865)
    prob = results["prob_B_better_than_A"]
    assert isinstance(prob, (int, float)), "prob_B_better_than_A must be a float"
    assert math.isclose(prob, 0.6865, abs_tol=0.001), f"Expected prob_B_better_than_A to be ~0.6865, got {prob}"

    # Validate benchmark time
    bench_time = results["benchmark_time_seconds"]
    assert isinstance(bench_time, (int, float)) and bench_time > 0, "benchmark_time_seconds must be a positive float"

    # Validate OMP_NUM_THREADS
    assert results["omp_threads"] == "4", f"Expected omp_threads to be '4', got {results['omp_threads']}"