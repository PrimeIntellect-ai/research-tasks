# test_final_state.py

import os
import subprocess
import pytest

def test_vendored_package_run_sh():
    run_sh_path = "/app/smtpd-stub-0.0.1/run.sh"
    assert os.path.isfile(run_sh_path), f"File {run_sh_path} is missing."
    assert os.access(run_sh_path, os.X_OK), f"File {run_sh_path} is not executable."

    # Test with SMTP_PORT set
    env = os.environ.copy()
    env['SMTP_PORT'] = '8888'
    res_custom = subprocess.run([run_sh_path], env=env, capture_output=True, text=True)
    assert '8888' in res_custom.stdout or '8888' in res_custom.stderr, \
        "run.sh did not pass the custom SMTP_PORT (8888) to server.py."

    # Test with SMTP_PORT unset
    if 'SMTP_PORT' in env:
        del env['SMTP_PORT']
    res_default = subprocess.run([run_sh_path], env=env, capture_output=True, text=True)
    assert '2525' in res_default.stdout or '2525' in res_default.stderr, \
        "run.sh did not use the default port 2525 when SMTP_PORT is unset."

def test_email_classifier_adversarial():
    classifier = "/home/user/classify_email"
    assert os.path.isfile(classifier), f"Classifier script {classifier} is missing."
    assert os.access(classifier, os.X_OK), f"Classifier script {classifier} is not executable."

    evil_dir = "/app/emails/evil/"
    clean_dir = "/app/emails/clean/"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for ef in evil_files:
        res = subprocess.run([classifier, ef])
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    clean_modified = []
    for cf in clean_files:
        res = subprocess.run([classifier, cf])
        if res.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_mail_profile_setup():
    profile = "/home/user/mail_profile.sh"
    assert os.path.isfile(profile), f"Profile script {profile} is missing."

    # Test exported variables
    cmd_vars = f"source {profile} && echo $SMTP_PORT && echo $MAIL_CLASSIFIER"
    res_vars = subprocess.run(['bash', '-c', cmd_vars], capture_output=True, text=True)
    assert res_vars.returncode == 0, "Failed to source mail_profile.sh."

    lines = res_vars.stdout.strip().split('\n')
    assert len(lines) >= 2, "Expected output for SMTP_PORT and MAIL_CLASSIFIER."
    assert lines[0] == "8025", f"Expected SMTP_PORT to be 8025, got {lines[0]}."
    assert lines[1] == "/home/user/classify_email", f"Expected MAIL_CLASSIFIER to be /home/user/classify_email, got {lines[1]}."

    # Test start_tunnel function definition
    cmd_func = f"source {profile} && declare -f start_tunnel"
    res_func = subprocess.run(['bash', '-c', cmd_func], capture_output=True, text=True)
    assert res_func.returncode == 0, "Function start_tunnel is not defined in mail_profile.sh."

    func_body = res_func.stdout.replace('\\\n', ' ')
    expected_cmd = "ssh -f -N -L 8025:localhost:25 mailadmin@mail.local -i /home/user/.ssh/mail_rsa"

    # We check if the exact command is present in the function definition
    assert expected_cmd in func_body or expected_cmd.replace("  ", " ") in func_body.replace("  ", " "), \
        "start_tunnel function does not contain the exact expected ssh command."