# test_final_state.py

import os
import json
import shutil
import subprocess
import tempfile
import hashlib
import urllib.request
import urllib.error
import pytest

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Sanitizer script not found at {sanitizer_path}"

    clean_corpus = "/app/test_corpus/clean"
    evil_corpus = "/app/test_corpus/evil"

    with tempfile.TemporaryDirectory() as temp_in, tempfile.TemporaryDirectory() as temp_out:
        clean_files = set(os.listdir(clean_corpus)) if os.path.exists(clean_corpus) else set()
        evil_files = set(os.listdir(evil_corpus)) if os.path.exists(evil_corpus) else set()

        for f in clean_files:
            shutil.copy(os.path.join(clean_corpus, f), os.path.join(temp_in, f))
        for f in evil_files:
            shutil.copy(os.path.join(evil_corpus, f), os.path.join(temp_in, f))

        try:
            result = subprocess.run(
                ["python3", sanitizer_path, "--input", temp_in, "--output", temp_out],
                capture_output=True, text=True, timeout=10
            )
        except subprocess.TimeoutExpired:
            pytest.fail("Sanitizer script timed out after 10 seconds.")

        assert result.returncode == 0, f"Sanitizer script failed with return code {result.returncode}.\nStderr: {result.stderr}"

        output_files = set(os.listdir(temp_out))
        if "manifest.json" in output_files:
            output_files.remove("manifest.json")

        bypassed_evil = evil_files.intersection(output_files)
        missing_clean = clean_files - output_files
        modified_clean = set()

        # Check clean files content and encoding
        for f in clean_files:
            if f in output_files:
                out_path = os.path.join(temp_out, f)
                try:
                    with open(out_path, 'r', encoding='utf-8') as out_f:
                        out_content = out_f.read()
                except UnicodeDecodeError:
                    modified_clean.add(f)

        error_msgs = []
        if bypassed_evil:
            error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
        if missing_clean or modified_clean:
            error_msgs.append(f"{len(missing_clean) + len(modified_clean)} of {len(clean_files)} clean modified or missing: {', '.join(missing_clean.union(modified_clean))}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))

        # Check manifest.json
        manifest_path = os.path.join(temp_out, "manifest.json")
        assert os.path.isfile(manifest_path), "manifest.json was not generated in the output directory."

        with open(manifest_path, 'r', encoding='utf-8') as mf:
            try:
                manifest_data = json.load(mf)
            except json.JSONDecodeError:
                pytest.fail("manifest.json is not valid JSON.")

        assert "files" in manifest_data, "manifest.json missing 'files' key."
        manifest_files = {item.get("filename"): item.get("sha256") for item in manifest_data["files"]}

        for f in clean_files:
            assert f in manifest_files, f"Clean file {f} missing from manifest.json."
            out_path = os.path.join(temp_out, f)
            with open(out_path, 'rb') as out_f:
                expected_hash = hashlib.sha256(out_f.read()).hexdigest()
            assert manifest_files[f] == expected_hash, f"Hash mismatch in manifest for {f}. Expected {expected_hash}, got {manifest_files[f]}"

def test_multi_service_stack():
    # Test Nginx manifest endpoint
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/manifest.json")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200 for manifest.json, got {response.status}"
            manifest_content = response.read().decode('utf-8')
            manifest_data = json.loads(manifest_content)
    except Exception as e:
        pytest.fail(f"Failed to fetch or parse /manifest.json from Nginx: {e}")

    assert "files" in manifest_data, "manifest.json fetched from Nginx missing 'files' key."

    if manifest_data["files"]:
        sample_file = manifest_data["files"][0]["filename"]
        try:
            req = urllib.request.Request(f"http://127.0.0.1:8080/docs/{sample_file}")
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"Expected status 200 for /docs/{sample_file}, got {response.status}"
                doc_content = response.read()
                # Check if it matches the hash
                expected_hash = manifest_data["files"][0]["sha256"]
                actual_hash = hashlib.sha256(doc_content).hexdigest()
                assert actual_hash == expected_hash, f"Content hash mismatch for {sample_file} via Nginx proxy."
        except Exception as e:
            pytest.fail(f"Failed to fetch /docs/{sample_file} from Nginx proxy: {e}")