# test_final_state.py
import hashlib
import os

def test_manifest_similarity():
    base_dir = '/home/user/legacy_configs'
    expected_manifest = set()

    # Recompute expected state directly
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.ini'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r') as f:
                    content = f.read()

                # Note: the agent should have updated the file in place, 
                # but we can't assume they didn't, so we'll check the current content
                # and assume it has already been replaced, or we compute what it *should* be
                # if they didn't replace it correctly, the checksum will fail.
                # Wait, if they replaced it correctly, `content` is already replaced.
                # Let's just compute the expected content from the original state?
                # No, the instructions say: 
                # "The agent should have updated the file"
                # "expected_content = content.replace('db_pool_size=10', 'db_pool_size=50')"
                # If they already updated it, `replace('db_pool_size=10', 'db_pool_size=50')` does nothing,
                # which is fine! It works whether they updated it or not.
                expected_content = content.replace('db_pool_size=10', 'db_pool_size=50')

                h = hashlib.sha256(expected_content.encode('utf-8')).hexdigest()
                rel_path = os.path.relpath(full_path, base_dir)
                expected_manifest.add(f"{rel_path},{h}")

    agent_manifest = set()
    manifest_path = '/home/user/update_manifest.csv'
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, 'r') as f:
        for line in f:
            if line.strip():
                agent_manifest.add(line.strip())

    if not expected_manifest and not agent_manifest:
        similarity = 0.0
    else:
        intersection = len(expected_manifest.intersection(agent_manifest))
        union = len(expected_manifest.union(agent_manifest))
        similarity = intersection / union

    assert similarity >= 0.95, f"Manifest similarity {similarity} is below threshold 0.95. Expected {len(expected_manifest)} entries, got {len(agent_manifest)}."