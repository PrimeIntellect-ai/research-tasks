# test_final_state.py

import os
import tarfile
import zipfile
import io

def test_updated_configs_archive():
    target_file = '/app/updated_configs.tar.xz'
    assert os.path.exists(target_file), f"Output file not found at {target_file}"

    size = os.path.getsize(target_file)
    assert size <= 102400, f"File size {size} is strictly greater than threshold 102400 bytes"

    # Verify contents
    with tarfile.open(target_file, 'r:xz') as tar:
        members = tar.getmembers()
        assert len(members) > 0, "The tar.xz archive is empty"
        for member in members:
            assert member.name.endswith('.zip'), f"Found non-zip member in tar: {member.name}"
            f = tar.extractfile(member)
            assert f is not None, f"Could not extract {member.name}"

            with zipfile.ZipFile(io.BytesIO(f.read())) as zf:
                namelist = zf.namelist()
                assert len(namelist) > 0, f"Zip file {member.name} is empty"
                for conf_name in namelist:
                    assert conf_name.endswith('.conf'), f"Found non-conf file in zip: {conf_name}"
                    content = zf.read(conf_name).decode('utf-8')
                    assert "MAX_CONNECTIONS=8192" in content, f"MAX_CONNECTIONS not correctly updated in {conf_name} of {member.name}"
                    assert "TIMEOUT=45" in content, f"TIMEOUT not correctly updated in {conf_name} of {member.name}"