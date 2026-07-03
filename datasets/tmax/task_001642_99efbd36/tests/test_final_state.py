# test_final_state.py
import requests
import tarfile
import zipfile
import io
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_binaries_tar_gz():
    url = f"{BASE_URL}/binaries.tar.gz"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 for {url}, got {resp.status_code}"

    try:
        with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:gz") as tar:
            members = [m for m in tar.getmembers() if m.isfile()]
            assert len(members) == 2, f"Expected 2 files in binaries.tar.gz, found {len(members)}"

            for member in members:
                assert "/" not in member.name, f"File {member.name} should be at the root of the archive"
                f = tar.extractfile(member)
                content = f.read()
                assert content.startswith(b"\x7fELF"), f"File {member.name} in binaries.tar.gz is not an ELF file"
    except tarfile.TarError as e:
        pytest.fail(f"Failed to parse binaries.tar.gz as a valid tar.gz archive: {e}")

def test_manufacturing_zip():
    url = f"{BASE_URL}/manufacturing.zip"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 for {url}, got {resp.status_code}"

    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            members = [m for m in zf.infolist() if not m.is_dir()]
            assert len(members) == 2, f"Expected 2 files in manufacturing.zip, found {len(members)}"

            contents = []
            for member in members:
                assert "/" not in member.filename, f"File {member.filename} should be at the root of the archive"
                with zf.open(member) as f:
                    contents.append(f.read())

            # Check contents
            has_doc = any(b"M109 S200" in c and b"G1 X10" in c for c in contents)
            has_img = any(b"M109 S210" in c and b"G1 X20" in c for c in contents)
            assert has_doc and has_img, "manufacturing.zip does not contain the expected GCODE file contents"
    except zipfile.BadZipFile as e:
        pytest.fail(f"Failed to parse manufacturing.zip as a valid zip archive: {e}")

def test_database_logs_tar_bz2():
    url = f"{BASE_URL}/database_logs.tar.bz2"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 for {url}, got {resp.status_code}"

    try:
        with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:bz2") as tar:
            members = [m for m in tar.getmembers() if m.isfile()]
            assert len(members) == 2, f"Expected 2 files in database_logs.tar.bz2, found {len(members)}"

            contents = []
            for member in members:
                assert "/" not in member.name, f"File {member.name} should be at the root of the archive"
                f = tar.extractfile(member)
                contents.append(f.read())

            has_log1 = any(c.startswith(b"\x37\x7f\x06\x82") for c in contents)
            has_log2 = any(c.startswith(b"\x37\x7f\x06\x83") for c in contents)
            assert has_log1 and has_log2, "database_logs.tar.bz2 does not contain the expected WAL file contents"
    except tarfile.TarError as e:
        pytest.fail(f"Failed to parse database_logs.tar.bz2 as a valid tar.bz2 archive: {e}")