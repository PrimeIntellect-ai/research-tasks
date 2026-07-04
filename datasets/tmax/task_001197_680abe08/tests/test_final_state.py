# test_final_state.py

import os
import io
import time
import ftplib
import subprocess
import requests
import pytest

def test_sync_script_exists_and_executable():
    path = "/home/user/sync.sh"
    assert os.path.isfile(path), f"{path} does not exist or is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_crontab_configured():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."
    assert "sync.sh" in result.stdout, "sync.sh is not scheduled in the user's crontab."

def test_end_to_end_pipeline():
    # 1. Upload a test CSV with embedded newlines via FTP
    ftp = ftplib.FTP()
    try:
        ftp.connect('127.0.0.1', 2121)
        ftp.login('ftpuser', 'ftppass')
    except Exception as e:
        pytest.fail(f"Failed to connect and login to FTP server: {e}")

    csv_content = (
        "TransactionID,Category,Amount,Notes\n"
        "9001,TestCat_Zeta,500,\"Multi-line\nNote 1\"\n"
        "9002,TestCat_Zeta,200,\"Single line note\"\n"
        "9003,TestCat_Omega,800,\"Multi-line\nNote\n2\"\n"
        "9004,TestCat_Omega,200,\"Normal\"\n"
        "9005,TestCat_Alpha,1000,\"Another\nnewline\"\n"
    )

    bio = io.BytesIO(csv_content.encode('utf-8'))
    try:
        ftp.storbinary('STOR /data/test_verification_pytest.csv', bio)
    except Exception as e:
        pytest.fail(f"Failed to upload file via FTP: {e}")
    finally:
        ftp.quit()

    # 2. Wait up to 70 seconds for the cron job to sync the file
    synced_file = "/home/user/local_data/test_verification_pytest.csv"
    synced = False
    for _ in range(70):
        if os.path.exists(synced_file):
            synced = True
            break
        time.sleep(1)

    assert synced, f"Cron job did not sync the new file to {synced_file} within 70 seconds."

    # 3. Request metrics via Nginx reverse proxy
    try:
        resp = requests.get("http://localhost:8080/api/metrics", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {resp.text}")

    assert isinstance(data, list), "Expected JSON response to be an array of objects."

    # 4. Verify aggregation and embedded newline parsing
    alpha_total = next((item.get('total') for item in data if item.get('category') == 'TestCat_Alpha'), None)
    omega_total = next((item.get('total') for item in data if item.get('category') == 'TestCat_Omega'), None)
    zeta_total  = next((item.get('total') for item in data if item.get('category') == 'TestCat_Zeta'), None)

    assert alpha_total == 1000, f"Expected TestCat_Alpha total to be 1000, got {alpha_total}. Embedded newlines might be breaking the CSV parser."
    assert omega_total == 1000, f"Expected TestCat_Omega total to be 1000, got {omega_total}."
    assert zeta_total == 700, f"Expected TestCat_Zeta total to be 700, got {zeta_total}."

    # 5. Verify sorting (descending by total, then alphabetically by category)
    for i in range(len(data) - 1):
        c1 = data[i]
        c2 = data[i+1]
        t1 = c1.get('total', 0)
        t2 = c2.get('total', 0)
        cat1 = c1.get('category', '')
        cat2 = c2.get('category', '')

        if t1 < t2:
            pytest.fail(f"Results not sorted descending by total: {c1} came before {c2}")
        elif t1 == t2:
            if cat1 > cat2:
                pytest.fail(f"Results with same total not sorted alphabetically by category: {c1} came before {c2}")