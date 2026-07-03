# test_final_state.py
import os
import json
import pstats

def test_mc_laplace_script():
    script_path = '/home/user/mc_laplace.py'
    assert os.path.exists(script_path), f"{script_path} does not exist."

    with open(script_path, 'r') as f:
        code = f.read()

    assert 'multiprocessing' in code or 'ProcessPoolExecutor' in code, "Script must use multiprocessing."
    assert 'cProfile' in code or 'profile' in code.lower(), "Script must use cProfile."

def test_profile_output():
    prof_path = '/home/user/profile.prof'
    assert os.path.exists(prof_path), f"{prof_path} does not exist."

    try:
        stats = pstats.Stats(prof_path)
        assert stats.total_calls > 0, "Profile stats indicate no calls were recorded."
    except Exception as e:
        assert False, f"Failed to read {prof_path} as a valid cProfile dump: {e}"

def test_results_json():
    json_path = '/home/user/results.json'
    assert os.path.exists(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not valid JSON."

    assert 'max_abs_error' in results, "Missing 'max_abs_error' in results.json"
    assert 'mse_reference' in results, "Missing 'mse_reference' in results.json"
    assert 'execution_time' in results, "Missing 'execution_time' in results.json"

    assert isinstance(results['max_abs_error'], (int, float)), "'max_abs_error' must be a number."
    assert isinstance(results['mse_reference'], (int, float)), "'mse_reference' must be a number."
    assert isinstance(results['execution_time'], (int, float)), "'execution_time' must be a number."

    assert results['max_abs_error'] < 0.08, f"max_abs_error is too high: {results['max_abs_error']} >= 0.08"
    assert results['mse_reference'] < 0.05, f"mse_reference is too high: {results['mse_reference']} >= 0.05"