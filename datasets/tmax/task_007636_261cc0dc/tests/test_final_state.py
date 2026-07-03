# test_final_state.py

import os
import tarfile
import json
import py_compile
import tempfile

def test_artifact_exists():
    artifact = "/home/user/migration/artifact.tar.gz"
    assert os.path.exists(artifact), f"Artifact {artifact} not found."
    assert os.path.isfile(artifact), f"{artifact} is not a file."
    assert tarfile.is_tarfile(artifact), f"{artifact} is not a valid tar archive."

def test_artifact_contents():
    artifact = "/home/user/migration/artifact.tar.gz"
    assert os.path.exists(artifact), "Artifact not found."

    with tarfile.open(artifact, "r:gz") as tar:
        names = tar.getnames()
        expected_names = {"version.info", "migrate.py", "output.json"}
        assert set(names) == expected_names, f"Tarball contains incorrect files. Expected {expected_names}, got {set(names)}"

def test_version_info_content():
    artifact = "/home/user/migration/artifact.tar.gz"
    assert os.path.exists(artifact), "Artifact not found."

    with tarfile.open(artifact, "r:gz") as tar:
        with tar.extractfile("version.info") as f:
            content = f.read().decode('utf-8').strip()
            assert content == "v2.0.1", f"Incorrect version in version.info: expected 'v2.0.1', got '{content}'"

def test_output_json_content():
    artifact = "/home/user/migration/artifact.tar.gz"
    assert os.path.exists(artifact), "Artifact not found."

    with tarfile.open(artifact, "r:gz") as tar:
        with tar.extractfile("output.json") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                assert False, "output.json is not valid JSON."

            assert isinstance(data, list), "output.json should contain a list of objects."
            assert len(data) == 3, f"output.json should have 3 records, found {len(data)}."

            expected_ids = {101, 102, 103}
            found_ids = set()
            for item in data:
                assert "new_id" in item, "Missing 'new_id' in output record."
                assert "full_name" in item, "Missing 'full_name' in output record."
                assert "is_admin" in item, "Missing 'is_admin' in output record."
                found_ids.add(item["new_id"])

            assert expected_ids == found_ids, f"Output JSON missing correct new_id fields. Expected {expected_ids}, got {found_ids}."

def test_migrate_py_syntax():
    artifact = "/home/user/migration/artifact.tar.gz"
    assert os.path.exists(artifact), "Artifact not found."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(artifact, "r:gz") as tar:
            tar.extract("migrate.py", path=tmpdir)

        extracted_script = os.path.join(tmpdir, "migrate.py")
        try:
            py_compile.compile(extracted_script, doraise=True)
        except py_compile.PyCompileError as e:
            assert False, f"migrate.py has Python 3 syntax errors: {e}"