# test_final_state.py
import os
import tarfile
import tempfile
import re

def test_clean_docs_archive_exists():
    path = '/home/user/clean_docs.tar.gz'
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert tarfile.is_tarfile(path), f"File {path} is not a valid tar archive."

def test_clean_docs_contents():
    path = '/home/user/clean_docs.tar.gz'
    expected_files = {'intro.txt', 'notes_win.txt', 'nested_doc.txt', 'data.md'}

    with tarfile.open(path, 'r:gz') as tar:
        members = tar.getmembers()
        # Ensure flat structure and correct files
        filenames = set()
        for m in members:
            assert m.isfile(), f"Archive contains non-file member: {m.name}"
            # Ensure flat structure (no directory separators)
            assert '/' not in m.name and '\\' not in m.name, f"Archive member is not in a flat structure: {m.name}"
            filenames.add(m.name)

        assert filenames == expected_files, f"Archive contains incorrect files. Expected {expected_files}, got {filenames}."

def test_file_encodings_and_contents():
    path = '/home/user/clean_docs.tar.gz'

    with tarfile.open(path, 'r:gz') as tar:
        # Check intro.txt
        f = tar.extractfile('intro.txt')
        content = f.read()
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            assert False, "intro.txt is not valid UTF-8."
        assert "This is the introduction." in text, "intro.txt content is incorrect."

        # Check notes_win.txt
        f = tar.extractfile('notes_win.txt')
        content = f.read()
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            assert False, "notes_win.txt is not valid UTF-8."
        assert "Café and résumé." in text, "notes_win.txt content is incorrect or not properly converted."

        # Check nested_doc.txt
        f = tar.extractfile('nested_doc.txt')
        content = f.read()
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            assert False, "nested_doc.txt is not valid UTF-8."
        assert "Nested secret document." in text, "nested_doc.txt content is incorrect or not properly converted."

def test_markdown_table_format():
    path = '/home/user/clean_docs.tar.gz'
    with tarfile.open(path, 'r:gz') as tar:
        f = tar.extractfile('data.md')
        content = f.read()
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            assert False, "data.md is not valid UTF-8."

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        assert len(lines) >= 3, "data.md does not have enough lines for a markdown table."

        # Check header
        assert "Item" in lines[0] and "Cost" in lines[0], "data.md table header is incorrect."
        assert lines[0].startswith('|') and lines[0].endswith('|'), "data.md table header is not properly formatted with pipes."

        # Check separator
        assert re.search(r'\|[-:]+\|\s*\|?[-:]+\|', lines[1].replace(' ', '')), "data.md table separator is incorrect."

        # Check rows
        assert "Apple" in lines[2] and "1.00" in lines[2], "data.md table row 1 is incorrect."
        assert "Über" in lines[3] and "2.50" in lines[3], "data.md table row 2 is incorrect or not properly converted to UTF-8."

def test_processing_log():
    path = '/home/user/processing.log'
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "CORRUPT_ARCHIVES:" in content, "Log file missing CORRUPT_ARCHIVES line."
    assert "PROCESSED_FILES:" in content, "Log file missing PROCESSED_FILES line."

    lines = content.splitlines()
    corrupt_line = next((line for line in lines if line.startswith("CORRUPT_ARCHIVES:")), "")
    processed_line = next((line for line in lines if line.startswith("PROCESSED_FILES:")), "")

    assert "corrupt_nested.zip" in corrupt_line, "Log file does not correctly list corrupt_nested.zip as a corrupt archive."

    expected_processed = ["data.md", "intro.txt", "nested_doc.txt", "notes_win.txt"]
    for file in expected_processed:
        assert file in processed_line, f"Log file PROCESSED_FILES missing {file}."

    # Check alphabetical order
    processed_files_str = processed_line.split(":", 1)[1].strip()
    processed_files_list = [x.strip() for x in processed_files_str.split(",")]
    assert processed_files_list == sorted(processed_files_list), "PROCESSED_FILES list is not sorted alphabetically."
    assert processed_files_list == expected_processed, f"PROCESSED_FILES list does not match expected exactly. Expected {expected_processed}, got {processed_files_list}."