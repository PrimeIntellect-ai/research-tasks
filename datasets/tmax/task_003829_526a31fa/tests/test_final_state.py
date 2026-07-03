# test_final_state.py

import os

def test_symlink_removed():
    symlink_path = '/home/user/data/subdir/loop'
    assert not os.path.exists(symlink_path) and not os.path.islink(symlink_path), (
        f"The recursive symlink {symlink_path} still exists. It should be removed."
    )

    # Also verify there are no other symlinks pointing to an ancestor in /home/user/data
    for root, dirs, files in os.walk('/home/user/data'):
        for d in dirs:
            p = os.path.join(root, d)
            if os.path.islink(p):
                target = os.path.realpath(p)
                assert not os.path.realpath(root).startswith(target), (
                    f"Found another recursive symlink at {p} pointing to {target}"
                )

def test_rust_program_exists():
    rust_file = '/home/user/parse_backup.rs'
    assert os.path.isfile(rust_file), f"The Rust program {rust_file} is missing."

def test_report_content():
    report_file = '/home/user/report.txt'
    assert os.path.isfile(report_file), f"The report file {report_file} is missing."

    with open(report_file, 'r') as f:
        content = f.read().strip()

    expected_path = '/home/user/data/subdir/loop'
    assert content == expected_path, (
        f"The content of {report_file} is incorrect. "
        f"Expected '{expected_path}', got '{content}'."
    )