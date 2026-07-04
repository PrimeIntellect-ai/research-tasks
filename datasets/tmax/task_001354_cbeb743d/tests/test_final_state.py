# test_final_state.py
import os
import tarfile

def test_markdown_archive_exists_and_valid():
    tar_path = '/home/user/markdown_archive.tar.gz'
    assert os.path.exists(tar_path), f"Tarball not found at {tar_path}"
    assert os.path.isfile(tar_path), f"{tar_path} is not a file"
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar file"

def test_markdown_archive_contents():
    tar_path = '/home/user/markdown_archive.tar.gz'
    assert os.path.exists(tar_path), "Tarball not found"

    expected_files = {
        "intro.md": b"# Introduction\nWelcome to the documentation.\n",
        "setup.md": b"## Setup\nRun `make install` to build.\n",
        "api.md": b"### API Reference\n- `get_data()`\n- `set_data()`\n"
    }

    with tarfile.open(tar_path, 'r:gz') as tar:
        names = tar.getnames()
        assert set(names) == set(expected_files.keys()), f"Incorrect files in tarball. Expected {set(expected_files.keys())}, got {set(names)}"

        for name, expected_content in expected_files.items():
            f = tar.extractfile(name)
            assert f is not None, f"Could not extract {name} from tarball"
            content = f.read()
            assert content == expected_content, f"Content of {name} does not match expected output"

def test_docs_extracted_directory():
    # The task asks to create /home/user/docs_extracted/ and put the extracted .md files there.
    docs_extracted_dir = '/home/user/docs_extracted'
    assert os.path.isdir(docs_extracted_dir), f"Directory {docs_extracted_dir} does not exist"

    expected_files = {
        "intro.md": b"# Introduction\nWelcome to the documentation.\n",
        "setup.md": b"## Setup\nRun `make install` to build.\n",
        "api.md": b"### API Reference\n- `get_data()`\n- `set_data()`\n"
    }

    for name, expected_content in expected_files.items():
        file_path = os.path.join(docs_extracted_dir, name)
        assert os.path.exists(file_path), f"File {name} not found in {docs_extracted_dir}"
        with open(file_path, 'rb') as f:
            content = f.read()
            assert content == expected_content, f"Content of {file_path} does not match expected output"