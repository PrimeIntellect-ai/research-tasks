# test_final_state.py

import os
import requests
import pytest

def test_files_moved_and_renamed():
    nginx_conf = "/app/nginx/nginx.conf"
    app_py = "/app/api/app.py"

    assert os.path.isfile(nginx_conf), f"File {nginx_conf} is missing. Did you move and rename it correctly?"
    assert os.path.isfile(app_py), f"File {app_py} is missing. Did you move and rename it correctly?"

def test_nginx_conf_content():
    nginx_conf = "/app/nginx/nginx.conf"
    if not os.path.isfile(nginx_conf):
        pytest.fail(f"Cannot test content because {nginx_conf} is missing.")

    with open(nginx_conf, 'r') as f:
        content = f.read()

    assert "127.0.0.1:5000" in content, "The upstream address in nginx.conf was not updated to 127.0.0.1:5000."
    assert "backend.example.com:80" not in content, "The old upstream address backend.example.com:80 is still in nginx.conf."

def test_app_py_content():
    app_py = "/app/api/app.py"
    if not os.path.isfile(app_py):
        pytest.fail(f"Cannot test content because {app_py} is missing.")

    with open(app_py, 'r') as f:
        content = f.read()

    assert "DB_HOST = \"127.0.0.1\"" in content, "The DB_HOST in app.py was not updated to 127.0.0.1."
    assert "redis.prod.internal" not in content, "The old DB_HOST redis.prod.internal is still in app.py."
    assert "ENV = \"development\"" in content, "The ENV in app.py was not updated to development."
    assert "production" not in content, "The old ENV production is still in app.py."

def test_health_endpoint():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}. Are Nginx and Flask running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = {"status": "ok", "env": "development", "redis_ping": True}
    assert data == expected_data, f"Expected JSON response {expected_data}, but got {data}"