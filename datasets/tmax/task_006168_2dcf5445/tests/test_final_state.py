# test_final_state.py

import os
import json
import configparser

def test_config_corrected_and_directory_created():
    config_path = '/home/user/config/app_services.ini'
    assert os.path.exists(config_path), f"Configuration file {config_path} is missing."

    config = configparser.ConfigParser()
    config.read(config_path)

    assert 'service_gamma' in config, "Section [service_gamma] is missing in the config."
    expected_dir = '/home/user/logs/service_gamma'
    actual_dir = config['service_gamma'].get('log_dir', '').strip()

    assert actual_dir == expected_dir, f"Expected service_gamma log_dir to be {expected_dir}, but got {actual_dir}."
    assert os.path.isdir(expected_dir), f"The directory {expected_dir} was not created."

def test_capacity_report_json():
    report_path = '/home/user/capacity_report.json'
    assert os.path.exists(report_path), f"The report file {report_path} was not created."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert 'active_port' in report, "The 'active_port' key is missing from the report."
    assert report['active_port'] == 9002, f"Expected active_port to be 9002, but got {report['active_port']}."

    assert 'storage_usage_bytes' in report, "The 'storage_usage_bytes' key is missing from the report."
    usage = report['storage_usage_bytes']

    assert usage.get('service_alpha') == 2548, f"Expected service_alpha usage to be 2548, got {usage.get('service_alpha')}."
    assert usage.get('service_beta') == 4096, f"Expected service_beta usage to be 4096, got {usage.get('service_beta')}."
    assert usage.get('service_gamma') == 0, f"Expected service_gamma usage to be 0, got {usage.get('service_gamma')}."

def test_log_rotation_effects():
    # service_alpha
    alpha_access_log = '/home/user/logs/service_alpha/access.log'
    alpha_access_archive = '/home/user/logs/service_alpha/access.log.archive'
    alpha_error_log = '/home/user/logs/service_alpha/error.log'
    alpha_error_archive = '/home/user/logs/service_alpha/error.log.archive'

    assert os.path.exists(alpha_access_archive), f"Archive file {alpha_access_archive} was not created."
    assert os.path.getsize(alpha_access_archive) == 2048, "The access.log.archive file should be 2048 bytes."
    assert os.path.exists(alpha_access_log), f"The new empty file {alpha_access_log} was not created."
    assert os.path.getsize(alpha_access_log) == 0, f"The new {alpha_access_log} file should be 0 bytes."

    assert not os.path.exists(alpha_error_archive), f"The file {alpha_error_archive} should not exist (size was <= 1024)."
    assert os.path.exists(alpha_error_log), f"The file {alpha_error_log} should still exist."
    assert os.path.getsize(alpha_error_log) == 500, f"The file {alpha_error_log} should remain 500 bytes."

    # service_beta
    beta_worker_log = '/home/user/logs/service_beta/worker.log'
    beta_worker_archive = '/home/user/logs/service_beta/worker.log.archive'

    assert os.path.exists(beta_worker_archive), f"Archive file {beta_worker_archive} was not created."
    assert os.path.getsize(beta_worker_archive) == 4096, "The worker.log.archive file should be 4096 bytes."
    assert os.path.exists(beta_worker_log), f"The new empty file {beta_worker_log} was not created."
    assert os.path.getsize(beta_worker_log) == 0, f"The new {beta_worker_log} file should be 0 bytes."