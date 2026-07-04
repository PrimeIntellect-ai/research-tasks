# test_final_state.py

import os
import tarfile

def test_final_state():
    archive_dir = "/home/user/archive"
    updated_archive = os.path.join(archive_dir, "updated_docs.tar.gz")
    temp_updated_archive = os.path.join(archive_dir, "updated_docs.tar.gz.tmp")

    # 1. The final file must exist
    assert os.path.isfile(updated_archive), f"The final archive {updated_archive} does not exist."

    # 2. The temporary file must NOT exist
    assert not os.path.exists(temp_updated_archive), f"The temporary file {temp_updated_archive} should have been renamed/removed."

    # 3. Extracting/reading should yield valid files and correct content
    nova_corp_count = 0
    file_count = 0

    try:
        with tarfile.open(updated_archive, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile():
                    file_count += 1
                    f = tar.extractfile(member)
                    content = f.read().decode('utf-8', errors='replace')

                    # 4. Searching for old name should return 0 results
                    assert "AcmeCorp" not in content, f"Found 'AcmeCorp' in {member.name} inside the updated archive. It should be replaced."

                    # Count new name occurrences
                    nova_corp_count += content.count("NovaCorp")
    except tarfile.TarError as e:
        assert False, f"Failed to read {updated_archive} as a gzip-compressed tar archive: {e}"

    assert file_count > 0, "The updated archive contains no files."

    # 5. Searching for new name should return > 0 results
    assert nova_corp_count > 0, "Could not find 'NovaCorp' in the updated archive. Replacement may have failed."