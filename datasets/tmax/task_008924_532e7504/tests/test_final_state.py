# test_final_state.py
import os
import tarfile

def test_mse_report_content():
    report_path = '/home/user/metrics/mse_report.txt'
    assert os.path.exists(report_path), f"MSE report not found at {report_path}"
    assert os.path.isfile(report_path), f"MSE report path {report_path} is not a file"

    with open(report_path, 'r') as f:
        content = f.read().strip()

    expected_mse = "0.000600"
    assert content == expected_mse, f"Incorrect MSE in report: expected {expected_mse}, got {content}"

def test_archive_exists_and_contents():
    archive_path = '/home/user/archive/experiment_run.tar.gz'
    assert os.path.exists(archive_path), f"Archive not found at {archive_path}"
    assert os.path.isfile(archive_path), f"Archive path {archive_path} is not a file"

    assert tarfile.is_tarfile(archive_path), f"File at {archive_path} is not a valid tar archive"

    with tarfile.open(archive_path, 'r:gz') as tar:
        members = tar.getnames()

    # Check that baseline.bin and experiment.bin are in the archive
    # The prompt asks for "just the files, do not preserve the absolute directory structure"
    # So we expect "baseline.bin" and "experiment.bin" or at least they should be present without absolute paths.

    has_baseline = any(m.endswith('baseline.bin') for m in members)
    has_experiment = any(m.endswith('experiment.bin') for m in members)

    assert has_baseline, "baseline.bin missing from the archive"
    assert has_experiment, "experiment.bin missing from the archive"

    # Check that they don't have absolute paths like /home/user/artifacts/...
    for m in members:
        assert not m.startswith('/'), f"Archive member {m} contains an absolute path"