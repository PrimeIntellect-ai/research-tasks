# test_final_state.py
import os
import tarfile
import tempfile
import stat

def test_script_exists_and_executable():
    script_path = '/home/user/process_docs.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_original_files_untouched():
    docs_dir = '/home/user/docs_raw'
    assert os.path.isdir(docs_dir), f"Directory {docs_dir} is missing."
    files = [f for f in os.listdir(docs_dir) if f.endswith('.txt')]
    assert len(files) == 50, f"Expected 50 original .txt files, found {len(files)}. Original files may have been deleted."

def test_archive_exists_and_header():
    archive_path = '/home/user/final_docs.cgz'
    assert os.path.exists(archive_path), f"Archive {archive_path} not found."

    with open(archive_path, 'rb') as f:
        header = f.read(14)
        assert header == b'DOCARCHIVE_V1\n', f"Invalid custom header. Expected b'DOCARCHIVE_V1\\n', got {header}"

def test_archive_contents():
    archive_path = '/home/user/final_docs.cgz'
    assert os.path.exists(archive_path), f"Archive {archive_path} not found."

    with open(archive_path, 'rb') as f:
        f.seek(14)
        gz_data = f.read()

    with tempfile.TemporaryDirectory() as tmpdir:
        gz_path = os.path.join(tmpdir, 'payload.tar.gz')
        with open(gz_path, 'wb') as f:
            f.write(gz_data)

        try:
            with tarfile.open(gz_path, 'r:gz') as tar:
                tar.extractall(path=tmpdir)
        except Exception as e:
            raise AssertionError(f"Failed to decompress and extract tarball: {e}")

        extracted_files = [f for f in os.listdir(tmpdir) if f.endswith('.md')]
        assert len(extracted_files) == 20, f"Expected 20 .md files in the archive, found {len(extracted_files)}."

        for md_file in extracted_files:
            with open(os.path.join(tmpdir, md_file), 'r') as f:
                content = f.read()
                assert "STATUS: FINAL" in content, f"File {md_file} is missing 'STATUS: FINAL'."
                assert "[HEADER]" not in content, f"File {md_file} still contains '[HEADER]'."
                assert "\n# " in content or content.startswith("# "), f"File {md_file} does not contain the replaced '# ' header."