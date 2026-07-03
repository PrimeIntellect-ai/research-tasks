# test_final_state.py
import os
import stat
import subprocess
import math

def compute_pearson(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x) ** 2 for xi in x)
    den_y = sum((yi - mean_y) ** 2 for yi in y)

    den = math.sqrt(den_x * den_y)
    if den == 0:
        return 0.0
    return num / den

def get_expected_top_match(target_user_id=1):
    ratings_file = "/home/user/ratings.csv"
    assert os.path.exists(ratings_file), f"Missing {ratings_file}"

    users = {}
    with open(ratings_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            user_id = int(parts[0])
            ratings = [float(p) for p in parts[1:]]
            users[user_id] = ratings

    assert target_user_id in users, f"Target user {target_user_id} not found in dataset."

    target_ratings = users[target_user_id]

    best_match = None
    best_score = -float('inf')

    for uid, ratings in users.items():
        if uid == target_user_id:
            continue
        score = compute_pearson(target_ratings, ratings)

        if score > best_score:
            best_score = score
            best_match = uid
        elif score == best_score:
            if best_match is None or uid < best_match:
                best_match = uid

    return best_match, best_score

def test_files_exist():
    """Verify all required files exist."""
    required_files = [
        "/home/user/recommender.c",
        "/home/user/Makefile",
        "/home/user/run_pipeline.sh"
    ]
    for f in required_files:
        assert os.path.isfile(f), f"Required file {f} is missing."

def test_makefile_contents():
    """Verify Makefile contains math library linking."""
    with open("/home/user/Makefile", "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not appear to link the math library (-lm)."

def test_script_executable():
    """Verify run_pipeline.sh is executable."""
    script_path = "/home/user/run_pipeline.sh"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_pipeline_execution():
    """Run the pipeline script and verify it succeeds."""
    script_path = "/home/user/run_pipeline.sh"

    # Remove top_match.txt if it exists to ensure the script generates it
    output_file = "/home/user/top_match.txt"
    if os.path.exists(output_file):
        os.remove(output_file)

    result = subprocess.run(["bash", script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.isfile(output_file), f"Pipeline script did not generate {output_file}."

def test_top_match_output():
    """Verify the contents of top_match.txt against the expected ground truth."""
    output_file = "/home/user/top_match.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_match, expected_score = get_expected_top_match(1)
    expected_str = f"Match: {expected_match}, Score: {expected_score:.4f}"

    assert content == expected_str, f"Output content mismatch.\nExpected: '{expected_str}'\nFound: '{content}'"