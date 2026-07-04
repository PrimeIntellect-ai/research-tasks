# test_final_state.py
import os
import tarfile
import pytest

def test_terminology_replaced():
    arch_path = "/home/user/docs/module_a/architecture.md"
    assert os.path.exists(arch_path), f"File {arch_path} is missing."
    with open(arch_path, "r") as f:
        content = f.read()
    assert "primary" in content, "Term 'master' was not replaced with 'primary' in architecture.md."
    assert "replica" in content, "Term 'slave' was not replaced with 'replica' in architecture.md."
    assert "master" not in content, "Old term 'master' is still present in architecture.md."
    assert "slave" not in content, "Old term 'slave' is still present in architecture.md."

    sec_path = "/home/user/docs/module_b/security.md"
    assert os.path.exists(sec_path), f"File {sec_path} is missing."
    with open(sec_path, "r") as f:
        content = f.read()
    assert "denylist" in content, "Term 'blacklist' was not replaced with 'denylist' in security.md."
    assert "allowlist" in content, "Term 'whitelist' was not replaced with 'allowlist' in security.md."
    assert "blacklist" not in content, "Old term 'blacklist' is still present in security.md."
    assert "whitelist" not in content, "Old term 'whitelist' is still present in security.md."

def test_tarball_contents():
    tarball_path = "/home/user/backups/diff_backup.tar.gz"
    assert os.path.exists(tarball_path), f"Tarball {tarball_path} is missing."

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            members = tar.getmembers()
    except tarfile.ReadError:
        pytest.fail(f"File {tarball_path} is not a valid gzip-compressed tarball.")

    actual_files = set()
    for m in members:
        if m.isfile():
            # Normalize path (e.g., remove leading './')
            m_norm = m.name.lstrip("./")
            actual_files.add(m_norm)

    expected_files = {
        "module_a/architecture.md",
        "module_b/security.md",
        "new_guide.md"
    }

    missing_files = expected_files - actual_files
    assert not missing_files, f"Tarball is missing expected files: {missing_files}"

    assert "module_a/networking.md" not in actual_files, "Tarball incorrectly contains unchanged file 'networking.md'."

    extra_files = actual_files - expected_files
    assert not extra_files, f"Tarball contains unexpected files: {extra_files}"

def test_backup_summary():
    summary_path = "/home/user/backups/backup_summary.txt"
    assert os.path.exists(summary_path), f"Summary file {summary_path} is missing."

    with open(summary_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "module_a/architecture.md",
        "module_b/security.md",
        "new_guide.md"
    ]

    assert sorted(lines) == sorted(expected_lines), f"Summary file contents are incorrect. Expected {expected_lines}, but found {lines}"