You are tasked with creating a Python-based configuration management script that acts as a simple Kubernetes backup operator. The script will manage backup states idempotently and simulate an email alert system for configuration changes.

First, ensure the following directory structure exists (create it if it doesn't):
- `/home/user/k8s_manifests`
- `/home/user/k8s_backups`
- `/home/user/mail_spool`

Create an initial Kubernetes manifest file at `/home/user/k8s_manifests/app.yaml` with the following content:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
```

Next, write a Python script at `/home/user/operator.py`. When executed, this script must do the following:
1. Iterate over all `.yaml` files in `/home/user/k8s_manifests/`.
2. For each file, calculate its SHA-256 hash.
3. Check if a backup for this exact version already exists in `/home/user/k8s_backups/`. The expected backup filename format is `<original_filename>.<sha256_hash>.bak` (e.g., `app.yaml.a1b2c...def.bak`).
4. If the backup does *not* exist, perform these two actions (if it does exist, skip and do nothing):
    a. Copy the current manifest file to the backup location with the formatted name.
    b. Create an email notification file in `/home/user/mail_spool/` named `<original_filename>.<sha256_hash>.eml`. The contents of this file must be exactly:
```
To: admin@local
Subject: Manifest Backup: <original_filename>
Hash: <sha256_hash>
```

After you have written `/home/user/operator.py`, perform the following steps to demonstrate its idempotency and functionality:
1. Run the script once. (This should back up the initial `app.yaml`).
2. Run the script a second time. (This should be completely idempotent and create no new files).
3. Append exactly the string `\n  # modified\n` to the end of `/home/user/k8s_manifests/app.yaml`.
4. Run the script a third time. (This should detect the change and create a new backup and a new email spool file).

Ensure you leave the system with all scripts, backups, and spool files in place so they can be verified.