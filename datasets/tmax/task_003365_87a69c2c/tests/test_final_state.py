# test_final_state.py

import urllib.request
import urllib.error
import pytest

def test_nginx_waf_accuracy():
    benign_payloads = [
        "image.png",
        "data.txt",
        "backup_2023.tar.gz",
        "report.pdf",
        "user_profile.jpg",
        "archive.zip",
        "log_2023_10_01.txt",
        "script.js",
        "style.css",
        "index.html",
        "app_config.json",
        "database.sqlite",
        "readme.md",
        "setup.py",
        "test_file.bin",
        "document.docx",
        "spreadsheet.xlsx",
        "presentation.pptx",
        "video.mp4",
        "audio.mp3",
        "image_copy.png",
        "data_v2.txt",
        "backup_final.tar.gz",
        "report_draft.pdf",
        "user_avatar.jpg",
        "archive_old.zip",
        "log_yesterday.txt",
        "main.js",
        "theme.css",
        "about.html",
        "settings.json",
        "cache.sqlite",
        "contributing.md",
        "install.sh",
        "blob.bin",
        "notes.docx",
        "finances.xlsx",
        "slides.pptx",
        "movie.mp4",
        "song.mp3",
        "photo.jpeg",
        "info.txt",
        "dump.sql",
        "cert.pem",
        "key.pub",
        "config.yaml",
        "dockerfile",
        "makefile",
        "requirements.txt",
        "tox.ini"
    ]

    malicious_payloads = [
        "../etc/passwd",
        "../../etc/shadow",
        "../../../var/log/messages",
        "....//etc/passwd",
        "..%2fetc/passwd",
        "..%2Fetc/shadow",
        "%2e%2e/var/log",
        "%2E%2E/var/log",
        "%2e%2e%2fetc/passwd",
        "%2E%2E%2Fetc/shadow",
        "foo/../../bar",
        "foo/..%2f..%2fbar",
        "foo/%2e%2e/%2e%2e/bar",
        "foo/%2e%2e%2f%2e%2e%2fbar",
        "../",
        "..%2f",
        "%2e%2e/",
        "%2e%2e%2f",
        "../../",
        "..%2f..%2f",
        "%2e%2e/%2e%2e/",
        "%2e%2e%2f%2e%2e%2f",
        "../../../",
        "..%2f..%2f..%2f",
        "%2e%2e/%2e%2e/%2e%2e/",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2f",
        "a/b/c/../../../d",
        "a/b/c/..%2f..%2f..%2fd",
        "a/b/c/%2e%2e/%2e%2e/%2e%2e/d",
        "a/b/c/%2e%2e%2f%2e%2e%2f%2e%2e%2fd",
        "..../",
        "....%2f",
        "%2e%2e%2e%2e/",
        "%2e%2e%2e%2e%2f",
        "../app.py",
        "..%2fapp.py",
        "%2e%2e/app.py",
        "%2e%2e%2fapp.py",
        "../../nginx.conf",
        "..%2f..%2fnginx.conf",
        "%2e%2e/%2e%2e/nginx.conf",
        "%2e%2e%2f%2e%2e%2fnginx.conf",
        "uploads/../app.py",
        "uploads/..%2fapp.py",
        "uploads/%2e%2e/app.py",
        "uploads/%2e%2e%2fapp.py",
        "../uploads/test.txt",
        "..%2fuploads/test.txt",
        "%2e%2e/uploads/test.txt",
        "%2e%2e%2fuploads/test.txt"
    ]

    true_positives = 0
    true_negatives = 0

    url = "http://localhost:8080/upload"

    for payload in benign_payloads:
        req = urllib.request.Request(url, data=b"testdata", method="POST")
        req.add_header("X-Upload-Filename", payload)
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status in [200, 201]:
                    true_negatives += 1
        except urllib.error.HTTPError as e:
            if e.code in [200, 201]:
                true_negatives += 1
        except Exception:
            pass

    for payload in malicious_payloads:
        req = urllib.request.Request(url, data=b"testdata", method="POST")
        req.add_header("X-Upload-Filename", payload)
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 403:
                    true_positives += 1
        except urllib.error.HTTPError as e:
            if e.code == 403:
                true_positives += 1
        except Exception:
            pass

    total_requests = len(benign_payloads) + len(malicious_payloads)
    accuracy = (true_positives + true_negatives) / total_requests

    assert accuracy >= 0.96, f"WAF accuracy too low: {accuracy:.2f} (Threshold: 0.96). TP: {true_positives}/{len(malicious_payloads)}, TN: {true_negatives}/{len(benign_payloads)}"