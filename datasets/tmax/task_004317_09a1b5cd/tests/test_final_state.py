# test_final_state.py

import os
import tarfile

def test_trigger_log_content():
    """Verify that the trigger log exists and contains the correct trigger file path."""
    log_path = '/home/user/trigger.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_path = '/home/user/workdir/subdir/trigger.txt'
    assert content == expected_path, f"Expected {log_path} to contain '{expected_path}', but got '{content}'."

def test_archive_exists_and_valid():
    """Verify that the snapshot archive exists and is a valid tar.gz file."""
    archive_path = '/home/user/snapshot.tar.gz'
    assert os.path.exists(archive_path), f"{archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

def test_archive_contents():
    """Verify that the snapshot archive contains the correct files and contents."""
    archive_path = '/home/user/snapshot.tar.gz'

    # We will extract it in memory and check contents
    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()

        # Look for initial.txt and subdir/trigger.txt
        # The paths might have a leading './' or 'workdir/' depending on how the student archived it,
        # but the requirements say "relative to the watched directory", so 'subdir/trigger.txt' and 'initial.txt'

        initial_member = None
        trigger_member = None

        for name in names:
            if name.endswith('initial.txt'):
                initial_member = name
            if name.endswith('trigger.txt'):
                trigger_member = name

        assert initial_member is not None, "initial.txt not found in the archive."
        assert trigger_member is not None, "trigger.txt not found in the archive."

        # Check content of initial.txt
        f_init = tar.extractfile(initial_member)
        assert f_init is not None, f"Could not extract {initial_member}"
        init_content = f_init.read().decode('utf-8').strip()
        assert init_content == "INIT", f"Expected initial.txt to contain 'INIT', got '{init_content}'"

        # Check content of trigger.txt
        f_trig = tar.extractfile(trigger_member)
        assert f_trig is not None, f"Could not extract {trigger_member}"
        trig_content = f_trig.read().decode('utf-8').strip()
        assert trig_content == "BACKUP_ME", f"Expected trigger.txt to contain 'BACKUP_ME', got '{trig_content}'"

def test_go_source_code():
    """Verify that the Go source code exists and uses required packages."""
    main_go_path = '/home/user/archiver/main.go'
    assert os.path.exists(main_go_path), f"{main_go_path} does not exist."

    with open(main_go_path, 'r') as f:
        content = f.read()

    assert 'fsnotify' in content, "The Go program must use the 'fsnotify' package."
    assert 'archive/tar' in content, "The Go program must use the 'archive/tar' package."
    assert 'compress/gzip' in content, "The Go program must use the 'compress/gzip' package."