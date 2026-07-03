# test_final_state.py

import os
import csv
import json
import pytest

CSV_PATH = "/home/user/legacy_topology.csv"
SCRIPT_PATH = "/home/user/deploy_migration.sh"
SERVICES_DIR = "/home/user/services"
CONFIGS_DIR = "/home/user/system_configs"
REPORT_PATH = "/home/user/migration_report.json"

def get_csv_data():
    if not os.path.exists(CSV_PATH):
        pytest.fail(f"CSV file {CSV_PATH} is missing.")

    services = []
    with open(CSV_PATH, "r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            services.append(row)
    return services

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Deployment script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Deployment script {SCRIPT_PATH} is not executable."

def test_directories_created():
    services = get_csv_data()

    assert os.path.exists(SERVICES_DIR), f"Services directory {SERVICES_DIR} does not exist."
    assert os.path.isdir(SERVICES_DIR), f"{SERVICES_DIR} is not a directory."

    assert os.path.exists(CONFIGS_DIR), f"System configs directory {CONFIGS_DIR} does not exist."
    assert os.path.isdir(CONFIGS_DIR), f"{CONFIGS_DIR} is not a directory."

    for svc in services:
        svc_dir = os.path.join(SERVICES_DIR, svc["ServiceName"])
        assert os.path.exists(svc_dir), f"Service directory {svc_dir} does not exist."
        assert os.path.isdir(svc_dir), f"{svc_dir} is not a directory."

def test_profile_files_content():
    services = get_csv_data()

    for svc in services:
        profile_path = os.path.join(SERVICES_DIR, svc["ServiceName"], ".app_profile")
        assert os.path.exists(profile_path), f"Profile file {profile_path} does not exist."

        expected_content = (
            f'export APP_ENV="cloud_migration"\n'
            f'export CLOUD_DB_HOST="{svc["CloudDBHost"]}"\n'
            f'export APP_PORT="{svc["NewPort"]}"\n'
            f'export MIGRATION_STATUS="ACTIVE"'
        )

        with open(profile_path, "r") as f:
            content = f.read().strip()

        assert content == expected_content, f"Content of {profile_path} does not match expected."

def test_config_files_content():
    services = get_csv_data()

    for svc in services:
        config_path = os.path.join(CONFIGS_DIR, f'{svc["ServiceName"]}_proxy.conf')
        assert os.path.exists(config_path), f"Config file {config_path} does not exist."

        expected_content = (
            f'[ProxyConfig]\n'
            f'ListenPort={svc["NewPort"]}\n'
            f'Upstream={svc["LegacyIP"]}:{svc["LegacyPort"]}\n'
            f'RequireGroup={svc["TargetGroup"]}'
        )

        with open(config_path, "r") as f:
            content = f.read().strip()

        assert content == expected_content, f"Content of {config_path} does not match expected."

def test_json_report_content():
    services = get_csv_data()

    assert os.path.exists(REPORT_PATH), f"JSON report {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert "migrated_services" in report_data, f"'migrated_services' key missing in {REPORT_PATH}."
    assert "total_services" in report_data, f"'total_services' key missing in {REPORT_PATH}."

    assert report_data["total_services"] == len(services), "Total services count in JSON does not match CSV."

    expected_migrated = []
    for svc in services:
        expected_migrated.append({
            "name": svc["ServiceName"],
            "port": int(svc["NewPort"]),
            "profile_path": f"/home/user/services/{svc['ServiceName']}/.app_profile"
        })

    expected_migrated.sort(key=lambda x: x["name"])

    assert report_data["migrated_services"] == expected_migrated, "Migrated services list in JSON does not match expected structure and sorting."