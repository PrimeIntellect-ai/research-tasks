# test_final_state.py

import os
import sqlite3
import pytest

def test_directories_moved_correctly():
    pos_dir = "/home/user/organized_data/positive"
    neg_dir = "/home/user/organized_data/negative"

    assert os.path.isdir(pos_dir), f"{pos_dir} does not exist"
    assert os.path.isdir(neg_dir), f"{neg_dir} does not exist"

    assert os.path.isdir(os.path.join(pos_dir, "exp_alpha")), "exp_alpha should be in positive directory"
    assert os.path.isdir(os.path.join(pos_dir, "exp_gamma")), "exp_gamma should be in positive directory"
    assert os.path.isdir(os.path.join(neg_dir, "exp_beta")), "exp_beta should be in negative directory"

    assert not os.path.exists("/home/user/experiments/exp_alpha"), "exp_alpha should have been moved"
    assert not os.path.exists("/home/user/experiments/exp_beta"), "exp_beta should have been moved"
    assert not os.path.exists("/home/user/experiments/exp_gamma"), "exp_gamma should have been moved"

def test_database_entries():
    db_path = "/home/user/experiment_tracking.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results';")
    assert cursor.fetchone() is not None, "Table 'results' does not exist in the database"

    # Check positive scores
    cursor.execute("SELECT experiment_name FROM results WHERE mean_score > 0 ORDER BY experiment_name;")
    pos_results = [row[0] for row in cursor.fetchall()]
    assert pos_results == ["exp_alpha", "exp_gamma"], "Positive results in database do not match expected"

    # Check negative scores
    cursor.execute("SELECT experiment_name FROM results WHERE mean_score <= 0 ORDER BY experiment_name;")
    neg_results = [row[0] for row in cursor.fetchall()]
    assert neg_results == ["exp_beta"], "Negative results in database do not match expected"

    conn.close()