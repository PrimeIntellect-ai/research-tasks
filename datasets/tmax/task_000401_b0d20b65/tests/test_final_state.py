# test_final_state.py

import os
import glob
import json
import requests
import re

def get_dependencies(directory):
    files = glob.glob(os.path.join(directory, "*.py"))
    basenames = [os.path.basename(f) for f in files]
    modules_in_dir = [os.path.splitext(b)[0] for b in basenames]

    deps = {}
    for fpath in files:
        bname = os.path.basename(fpath)
        deps[bname] = []
        with open(fpath, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'^\s*import\s+([a-zA-Z0-9_]+)', line)
                if match:
                    imported = match.group(1)
                    if imported in modules_in_dir:
                        deps[bname].append(imported + ".py")
    return deps

def test_api_and_modularity_score():
    target_dir = "/app/eval_project/"

    try:
        resp = requests.post("http://localhost:8000/organize", json={"dir": target_dir}, timeout=10)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to API on port 8000: {e}"

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {resp.text}"

    assert "score" in data, "Response JSON missing 'score' key."
    assert "modules" in data, "Response JSON missing 'modules' key."

    modules = data["modules"]

    # Verify constraint: max 3 files per module
    for mod_name, files in modules.items():
        assert len(files) <= 3, f"Module '{mod_name}' exceeds 3 files limit: {files}"

    # Check that all files in the target directory are accounted for
    all_target_files = set(os.path.basename(f) for f in glob.glob(os.path.join(target_dir, "*.py")))
    all_assigned_files = set()
    for files in modules.values():
        all_assigned_files.update(files)

    assert all_target_files.issubset(all_assigned_files), "Not all files in the directory were assigned to a module."

    # Recalculate score
    deps = get_dependencies(target_dir)

    total_edges = sum(len(d) for d in deps.values())

    intra_edges = 0
    for mod_name, files in modules.items():
        files_set = set(files)
        for f in files:
            if f in deps:
                for imported in deps[f]:
                    if imported in files_set:
                        intra_edges += 1

    if total_edges == 0:
        real_score = 1.0
    else:
        real_score = intra_edges / total_edges

    # Check if agent score matches real score
    agent_score = data["score"]
    assert abs(agent_score - real_score) < 0.01, f"Agent reported score {agent_score}, but recalculated score is {real_score}."

    # Check metric threshold
    assert real_score >= 0.80, f"Modularity score {real_score} is below the required threshold of 0.80."