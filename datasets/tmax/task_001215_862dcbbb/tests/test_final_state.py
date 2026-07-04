# test_final_state.py
import os
import hashlib

def rle_encode(s):
    if not s:
        return ""
    encoded = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            encoded.append(f"{count}{s[i-1]}")
            count = 1
    encoded.append(f"{count}{s[-1]}")
    return "".join(encoded)

def test_drafts_modified():
    drafts_dir = '/home/user/docs_system/drafts'

    expected_docA = "Title: Doc A\nStatus: Draft\nContents containing [REDACTED] data.\nMore text here.\n"
    expected_docB = "Title: Doc B\nStatus: Review\nThis one has no secrets.\n"
    expected_docC = "Title: Doc C\nStatus: Draft\nAnother [REDACTED] mission.\n[REDACTED] is everywhere.\n"

    with open(os.path.join(drafts_dir, 'docA.md'), 'r') as f:
        assert f.read() == expected_docA, "docA.md was not correctly modified."

    with open(os.path.join(drafts_dir, 'docB.md'), 'r') as f:
        assert f.read() == expected_docB, "docB.md should not have been modified."

    with open(os.path.join(drafts_dir, 'docC.md'), 'r') as f:
        assert f.read() == expected_docC, "docC.md was not correctly modified."

def test_merged_drafts():
    merged_path = '/home/user/docs_system/merged_drafts.md'
    assert os.path.isfile(merged_path), "merged_drafts.md does not exist."

    expected_docA = "Title: Doc A\nStatus: Draft\nContents containing [REDACTED] data.\nMore text here.\n"
    expected_docC = "Title: Doc C\nStatus: Draft\nAnother [REDACTED] mission.\n[REDACTED] is everywhere.\n"
    expected_merged = expected_docA + expected_docC

    with open(merged_path, 'r') as f:
        assert f.read() == expected_merged, "merged_drafts.md does not contain the correct concatenated content."

def test_cpp_program_exists():
    assert os.path.isfile('/home/user/docs_system/processor.cpp'), "processor.cpp does not exist."
    assert os.path.isfile('/home/user/docs_system/processor'), "Compiled processor executable does not exist."
    assert os.access('/home/user/docs_system/processor', os.X_OK), "Compiled processor is not executable."

def test_chunks_and_rle():
    chunks_dir = '/home/user/docs_system/chunks'
    assert os.path.isdir(chunks_dir), "chunks/ directory does not exist."

    expected_texts = [
        "Chapter 1\nHellooo\n",
        "Chapter 2\nSpacesss   !\n",
        "Chapter 3\nAABBCC\n"
    ]

    for i, text in enumerate(expected_texts, 1):
        chunk_path = os.path.join(chunks_dir, f'chunk_{i}.rle')
        assert os.path.isfile(chunk_path), f"chunk_{i}.rle does not exist."

        expected_rle = rle_encode(text)
        with open(chunk_path, 'r') as f:
            assert f.read() == expected_rle, f"chunk_{i}.rle does not have the correct RLE encoded content."

def test_manifest():
    manifest_path = '/home/user/docs_system/manifest.txt'
    assert os.path.isfile(manifest_path), "manifest.txt does not exist."

    chunks_dir = '/home/user/docs_system/chunks'
    expected_lines = []

    for i in range(1, 4):
        chunk_filename = f'chunk_{i}.rle'
        chunk_path = os.path.join(chunks_dir, chunk_filename)
        if os.path.isfile(chunk_path):
            with open(chunk_path, 'rb') as f:
                sha1 = hashlib.sha1(f.read()).hexdigest()
            expected_lines.append(f"{sha1}  {chunk_filename}")

    expected_lines.sort()

    with open(manifest_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "manifest.txt does not match the expected sorted sha1sums."