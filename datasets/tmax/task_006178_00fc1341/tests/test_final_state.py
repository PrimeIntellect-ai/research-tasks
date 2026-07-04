# test_final_state.py
import os
import hashlib
import stat

PROCESSED_CONFIGS_DIR = "/home/user/processed_configs"
SCRIPT_PATH = "/home/user/process_configs.sh"

EXPECTED_FILES = {
    "production_database_config_a.txt.conf": "# ENV: production\n# SERVICE: database\nparam=1\n",
    "staging_web_server_config_b.txt.conf": "# ENV: staging\n# SERVICE: web server\nparam=2\n",
    "qa_auth_config_c.txt.conf": "Random data\n# ENV: qa\n# SERVICE: auth\nparam=3\n"
}

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_processed_files_exist_and_content_correct():
    assert os.path.isdir(PROCESSED_CONFIGS_DIR), f"Directory {PROCESSED_CONFIGS_DIR} does not exist."

    for filename, expected_content in EXPECTED_FILES.items():
        filepath = os.path.join(PROCESSED_CONFIGS_DIR, filename)
        assert os.path.isfile(filepath), f"Expected processed file {filename} is missing."

        with open(filepath, 'r') as f:
            content = f.read()

        # Check if content matches (allowing for minor differences in trailing newlines)
        assert content.strip() == expected_content.strip(), f"Content of {filename} does not match expected."

def test_no_extra_files_processed():
    files_in_dir = set(f for f in os.listdir(PROCESSED_CONFIGS_DIR) if os.path.isfile(os.path.join(PROCESSED_CONFIGS_DIR, f)))
    expected_filenames = set(EXPECTED_FILES.keys())
    expected_filenames.add("manifest.sha256")

    extra_files = files_in_dir - expected_filenames
    assert not extra_files, f"Found unexpected files in processed configs directory: {extra_files}"

def test_manifest_correctness():
    manifest_path = os.path.join(PROCESSED_CONFIGS_DIR, "manifest.sha256")
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, 'r') as f:
        manifest_lines = f.read().strip().splitlines()

    assert len(manifest_lines) == len(EXPECTED_FILES), f"Manifest should contain exactly {len(EXPECTED_FILES)} entries, found {len(manifest_lines)}."

    manifest_dict = {}
    for line in manifest_lines:
        parts = line.strip().split(None, 1)
        assert len(parts) == 2, f"Invalid manifest line format: {line}"
        hash_val, filename = parts
        # Filename should be just the basename
        assert os.path.basename(filename) == filename, f"Manifest should only contain basenames, found path: {filename}"
        filename = filename.lstrip('*') # handle potential binary mode prefix in sha256sum
        manifest_dict[filename] = hash_val

    for filename, expected_content in EXPECTED_FILES.items():
        assert filename in manifest_dict, f"File {filename} is missing from manifest."

        filepath = os.path.join(PROCESSED_CONFIGS_DIR, filename)
        with open(filepath, 'rb') as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        assert manifest_dict[filename] == actual_hash, f"Manifest hash for {filename} is incorrect. Expected {actual_hash}, got {manifest_dict[filename]}."