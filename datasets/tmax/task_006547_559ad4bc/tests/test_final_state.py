# test_final_state.py
import os
import tarfile
import tempfile
import re

def test_parser_c_exists():
    assert os.path.exists('/home/user/parser.c'), "parser.c does not exist"
    assert os.path.isfile('/home/user/parser.c'), "parser.c is not a file"

def test_parser_executable_exists():
    assert os.path.exists('/home/user/parser'), "compiled parser does not exist"
    assert os.path.isfile('/home/user/parser'), "parser is not a file"
    assert os.access('/home/user/parser', os.X_OK), "parser is not executable"

def test_metadata_csv_contents():
    csv_path = '/home/user/metadata.csv'
    assert os.path.exists(csv_path), "metadata.csv does not exist"

    expected_lines = [
        "docs/api/v1.txt,Bob,2021-05-12",
        "docs/api/v2.txt,Charlie,2022-10-10",
        "docs/guides/guide1.txt,Dave,UNKNOWN",
        "docs/intro.txt,Alice,2020-01-01"
    ]

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"metadata.csv contents do not match expected. Got: {lines}"

def test_processed_docs_archive():
    archive_path = '/home/user/processed_docs.tar.gz'
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist"
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive"

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()

        # Check metadata.csv is in archive
        assert 'metadata.csv' in names or './metadata.csv' in names, "metadata.csv not found in processed_docs.tar.gz"

        # Check docs files are in archive
        docs_files = [n for n in names if n.startswith('docs/') and n.endswith('.txt')]
        assert len(docs_files) == 4, "Not all expected docs files are in the archive"

        # Verify normalization
        for member in tar.getmembers():
            if member.name.startswith('docs/') and member.name.endswith('.txt'):
                f = tar.extractfile(member)
                content = f.read().decode('utf-8')

                # Check for unnormalized tags
                assert not re.search(r'%%\s+AUTHOR', content), f"Unnormalized AUTHOR tag found in {member.name}"
                assert not re.search(r'AUTHOR\s+:', content), f"Unnormalized AUTHOR tag found in {member.name}"
                assert not re.search(r':\s+', content[:content.find('%%AUTHOR:')+20] if '%%AUTHOR:' in content else content), f"Unnormalized spaces after colon in {member.name}"

                assert not re.search(r'%%\s+DATE', content), f"Unnormalized DATE tag found in {member.name}"
                assert not re.search(r'DATE\s+:', content), f"Unnormalized DATE tag found in {member.name}"