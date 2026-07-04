# test_final_state.py

import os
import subprocess

def test_index_html_extracted():
    """Verify that the HTML payload was extracted to /home/user/index.html"""
    html_path = "/home/user/index.html"
    assert os.path.isfile(html_path), f"File {html_path} is missing. You must extract the HTML payload."

    with open(html_path, "r") as f:
        content = f.read()

    assert "trusted-cdn.example.com" in content, "The extracted HTML does not appear to contain the correct payload."
    assert "evil-crypto-miner.hacker.net" in content, "The extracted HTML does not appear to contain the correct payload."

def test_csp_score():
    """Verify that the generated CSP meets the security score threshold."""
    script_path = "/home/user/generate_csp.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Execute the student's script to get the CSP
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute. Error: {result.stderr}"

    csp = result.stdout.strip().lower()
    assert csp, "The script did not output any CSP string."

    # Re-derive the metric score based on the evaluator logic
    score = 100

    if "default-src 'self'" not in csp:
        score -= 20

    if "script-src" in csp:
        if "https://trusted-cdn.example.com" not in csp:
            score -= 30
        script_src_part = csp.split("script-src")[1].split(";")[0]
        if "evil-crypto-miner" in csp or "*" in script_src_part:
            score -= 50
    else:
        score -= 40

    if "img-src" in csp:
        if "https://trusted-images.example.com" not in csp:
            score -= 15
    else:
        score -= 10

    if "style-src" in csp:
        if "https://internal-styles.example.com" not in csp:
            score -= 15
    else:
        score -= 10

    score = max(0, score)

    assert score >= 90, f"CSP Security Score is {score}, which is below the target threshold of 90. Generated CSP: {csp}"