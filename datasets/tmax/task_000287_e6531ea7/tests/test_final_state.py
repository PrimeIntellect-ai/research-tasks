# test_final_state.py
import os
import stat

def test_elf_files_moved():
    bin_dir = "/home/user/organized/bin"
    assert os.path.isdir(bin_dir), f"Directory {bin_dir} does not exist."

    prog_a = os.path.join(bin_dir, "program_a")
    prog_b = os.path.join(bin_dir, "program_b")
    not_elf = os.path.join(bin_dir, "not_elf_program")

    assert os.path.isfile(prog_a), f"ELF file {prog_a} is missing."
    assert os.path.isfile(prog_b), f"ELF file {prog_b} is missing."
    assert not os.path.exists(not_elf), f"Non-ELF file {not_elf} should not be in {bin_dir}."

def test_gcode_times_report():
    report_path = "/home/user/organized/gcode_times.txt"
    assert os.path.isfile(report_path), f"Report {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "part1.gcode: 3600s",
        "part2_noext: 8450s"
    ]
    assert lines == expected_lines, f"Contents of {report_path} are incorrect. Expected {expected_lines}, got {lines}."

def test_log_splitting():
    extracted_dir = "/home/user/extracted"

    aa_log = os.path.join(extracted_dir, "system_part_aa.log")
    ab_log = os.path.join(extracted_dir, "system_part_ab.log")
    ac_log = os.path.join(extracted_dir, "system_part_ac.log")
    original_log = os.path.join(extracted_dir, "system.log")

    assert not os.path.exists(original_log), f"Original log file {original_log} was not deleted."
    assert os.path.isfile(aa_log), f"Split log {aa_log} is missing."
    assert os.path.isfile(ab_log), f"Split log {ab_log} is missing."
    assert os.path.isfile(ac_log), f"Split log {ac_log} is missing."

    with open(aa_log, "r") as f:
        assert len(f.readlines()) == 500, f"{aa_log} should have exactly 500 lines."
    with open(ab_log, "r") as f:
        assert len(f.readlines()) == 500, f"{ab_log} should have exactly 500 lines."
    with open(ac_log, "r") as f:
        assert len(f.readlines()) == 200, f"{ac_log} should have exactly 200 lines."

def test_build_index_script():
    script_path = "/home/user/build_index.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "flock" in content, "Script does not contain 'flock'."
    assert "&" in content, "Script does not contain '&' for background jobs."
    assert "wait" in content, "Script does not contain 'wait'."

def test_master_index_contents():
    index_path = "/home/user/organized/master_index.txt"
    assert os.path.isfile(index_path), f"Master index {index_path} is missing."

    with open(index_path, "r") as f:
        lines = sorted([line.strip() for line in f if line.strip()])

    # We only check standard text files and log chunks to avoid issues with the MZ binary rendering
    expected_entries = [
        "changelog.md | Changelog for V2",
        "part1.gcode | ; FLAVOR:Marlin",
        "part2_noext | ; FLAVOR:Marlin",
        "readme.txt | Project Alpha Documentation",
        "system_part_aa.log | Log Started",
        "system_part_ab.log | Log entry line 501",
        "system_part_ac.log | Log entry line 1001"
    ]

    for expected in expected_entries:
        assert any(expected in line for line in lines), f"Expected entry '{expected}' not found in {index_path}."