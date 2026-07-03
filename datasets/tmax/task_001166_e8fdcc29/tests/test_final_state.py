# test_final_state.py
import os

def test_directory_and_files_exist():
    base_dir = "/home/user/spectro_sim"
    assert os.path.isdir(base_dir), f"Directory {base_dir} does not exist."

    expected_files = ["go.mod", "simulate.go", "run_pipeline.sh", "peaks.csv", "top_peaks.txt", "simulator"]
    for f in expected_files:
        assert os.path.isfile(os.path.join(base_dir, f)), f"Expected file {f} does not exist."

    script_path = os.path.join(base_dir, "run_pipeline.sh")
    assert os.access(script_path, os.X_OK), "run_pipeline.sh is not executable."

def test_go_mod_content():
    with open("/home/user/spectro_sim/go.mod", "r") as f:
        content = f.read()
    assert "module spectro_sim" in content, "go.mod does not contain 'module spectro_sim'."

def test_peaks_csv_format():
    with open("/home/user/spectro_sim/peaks.csv", "r") as f:
        lines = f.readlines()
    assert len(lines) > 1, "peaks.csv should have a header and at least one data row."
    assert lines[0].strip() == "BinIndex,BinCenter,SmoothedCount", "peaks.csv header is incorrect."

def test_top_peaks_txt_content():
    with open("/home/user/spectro_sim/top_peaks.txt", "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    assert len(lines) == 2, f"top_peaks.txt should contain exactly 2 lines, found {len(lines)}."

    vals = []
    for line in lines:
        try:
            vals.append(float(line))
        except ValueError:
            assert False, f"Could not parse '{line}' as float in top_peaks.txt."

    has_4_5 = any(4.4 <= v <= 4.6 for v in vals)
    has_7_5 = any(7.4 <= v <= 7.6 for v in vals)

    assert has_4_5, f"Expected a peak near 4.5 in top_peaks.txt, got: {vals}"
    assert has_7_5, f"Expected a peak near 7.5 in top_peaks.txt, got: {vals}"