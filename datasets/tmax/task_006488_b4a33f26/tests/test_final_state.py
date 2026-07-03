# test_final_state.py
import os
import pytest

def test_restored_system_log():
    filepath = '/home/user/restored/system_log.txt'
    assert os.path.exists(filepath), f"Expected restored file {filepath} does not exist."

    expected_content = 'INFO: System booted successfully.\n' * 5
    with open(filepath, 'r') as f:
        content = f.read()
    assert content == expected_content, f"Content of {filepath} is incorrect."

def test_restored_cpu_metrics():
    filepath = '/home/user/restored/cpu_metrics.csv'
    assert os.path.exists(filepath), f"Expected restored file {filepath} does not exist."

    expected_content = 'cpu0,100\ncpu1,98\ncpu2,100\n'
    with open(filepath, 'r') as f:
        content = f.read()
    assert content == expected_content, f"Content of {filepath} is incorrect."

def test_symlink_job_8081():
    linkpath = '/home/user/restored/job_8081.link'
    assert os.path.islink(linkpath), f"Expected symlink {linkpath} does not exist or is not a symlink."

    target = os.readlink(linkpath)
    expected_targets = ['system_log.txt', '/home/user/restored/system_log.txt']
    assert target in expected_targets, f"Symlink {linkpath} points to {target}, expected one of {expected_targets}."

def test_symlink_job_8083():
    linkpath = '/home/user/restored/job_8083.link'
    assert os.path.islink(linkpath), f"Expected symlink {linkpath} does not exist or is not a symlink."

    target = os.readlink(linkpath)
    expected_targets = ['cpu_metrics.csv', '/home/user/restored/cpu_metrics.csv']
    assert target in expected_targets, f"Symlink {linkpath} points to {target}, expected one of {expected_targets}."

def test_failed_job_not_restored():
    filepath = '/home/user/restored/do_not_restore.txt'
    assert not os.path.exists(filepath), f"File {filepath} should not have been restored as its job status was FAILED."

def test_c_program_exists():
    filepath = '/home/user/restore.c'
    assert os.path.exists(filepath), f"C program {filepath} does not exist."