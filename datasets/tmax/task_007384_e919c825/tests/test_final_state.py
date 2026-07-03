# test_final_state.py
import os
import hashlib
import stat

def test_script_exists_and_executable():
    script_path = "/home/user/snapshot_configs.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a regular file"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable by the owner"

def test_snapshot_output_correct():
    output_path = "/home/user/config_snapshot.log"
    assert os.path.exists(output_path), f"Output file not found at {output_path}. Did you run the script?"

    # Compute expected output dynamically
    baseline_stamp = "/home/user/system/baseline.stamp"
    overrides_file = "/home/user/system/overrides.txt"
    configs_dir = "/home/user/system/configs"

    assert os.path.exists(baseline_stamp), "Baseline stamp file missing"
    assert os.path.exists(overrides_file), "Overrides file missing"

    baseline_mtime = os.path.getmtime(baseline_stamp)

    with open(overrides_file, 'r') as f:
        overrides = set(line.strip() for line in f if line.strip())

    results = []
    for root, _, files in os.walk(configs_dir):
        for file in files:
            if file.endswith('.conf'):
                filepath = os.path.join(root, file)

                # 2. Exclusion List
                if filepath in overrides:
                    continue

                # 1. Size greater than 0
                if os.path.getsize(filepath) == 0:
                    continue

                # 1. Strictly newer than baseline stamp
                if os.path.getmtime(filepath) <= baseline_mtime:
                    continue

                # 3. File Splitting and Parsing
                with open(filepath, 'rb') as f:
                    content = f.read()

                chunk_index = 0
                for i in range(0, len(content), 50):
                    chunk = content[i:i+50]
                    h = hashlib.sha256(chunk).hexdigest()
                    results.append(f"{filepath}:{chunk_index}:{h}")
                    chunk_index += 1

    # 4. Merging and Formatting (Sort alphabetically by path, then numerically by index)
    def sort_key(line):
        parts = line.split(':')
        return (parts[0], int(parts[1]))

    results.sort(key=sort_key)
    expected_content = "\n".join(results)

    with open(output_path, 'r') as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"Content of {output_path} does not match expected output.\n"
        f"Expected:\n{expected_content.strip()}\n\n"
        f"Actual:\n{actual_content.strip()}"
    )