# test_final_state.py
import os
import glob

def test_operator_script_exists():
    assert os.path.exists("/home/user/operator.py"), "The operator script /home/user/operator.py is missing."
    assert os.path.isfile("/home/user/operator.py"), "/home/user/operator.py is not a file."

def test_manifest_modified_correctly():
    manifest_path = '/home/user/k8s_manifests/app.yaml'
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} not found."

    with open(manifest_path, 'rb') as f:
        content = f.read()

    assert content.endswith(b"\n  # modified\n"), "Manifest was not modified correctly with '\\n  # modified\\n'."

def test_backups_and_emails_exist_and_match():
    backups_dir = '/home/user/k8s_backups'
    mail_dir = '/home/user/mail_spool'

    assert os.path.isdir(backups_dir), f"Directory {backups_dir} not found."
    assert os.path.isdir(mail_dir), f"Directory {mail_dir} not found."

    backups = glob.glob(os.path.join(backups_dir, 'app.yaml.*.bak'))
    assert len(backups) == 2, f"Expected exactly 2 backup files in {backups_dir}, found {len(backups)}."

    emails = glob.glob(os.path.join(mail_dir, 'app.yaml.*.eml'))
    assert len(emails) == 2, f"Expected exactly 2 email files in {mail_dir}, found {len(emails)}."

    for backup in backups:
        # Extract hash from filename app.yaml.<hash>.bak
        filename = os.path.basename(backup)
        parts = filename.split('.')
        assert len(parts) >= 4, f"Backup filename {filename} does not match expected format."
        hash_val = parts[-2]

        eml_file = os.path.join(mail_dir, f'app.yaml.{hash_val}.eml')
        assert os.path.exists(eml_file), f"Missing corresponding email file for hash {hash_val}."

        with open(eml_file, 'r') as f:
            eml_content = f.read()

        expected_eml = f"To: admin@local\nSubject: Manifest Backup: app.yaml\nHash: {hash_val}"
        assert expected_eml.strip() in eml_content.strip(), f"Email content incorrect in {eml_file}."