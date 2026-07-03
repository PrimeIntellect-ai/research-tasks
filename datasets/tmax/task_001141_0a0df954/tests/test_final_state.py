# test_final_state.py
import os
import json
import glob
import subprocess
import tempfile

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), "report.json is missing"
    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "report.json is not valid JSON"

    assert "total_raw_frames" in data, "total_raw_frames key missing in report.json"
    assert data["total_raw_frames"] == 60, f"total_raw_frames should be 60, got {data['total_raw_frames']}"

    assert "total_clean_frames" in data, "total_clean_frames key missing in report.json"
    assert data["total_clean_frames"] == 50, f"total_clean_frames should be 50, got {data['total_clean_frames']}"

    assert "cv_accuracy" in data, "cv_accuracy key missing in report.json"
    assert isinstance(data["cv_accuracy"], (int, float)), "cv_accuracy must be a number"
    assert 0.90 <= data["cv_accuracy"] <= 1.0, f"cv_accuracy should be between 0.90 and 1.0, got {data['cv_accuracy']}"

def test_frames_extracted():
    raw_frames = glob.glob("/home/user/raw_frames/*.jpg") + glob.glob("/home/user/raw_frames/*.png")
    assert len(raw_frames) == 60, f"Expected exactly 60 raw frames, found {len(raw_frames)}"

    clean_frames = glob.glob("/home/user/clean_frames/*.jpg") + glob.glob("/home/user/clean_frames/*.png")
    assert len(clean_frames) == 50, f"Expected exactly 50 clean frames, found {len(clean_frames)}"

def test_adversarial_corpus():
    script_path = "/home/user/filter_dataset.py"
    assert os.path.exists(script_path), f"Script {script_path} not found"

    clean_dir = "/app/secret_eval/clean"
    evil_dir = "/app/secret_eval/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus dir {clean_dir} missing"
    assert os.path.isdir(evil_dir), f"Evil corpus dir {evil_dir} missing"

    with tempfile.TemporaryDirectory() as out_clean, tempfile.TemporaryDirectory() as out_evil:
        # Test clean corpus
        try:
            subprocess.run(["python3", script_path, clean_dir, out_clean], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            assert False, f"Script failed on clean corpus:\n{e.stderr}"

        clean_input_files = [f for f in os.listdir(clean_dir) if f.endswith(('.jpg', '.png'))]
        clean_output_files = os.listdir(out_clean)

        missing_clean = set(clean_input_files) - set(clean_output_files)
        assert not missing_clean, f"{len(missing_clean)} of {len(clean_input_files)} clean modified/rejected. Offending files: {list(missing_clean)[:5]}"

        # Test evil corpus
        try:
            subprocess.run(["python3", script_path, evil_dir, out_evil], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            assert False, f"Script failed on evil corpus:\n{e.stderr}"

        evil_input_files = [f for f in os.listdir(evil_dir) if f.endswith(('.jpg', '.png'))]
        evil_output_files = os.listdir(out_evil)

        bypassed_evil = set(evil_output_files)
        assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_input_files)} evil bypassed. Offending files: {list(bypassed_evil)[:5]}"