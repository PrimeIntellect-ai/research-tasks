# test_final_state.py

import os
import json
import urllib.request
import urllib.parse
import urllib.error
import pytest

def test_cracked_password():
    cracked_path = "/home/user/cracked_password.txt"
    assert os.path.exists(cracked_path), f"{cracked_path} is missing."
    with open(cracked_path, "r") as f:
        password = f.read().strip()
    assert password == "password", "The cracked password is incorrect."

def test_auth_config_updated():
    config_path = "/app/auth_config.json"
    assert os.path.exists(config_path), f"{config_path} is missing."
    with open(config_path, "r") as f:
        data = json.load(f)

    assert "admin_hash" in data, "admin_hash key missing in auth_config.json"
    admin_hash = data["admin_hash"]

    # Check if it's a bcrypt hash
    assert admin_hash.startswith("$2") and len(admin_hash) == 60, "admin_hash does not appear to be a valid bcrypt hash."
    assert admin_hash != "5f4dcc3b5aa765d61d8327deb882cf99", "admin_hash was not updated from the original MD5 hash."

def test_validator_direct_corpus():
    clean_corpus = "/app/corpus/clean/safe.txt"
    evil_corpus = "/app/corpus/evil/payloads.txt"

    with open(clean_corpus, "r") as f:
        clean_payloads = [line.strip() for line in f if line.strip()]

    with open(evil_corpus, "r") as f:
        evil_payloads = [line.strip() for line in f if line.strip()]

    clean_failures = []
    for payload in clean_payloads:
        url = f"http://127.0.0.1:8080/validate?next={urllib.parse.quote(payload)}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    clean_failures.append(payload)
        except urllib.error.HTTPError as e:
            if e.code != 200:
                clean_failures.append(payload)
        except Exception:
            clean_failures.append(payload)

    evil_failures = []
    for payload in evil_payloads:
        url = f"http://127.0.0.1:8080/validate?next={urllib.parse.quote(payload)}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.status != 403:
                    evil_failures.append(payload)
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_failures.append(payload)
        except Exception:
            evil_failures.append(payload)

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_payloads)} evil bypassed direct validator: {evil_failures}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_payloads)} clean modified/rejected by direct validator: {clean_failures}")

    assert not error_msgs, " | ".join(error_msgs)

def test_nginx_integration_corpus():
    clean_corpus = "/app/corpus/clean/safe.txt"
    evil_corpus = "/app/corpus/evil/payloads.txt"

    with open(clean_corpus, "r") as f:
        clean_payloads = [line.strip() for line in f if line.strip()]

    with open(evil_corpus, "r") as f:
        evil_payloads = [line.strip() for line in f if line.strip()]

    clean_failures = []
    for payload in clean_payloads:
        url = f"http://127.0.0.1:8000/login?next={urllib.parse.quote(payload)}"
        try:
            # We don't want urllib to automatically follow redirects since Flask returns a 302
            class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            opener = urllib.request.build_opener(NoRedirectHandler)
            req = urllib.request.Request(url)
            response = opener.open(req)
            if response.status not in (200, 302):
                clean_failures.append(payload)
        except urllib.error.HTTPError as e:
            if e.code not in (200, 302):
                clean_failures.append(payload)
        except Exception:
            clean_failures.append(payload)

    evil_failures = []
    for payload in evil_payloads:
        url = f"http://127.0.0.1:8000/login?next={urllib.parse.quote(payload)}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.status != 403:
                    evil_failures.append(payload)
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_failures.append(payload)
        except Exception:
            evil_failures.append(payload)

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_payloads)} evil bypassed NGINX integration: {evil_failures}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_payloads)} clean modified/rejected by NGINX integration: {clean_failures}")

    assert not error_msgs, " | ".join(error_msgs)