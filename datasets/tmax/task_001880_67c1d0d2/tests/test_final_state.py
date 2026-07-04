# test_final_state.py

import os
import glob

def test_notes_are_utf8():
    notes_dir = "/home/user/backups/notes"
    assert os.path.isdir(notes_dir), f"Directory {notes_dir} is missing."

    txt_files = glob.glob(os.path.join(notes_dir, "*.txt"))
    assert len(txt_files) > 0, "No .txt files found in notes directory."

    for txt_file in txt_files:
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError:
            pytest.fail(f"File {txt_file} is not valid UTF-8.")

def test_backup_report_content():
    report_path = "/home/user/backup_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    # Derive expected corrupted archives
    archives_dir = "/home/user/backups/archives"
    corrupted_archives = []
    if os.path.isdir(archives_dir):
        for f in glob.glob(os.path.join(archives_dir, "*.tar.gz")):
            # Use os.system to check tar integrity
            if os.system(f"tar -tzf {f} > /dev/null 2>&1") != 0:
                corrupted_archives.append(f)
    corrupted_archives.sort()

    # Derive expected failed jobs
    log_path = "/home/user/backups/logs/job_history.log"
    failed_jobs = []
    if os.path.isfile(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            records = content.split("---")
            for record in records:
                if "Status: FAILED" in record:
                    for line in record.strip().split("\n"):
                        if line.startswith("Job ID:"):
                            failed_jobs.append(line.split(":")[1].strip())
    failed_jobs.sort()

    # Derive expected ELF files
    data_dir = "/home/user/backups/data"
    elf_files = []
    if os.path.isdir(data_dir):
        for root, _, files in os.walk(data_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        header = f.read(4)
                        if header == b"\x7fELF":
                            elf_files.append(file_path)
                except Exception:
                    pass
    elf_files.sort()

    # Derive expected converted notes count
    notes_dir = "/home/user/backups/notes"
    notes_count = 0
    if os.path.isdir(notes_dir):
        notes_count = len(glob.glob(os.path.join(notes_dir, "*.txt")))

    # Build expected report
    expected_lines = []
    expected_lines.append("[Corrupted Archives]")
    expected_lines.extend(corrupted_archives)
    expected_lines.append("")
    expected_lines.append("[Failed Jobs]")
    expected_lines.extend(failed_jobs)
    expected_lines.append("")
    expected_lines.append("[ELF Files]")
    expected_lines.extend(elf_files)
    expected_lines.append("")
    expected_lines.append("[Converted Notes]")
    expected_lines.append(f"Total converted: {notes_count}")

    expected_content = "\n".join(expected_lines).strip()

    with open(report_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Report content does not match expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}"
    )