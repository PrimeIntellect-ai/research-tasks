# test_final_state.py
import os
import json
import stat

def test_scripts_exist_and_executable():
    """Check if the required scripts exist and have correct permissions."""
    prep_path = '/home/user/prep.sh'
    train_path = '/home/user/train.py'
    track_path = '/home/user/track.sh'

    assert os.path.exists(prep_path), f"Missing {prep_path}"
    assert os.path.exists(train_path), f"Missing {train_path}"
    assert os.path.exists(track_path), f"Missing {track_path}"

    # prep.sh and track.sh must be executable
    assert os.stat(prep_path).st_mode & stat.S_IXUSR, f"{prep_path} is not executable"
    assert os.stat(track_path).st_mode & stat.S_IXUSR, f"{track_path} is not executable"

def test_experiments_jsonl_format():
    """Check if experiments.jsonl exists and has the correct format and data."""
    jsonl_path = '/home/user/experiments.jsonl'
    assert os.path.exists(jsonl_path), f"Missing {jsonl_path}. Did track.sh run successfully?"

    with open(jsonl_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {jsonl_path}, found {len(lines)}"

    expected_n_words = [3, 5, 10]
    found_n_words = []

    for idx, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {idx+1} is not valid JSON: {line}"

        assert "n_words" in data, f"Missing 'n_words' key in line {idx+1}: {line}"
        assert "accuracy" in data, f"Missing 'accuracy' key in line {idx+1}: {line}"

        n_words = data["n_words"]
        accuracy = data["accuracy"]

        assert isinstance(n_words, int), f"'n_words' must be an integer, got {type(n_words)}"
        assert isinstance(accuracy, (float, int)), f"'accuracy' must be a float, got {type(accuracy)}"
        assert 0.0 <= accuracy <= 1.0, f"'accuracy' must be between 0 and 1, got {accuracy}"

        found_n_words.append(n_words)

    assert sorted(found_n_words) == expected_n_words, f"Expected n_words to be {expected_n_words}, got {sorted(found_n_words)}"