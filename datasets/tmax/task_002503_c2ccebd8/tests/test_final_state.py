# test_final_state.py
import os
import glob

def test_processed_data_files():
    processed_dir = '/home/user/processed_data'
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    processed_files = glob.glob(os.path.join(processed_dir, 'EXP-*.txt'))
    assert len(processed_files) == 100, f"Expected exactly 100 processed files, found {len(processed_files)}."

    for i in range(1, 101):
        expected_file = os.path.join(processed_dir, f"EXP-{i:05d}.txt")
        assert os.path.exists(expected_file), f"Expected processed file {expected_file} is missing."

def test_status_directories():
    by_status_dir = '/home/user/by_status'
    assert os.path.isdir(by_status_dir), f"Directory {by_status_dir} does not exist."

    status_dirs = os.listdir(by_status_dir)
    assert set(status_dirs) == {'SUCCESS', 'FAILED'}, f"Expected exactly SUCCESS and FAILED directories, found: {status_dirs}"

def test_symlinks_and_content():
    success_links = glob.glob('/home/user/by_status/SUCCESS/EXP-*.txt')
    failed_links = glob.glob('/home/user/by_status/FAILED/EXP-*.txt')

    assert len(success_links) + len(failed_links) == 100, f"Total symlinks should be 100, found {len(success_links) + len(failed_links)}."

    for link in success_links + failed_links:
        assert os.path.islink(link), f"Expected {link} to be a symbolic link."

        target = os.readlink(link)
        assert target.startswith('/home/user/processed_data/'), f"Symlink {link} does not point to an absolute path in /home/user/processed_data/. Target: {target}"

        assert os.path.exists(link), f"Symlink {link} is broken."

        with open(link, 'r') as f:
            content = f.read()

        assert "=== RUN START ===" in content, f"File {link} missing RUN START marker."
        assert "=== RUN END ===" in content, f"File {link} missing RUN END marker."

        if "SUCCESS" in link:
            assert "Status: SUCCESS\n" in content, f"File {link} should contain 'Status: SUCCESS'."
            assert "Status: OK\n" not in content, f"File {link} still contains unnormalized 'Status: OK'."
        elif "FAILED" in link:
            assert "Status: FAILED\n" in content, f"File {link} should contain 'Status: FAILED'."
            assert "Status: ERROR" not in content, f"File {link} still contains unnormalized 'ERROR' status."