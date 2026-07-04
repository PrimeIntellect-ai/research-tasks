# test_final_state.py
import pytest
import requests

BASE_URL = "http://localhost:8080"
HEADERS = {"Authorization": "Bearer loc_token_99"}

def test_missing_auth():
    """Test that missing authorization header returns 401."""
    try:
        response = requests.get(f"{BASE_URL}/locales?lang=fr", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing Auth header, got {response.status_code}"

def test_invalid_auth():
    """Test that invalid authorization header returns 401."""
    try:
        response = requests.get(f"{BASE_URL}/locales?lang=fr", headers={"Authorization": "Bearer wrong_token"}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid Auth header, got {response.status_code}"

def test_locales_fr():
    """Test /locales endpoint for French translations."""
    try:
        response = requests.get(f"{BASE_URL}/locales?lang=fr", headers=HEADERS, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    expected = {
        "ui_welcome": "Bienvenue",
        "ui_logout": "Se déconnecter",
        "ui_dashboard": "Tableau de bord",
        "ui_settings": "Paramètres"
    }

    for key, val in expected.items():
        assert data.get(key) == val, f"Expected key '{key}' to be '{val}', but got '{data.get(key)}'"

def test_locales_es():
    """Test /locales endpoint for Spanish translations (checks overwrite and trim)."""
    try:
        response = requests.get(f"{BASE_URL}/locales?lang=es", headers=HEADERS, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    expected = {
        "ui_welcome": "Bienvenido",
        "ui_logout": "Cerrar sesión"
    }

    for key, val in expected.items():
        assert data.get(key) == val, f"Expected key '{key}' to be '{val}', but got '{data.get(key)}'"

def test_subtitle_scene_1():
    """Test /subtitle endpoint for scene 1 (0-4.5s)."""
    try:
        response = requests.get(f"{BASE_URL}/subtitle?lang=fr&time=2.0", headers=HEADERS, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert data.get("key") == "ui_welcome", f"Expected key 'ui_welcome', got {data.get('key')}"
    assert data.get("text") == "Bienvenue", f"Expected text 'Bienvenue', got {data.get('text')}"

def test_subtitle_scene_3_fallback():
    """Test /subtitle endpoint for scene 3 (9.2s-14.0s) with English fallback."""
    try:
        response = requests.get(f"{BASE_URL}/subtitle?lang=es&time=11.0", headers=HEADERS, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert data.get("key") == "ui_settings", f"Expected key 'ui_settings', got {data.get('key')}"
    assert data.get("text") == "Settings", f"Expected text 'Settings', got {data.get('text')}"

def test_subtitle_scene_4_fallback():
    """Test /subtitle endpoint for scene 4 (14.0s+) with English fallback."""
    try:
        response = requests.get(f"{BASE_URL}/subtitle?lang=de&time=15.0", headers=HEADERS, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert data.get("key") == "ui_logout", f"Expected key 'ui_logout', got {data.get('key')}"
    assert data.get("text") == "Log out", f"Expected text 'Log out', got {data.get('text')}"