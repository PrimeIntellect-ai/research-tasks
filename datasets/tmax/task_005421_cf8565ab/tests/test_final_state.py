# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_analytics_score():
    """
    Fetches the metric score from the Analytics Service and verifies it meets the threshold.
    """
    url = "http://127.0.0.1:5001/score"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            score = float(data.get("score", 0.0))
    except Exception as e:
        pytest.fail(f"Failed to fetch score from analytics service at {url}: {e}\n"
                    "Ensure that your Rust worker is running, processed the archives, "
                    "and reported the results to the Analytics Service.")

    assert score >= 1.0, f"Metric threshold not met: expected score >= 1.0, but got {score}"

def test_organizer_project_exists():
    """
    Verifies that the Rust project directory was created.
    """
    assert os.path.isdir('/home/user/organizer'), (
        "The Rust project directory /home/user/organizer/ does not exist. "
        "Did you create your Rust program in the correct location?"
    )

def test_projects_extracted():
    """
    Verifies that the projects directory contains extracted subdirectories.
    """
    projects_dir = '/home/user/projects'
    assert os.path.isdir(projects_dir), f"The extraction directory {projects_dir} does not exist."

    contents = os.listdir(projects_dir)
    assert len(contents) > 0, (
        f"No extracted projects found in {projects_dir}. "
        "Your worker should extract the tar files into this directory."
    )