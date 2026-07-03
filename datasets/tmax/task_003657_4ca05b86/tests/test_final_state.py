# test_final_state.py
import os
import re

def test_cwe_findings():
    path = '/home/user/cwe_findings.txt'
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read().upper()

    cwes_found = re.findall(r'CWE-\d+', content)
    assert 'CWE-78' in cwes_found, "CWE-78 (Command Injection) not found in cwe_findings.txt."
    assert 'CWE-79' in cwes_found, "CWE-79 (Cross-Site Scripting) not found in cwe_findings.txt."

def test_pwned_file_does_not_exist():
    path = '/home/user/pwned_file'
    assert not os.path.exists(path), "Command injection was not mitigated; pwned_file exists."

def test_report_html_escaped():
    path = '/home/user/report.html'
    assert os.path.exists(path), f"File {path} is missing. Did you run the script?"

    with open(path, 'r') as f:
        content = f.read()

    assert "&lt;script&gt;" in content, "XSS was not mitigated; <script> tag was not escaped in report.html."
    assert "<script>" not in content, "XSS was not mitigated; raw <script> tag found in report.html."

def test_log_analyzer_fixes():
    path = '/home/user/log_analyzer.py'
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    assert "html.escape" in content, "html.escape is not used in log_analyzer.py."
    assert "timeout=2" in content.replace(" ", ""), "timeout=2 is not used in subprocess.run."

    # Check that shell=True is removed or changed to shell=False
    assert "shell=True" not in content.replace(" ", ""), "shell=True is still present in log_analyzer.py."