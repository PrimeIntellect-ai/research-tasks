# test_final_state.py
import os
import tarfile
import shutil
import pytest

def test_updated_docs_archive_accuracy():
    target_archive = '/home/user/updated_docs.tar.gz'
    assert os.path.exists(target_archive), f"Target archive not found at {target_archive}"

    extract_dir = '/tmp/verify_docs_test'
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    try:
        with tarfile.open(target_archive, 'r:gz') as tar:
            tar.extractall(path=extract_dir)
    except Exception as e:
        pytest.fail(f"Failed to extract {target_archive}: {e}")

    expected_replacements = {
        "ACME_CORP": "GLOBAL_TECH_INC",
        "LEGACY_SYSTEM_V1": "CLOUD_NATIVE_V2",
        "USER_MANUAL": "ADMIN_GUIDE"
    }

    correct = 0
    incorrect = 0

    txt_count = 0
    xml_count = 0

    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.endswith('.txt'):
                txt_count += 1
                with open(os.path.join(root, f), 'r') as fd:
                    content = fd.read()
                    for old, new in expected_replacements.items():
                        correct += content.count(new)
                        incorrect += content.count(old)
            elif f.endswith('.xml'):
                xml_count += 1
                with open(os.path.join(root, f), 'r') as fd:
                    content = fd.read()
                    for old, new in expected_replacements.items():
                        correct += content.count(new)
                        incorrect += content.count(old)

    assert txt_count > 0 or xml_count > 0, "No .txt or .xml files found in the extracted archive."

    # Based on the setup, there are 10 txt files and 10 xml files.
    # Each txt file has 3 terms to replace. Each xml file has 2 terms to replace.
    # 10 * 3 + 10 * 2 = 50
    total_expected = 50 

    score = max(0.0, (correct - incorrect) / total_expected)

    assert score >= 0.95, f"Term replacement accuracy is {score:.2f}, which is below the threshold of 0.95. (Correct: {correct}, Incorrect remaining: {incorrect})"