# test_final_state.py
import os
import struct
import zlib
import pytest

def test_archive_and_log():
    archive_path = "/home/user/archive.mybak"
    log_path = "/home/user/filter.log"
    corpus_dir = "/app/corpus"
    clean_dir = os.path.join(corpus_dir, "clean")
    evil_dir = os.path.join(corpus_dir, "evil")

    assert os.path.isfile(archive_path), f"Archive file missing at {archive_path}"
    assert os.path.isfile(log_path), f"Log file missing at {log_path}"

    # Read log file
    with open(log_path, "r") as f:
        log_lines = [line.strip() for line in f if line.strip()]

    log_dict = {}
    for line in log_lines:
        parts = line.split(",")
        if len(parts) >= 2:
            log_dict[parts[0]] = parts[1]

    # Parse archive
    archive_files = {}
    with open(archive_path, "rb") as f:
        header = f.read(8)
        assert header == b"MYBAK_v1", f"Invalid archive global header: {header}"

        while True:
            len_bytes = f.read(2)
            if not len_bytes:
                break

            assert len(len_bytes) == 2, "Unexpected EOF while reading path length"
            path_len = struct.unpack("<H", len_bytes)[0]

            rel_path_bytes = f.read(path_len)
            assert len(rel_path_bytes) == path_len, "Unexpected EOF while reading path"
            rel_path = rel_path_bytes.decode("utf-8")

            size_bytes = f.read(4)
            assert len(size_bytes) == 4, "Unexpected EOF while reading file size"
            file_size = struct.unpack("<I", size_bytes)[0]

            compressed_content = f.read(file_size)
            assert len(compressed_content) == file_size, "Unexpected EOF while reading compressed content"

            try:
                decompressed_content = zlib.decompress(compressed_content)
            except zlib.error as e:
                pytest.fail(f"Failed to decompress content for {rel_path}: {e}")

            archive_files[rel_path] = decompressed_content

    # Evaluate against corpora
    clean_files = []
    for root, _, files in os.walk(clean_dir):
        for file in files:
            clean_files.append(os.path.relpath(os.path.join(root, file), corpus_dir))

    evil_files = []
    for root, _, files in os.walk(evil_dir):
        for file in files:
            evil_files.append(os.path.relpath(os.path.join(root, file), corpus_dir))

    # Check evil bypassed
    evil_bypassed = []
    for evil in evil_files:
        if log_dict.get(evil) != "REJECTED":
            evil_bypassed.append(evil)
        elif evil in archive_files:
            evil_bypassed.append(evil)

    # Check clean modified/rejected
    clean_failed = []
    for clean in clean_files:
        if log_dict.get(clean) != "ACCEPTED":
            clean_failed.append(clean)
        elif clean not in archive_files:
            clean_failed.append(clean)
        else:
            # Verify content matches
            orig_path = os.path.join(corpus_dir, clean)
            with open(orig_path, "rb") as f:
                orig_content = f.read()
            if archive_files[clean] != orig_content:
                clean_failed.append(clean)

    if evil_bypassed or clean_failed:
        msg = []
        if evil_bypassed:
            msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(os.path.basename(f) for f in evil_bypassed)}")
        if clean_failed:
            msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(os.path.basename(f) for f in clean_failed)}")
        pytest.fail("; ".join(msg))