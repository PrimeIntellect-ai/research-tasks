# test_final_state.py

import os
import re
import configparser
import subprocess
import time
import glob
import signal
import pytest
import urllib.request
import urllib.error

def test_nginx_conf_fixed():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"File {nginx_conf_path} is missing."

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://unix:/home/user/app/app.sock;" in content, "nginx.conf does not contain the corrected socket path 'app.sock'."
    assert "app_wrong.sock" not in content, "nginx.conf still contains the intentional typo 'app_wrong.sock'."

def test_supervisord_conf_valid():
    sup_conf_path = "/home/user/supervisord.conf"
    assert os.path.isfile(sup_conf_path), f"File {sup_conf_path} is missing."

    config = configparser.ConfigParser()
    try:
        config.read(sup_conf_path)
    except Exception as e:
        pytest.fail(f"Could not parse {sup_conf_path} as an ini file: {e}")

    # Check for programs
    programs = [sec for sec in config.sections() if sec.startswith("program:")]
    assert len(programs) >= 2, f"Expected at least 2 programs in supervisord.conf, found {len(programs)}."

    has_app = False
    has_nginx = False

    for prog in programs:
        cmd = config.get(prog, "command", fallback="")
        autostart = config.getboolean(prog, "autostart", fallback=False)
        autorestart = config.getboolean(prog, "autorestart", fallback=False)

        if "app.py" in cmd:
            has_app = True
            assert autostart, f"Program {prog} (app) does not have autostart=true"
            assert autorestart, f"Program {prog} (app) does not have autorestart=true"
        if "nginx" in cmd:
            has_nginx = True
            assert autostart, f"Program {prog} (nginx) does not have autostart=true"
            assert autorestart, f"Program {prog} (nginx) does not have autorestart=true"
            assert "daemon off" in cmd or "daemon off;" in cmd, f"Program {prog} (nginx) must run in foreground (e.g., daemon off;)"

    assert has_app, "supervisord.conf is missing the python app."
    assert has_nginx, "supervisord.conf is missing nginx."

def test_monitor_script_exists():
    monitor_path = "/home/user/monitor.py"
    assert os.path.isfile(monitor_path), f"File {monitor_path} is missing."

def test_monitor_script_behavior():
    # We will test the monitor script by mocking a local server or using the real one.
    # The requirement is to run the supervisor and monitor, kill the app, and see if alert is generated.

    # Clean up alerts dir
    alerts_dir = "/home/user/alerts"
    os.makedirs(alerts_dir, exist_ok=True)
    for f in glob.glob(os.path.join(alerts_dir, "alert_*.eml")):
        os.remove(f)

    sup_conf_path = "/home/user/supervisord.conf"
    monitor_path = "/home/user/monitor.py"

    # Start supervisord
    sup_proc = subprocess.Popen(["supervisord", "-c", sup_conf_path, "-n"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # wait for processes to start

    # Start monitor
    mon_proc = subprocess.Popen(["python3", monitor_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)

    try:
        # Check that web server is up and returns 200
        try:
            req = urllib.request.urlopen("http://127.0.0.1:8080/")
            assert req.getcode() == 200
        except Exception as e:
            pytest.fail(f"Failed to reach web server via nginx: {e}")

        # Kill the python app process
        subprocess.run(["pkill", "-f", "app.py"])

        # Wait for monitor to detect 502 and write alert
        time.sleep(4)

        # Check alerts
        alerts = glob.glob(os.path.join(alerts_dir, "alert_*.eml"))
        assert len(alerts) > 0, "No alert file was generated in /home/user/alerts/"

        # Read the most recent alert
        latest_alert = max(alerts, key=os.path.getctime)
        with open(latest_alert, "r") as f:
            content = f.read()

        assert "To: admin@local.dev" in content, "Missing To: header in alert."
        assert "From: monitor@local.dev" in content, "Missing From: header in alert."
        assert "Subject: Alert - HTTP 502" in content, "Missing or incorrect Subject in alert."
        assert "The web server returned HTTP status 502." in content, "Missing or incorrect body in alert."

    finally:
        # Cleanup processes
        if mon_proc:
            mon_proc.terminate()
            mon_proc.wait(timeout=2)
        if sup_proc:
            sup_proc.terminate()
            sup_proc.wait(timeout=2)
        subprocess.run(["pkill", "-f", "nginx"])
        subprocess.run(["pkill", "-f", "app.py"])