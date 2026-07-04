# test_final_state.py
import os
import json
import tarfile
import tempfile

def test_master_output_exists_and_content():
    master_path = '/home/user/master_output.json'
    assert os.path.exists(master_path), f"File {master_path} does not exist."

    with open(master_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 11, f"Expected 11 lines in {master_path}, found {len(lines)}."

    # Parse lines as JSON to avoid strict string matching issues (e.g. spacing)
    records = []
    for i, line in enumerate(lines):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in {master_path} is not valid JSON: {line}"

    expected_apollo = {"id": "101", "project_name": "Apollo", "status": "active"}
    expected_dummy = {"id": "999", "project_name": "final_check", "status": "completed"}

    assert expected_apollo in records, f"Record {expected_apollo} not found in {master_path}."
    assert expected_dummy in records, f"Dummy record {expected_dummy} not found in {master_path}."

def test_backup_level0():
    backup0_path = '/home/user/backup_level0.tar'
    assert os.path.exists(backup0_path), f"Backup file {backup0_path} does not exist."

    with tarfile.open(backup0_path, 'r') as tar:
        members = tar.getnames()
        master_member = [m for m in members if m.endswith('master_output.json')]
        assert master_member, f"master_output.json not found in {backup0_path}."

        with tempfile.TemporaryDirectory() as tmpdir:
            tar.extract(master_member[0], path=tmpdir)
            extracted_file = os.path.join(tmpdir, master_member[0])
            with open(extracted_file, 'r') as f:
                lines = f.read().splitlines()

            assert len(lines) == 10, f"Expected 10 lines in Level 0 backup of master_output.json, found {len(lines)}."

            # Ensure dummy is NOT in level 0
            for line in lines:
                try:
                    record = json.loads(line)
                    assert record.get("id") != "999", "Dummy record found in Level 0 backup, which should only have 10 original records."
                except json.JSONDecodeError:
                    pass

def test_backup_level1():
    backup1_path = '/home/user/backup_level1.tar'
    assert os.path.exists(backup1_path), f"Backup file {backup1_path} does not exist."

    with tarfile.open(backup1_path, 'r') as tar:
        members = tar.getnames()
        master_member = [m for m in members if m.endswith('master_output.json')]
        assert master_member, f"master_output.json not found in {backup1_path}."

        with tempfile.TemporaryDirectory() as tmpdir:
            tar.extract(master_member[0], path=tmpdir)
            extracted_file = os.path.join(tmpdir, master_member[0])
            with open(extracted_file, 'r') as f:
                lines = f.read().splitlines()

            assert len(lines) == 11, f"Expected 11 lines in Level 1 backup of master_output.json, found {len(lines)}."

            dummy_found = False
            for line in lines:
                try:
                    record = json.loads(line)
                    if record.get("id") == "999":
                        dummy_found = True
                        break
                except json.JSONDecodeError:
                    pass

            assert dummy_found, "Dummy record not found in Level 1 backup."

def test_c_program_compiled():
    c_source = '/home/user/transformer.c'
    c_bin = '/home/user/transformer'

    assert os.path.exists(c_source), f"C source file {c_source} does not exist."
    assert os.path.exists(c_bin), f"Compiled binary {c_bin} does not exist."
    assert os.access(c_bin, os.X_OK), f"Compiled binary {c_bin} is not executable."