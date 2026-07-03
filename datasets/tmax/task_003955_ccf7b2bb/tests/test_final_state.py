# test_final_state.py

import os
import requests
import xml.etree.ElementTree as ET

def test_video_analysis():
    url = "http://127.0.0.1:8080/video-analysis"
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {resp.text}"

    assert "black_frames_count" in data, "Key 'black_frames_count' missing in response"
    assert data["black_frames_count"] == 5, f"Expected 5 black frames, got {data['black_frames_count']}"

def test_storage_scan():
    url = "http://127.0.0.1:8080/storage-scan"
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {resp.text}"

    # Recompute the expected value by walking the directory
    expected = []
    base_dir = "/home/user/storage_dump"

    # Use a set to track visited real paths to avoid symlink loops if we were implementing it,
    # but os.walk does not follow symlinks by default.
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".dat"):
                path = os.path.join(root, f)
                with open(path, "rb") as fp:
                    header = fp.read(4).hex().lower()
                expected.append({"path": path, "header": header})

    expected = sorted(expected, key=lambda x: x["path"])

    assert isinstance(data, list), "Expected response to be a JSON array"

    # The prompt requires the output to be sorted alphabetically by file path
    data_sorted = sorted(data, key=lambda x: x.get("path", ""))

    assert data == data_sorted, "The JSON array is not sorted alphabetically by file path"
    assert data == expected, f"Storage scan results mismatch.\nExpected: {expected}\nGot: {data}"

def test_clean_config():
    url = "http://127.0.0.1:8080/clean-config"
    test_xml = """<backup>
  <target>/mnt/data</target>
  <loop_detected/><loop_detected/>
  <retention>7</retention>
</backup>"""

    try:
        resp = requests.post(url, data=test_xml, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"

    output = resp.text
    assert "<loop_detected" not in output, "The <loop_detected/> tags were not completely removed"
    assert "<target>/mnt/data</target>" in output, "The <target> tag is missing or altered"
    assert "<retention>7</retention>" in output, "The <retention> tag is missing or altered"

    # Ensure the returned text is still valid XML
    try:
        root = ET.fromstring(output)
        assert root.tag == "backup", "Root element should be <backup>"
        assert root.find("target") is not None and root.find("target").text == "/mnt/data"
        assert root.find("retention") is not None and root.find("retention").text == "7"
    except ET.ParseError as e:
        assert False, f"Returned XML is invalid or malformed: {e}\nOutput was:\n{output}"