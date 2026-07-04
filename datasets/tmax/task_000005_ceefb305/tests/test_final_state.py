# test_final_state.py
import os
import glob
import struct
import tarfile
import tempfile
import pytest

def get_elf_entry(filepath):
    """Parses the ELF header to find the entry point virtual address."""
    if not os.path.isfile(filepath):
        return None
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        if magic != b'\x7fELF':
            return None

        # Read e_ident to check architecture class and endianness
        f.seek(4)
        e_class_bytes = f.read(1)
        e_data_bytes = f.read(1)
        if not e_class_bytes or not e_data_bytes:
            return None

        e_class = e_class_bytes[0]
        e_data = e_data_bytes[0]

        if e_class != 2:  # Not 64-bit
            return None

        endian = '<' if e_data == 1 else '>'

        # e_entry is at offset 0x18 for 64-bit ELF
        f.seek(0x18)
        entry_bytes = f.read(8)
        if len(entry_bytes) < 8:
            return None

        entry = struct.unpack(endian + 'Q', entry_bytes)[0]
        return hex(entry)

def test_c_source_code_constraints():
    src_path = "/home/user/archiver.c"
    assert os.path.exists(src_path), f"{src_path} is missing."

    with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    # Check for forbidden functions and required headers
    code_no_spaces = code.replace(" ", "")
    assert "system(" not in code_no_spaces, "Forbidden system() call found in C source code."
    assert "<elf.h>" in code, "<elf.h> not included in C source code."
    assert "<iconv.h>" in code, "<iconv.h> not included in C source code."
    assert "<sys/file.h>" in code or "<fcntl.h>" in code, "File locking header (<sys/file.h> or <fcntl.h>) not included in C source code."

def test_archive_index_wal_contents():
    wal_path = "/home/user/archive_index.wal"
    assert os.path.exists(wal_path), f"{wal_path} does not exist."

    try:
        with open(wal_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"{wal_path} is not valid UTF-8.")

    expected_text = "Système de sauvegarde prêt. Résumé des opérations."
    assert expected_text in content, f"Expected UTF-8 converted text not found in {wal_path}."

    # Parse ELF entries from WAL
    found_entries = {}
    for line in content.splitlines():
        if line.strip().startswith("ELF:"):
            parts = line.split("ENTRY:")
            if len(parts) == 2:
                fname = parts[0].replace("ELF:", "").strip()
                addr_str = parts[1].strip()
                try:
                    found_entries[fname] = int(addr_str, 16)
                except ValueError:
                    pass

    # Verify dynamically against actual ELF files in incoming/
    incoming_dir = "/home/user/incoming"
    assert os.path.isdir(incoming_dir), f"{incoming_dir} is missing."

    elf_files_checked = 0
    for filename in os.listdir(incoming_dir):
        filepath = os.path.join(incoming_dir, filename)
        entry_hex = get_elf_entry(filepath)
        if entry_hex is not None:
            elf_files_checked += 1
            expected_entry_int = int(entry_hex, 16)
            assert filename in found_entries, f"Entry for ELF file '{filename}' not found in {wal_path}."
            assert found_entries[filename] == expected_entry_int, f"Incorrect entry point for '{filename}' in {wal_path}. Expected {entry_hex}."

    assert elf_files_checked > 0, "No 64-bit ELF files found in incoming directory to verify."

def test_split_archives():
    backup_dir = "/home/user/backup_parts"
    assert os.path.isdir(backup_dir), f"{backup_dir} is missing."

    parts = sorted(glob.glob(os.path.join(backup_dir, "backup.tar.gz.part*")))
    assert parts, f"No split archive parts found in {backup_dir}."

    # Check part sizes (1MB), except possibly the last one
    for part in parts[:-1]:
        size = os.path.getsize(part)
        assert size == 1024 * 1024, f"Archive part {part} size is {size} bytes, expected exactly 1048576 bytes (1MB)."

    # Reassemble archive
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        for part in parts:
            with open(part, 'rb') as p:
                tmp.write(p.read())
        tmp_name = tmp.name

    try:
        assert tarfile.is_tarfile(tmp_name), "Reassembled file is not a valid tar archive."
        with tarfile.open(tmp_name, 'r:gz') as tar:
            names = tar.getnames()

            # Ensure the required files are present in the archive
            has_wal = any(name.endswith("archive_index.wal") for name in names)
            has_sys_monitor = any(name.endswith("sys_monitor") for name in names)
            has_db_sync = any(name.endswith("db_sync") for name in names)

            assert has_wal, "archive_index.wal not found in the reassembled tarball."
            assert has_sys_monitor, "sys_monitor not found in the reassembled tarball."
            assert has_db_sync, "db_sync not found in the reassembled tarball."
    finally:
        os.remove(tmp_name)