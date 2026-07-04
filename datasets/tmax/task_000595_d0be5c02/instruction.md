You are tasked with writing a simulated Kubernetes Operator script in Python that manages manifest files, handles backups, and strictly adheres to system timezone and configuration requirements.

The environment is structured under `/home/user/k8s-operator/`.
There are four directories:
- `/home/user/k8s-operator/incoming/`: Contains new Kubernetes YAML manifests submitted for deployment.
- `/home/user/k8s-operator/active/`: Contains the currently "running" (active) manifests.
- `/home/user/k8s-operator/backups/`: Destination for backup archives.
- `/home/user/k8s-operator/config/`: Contains the operator configuration.

The configuration file is located at `/home/user/k8s-operator/config/operator.ini` and contains:
```ini
[settings]
timezone = Asia/Tokyo
backup_format = tar.gz
```

Your objective is to write a Python script at `/home/user/k8s-operator/operator.py` that performs the following steps when executed:

1. **Read Configuration**: Parse `/home/user/k8s-operator/config/operator.ini` to get the target timezone and backup format.
2. **Calculate Timestamp**: Determine the current time in the configured timezone (`Asia/Tokyo`).
3. **Backup Strategy**: 
   - Create a backup of the *current* contents of `/home/user/k8s-operator/active/` before making any changes.
   - The backup must be saved in `/home/user/k8s-operator/backups/` as `backup_YYYYMMDD_HHMMSS.tar.gz` (where the timestamp is in the `Asia/Tokyo` timezone).
   - The archive should contain the files directly (not a nested `active/` directory).
4. **Manifest Processing**:
   - For every `.yaml` file in `/home/user/k8s-operator/incoming/`, read its contents.
   - Inject an annotation under `metadata.annotations` (create the `annotations` block if it doesn't exist).
   - The annotation must be `operator.k8s.io/processed-at: "YYYY-MM-DD HH:MM:SS Z"` (e.g., `2023-10-25 14:30:00 +0900`, using the `Asia/Tokyo` timezone).
   - Write the modified YAML file to `/home/user/k8s-operator/active/`, overwriting any file with the same name.
5. **Cleanup & Logging**:
   - Delete all files from `/home/user/k8s-operator/incoming/` after successful processing.
   - Append a line to `/home/user/k8s-operator/operator.log` with the exact format: `[YYYY-MM-DD HH:MM:SS Z] SUCCESS: Backed up to <backup_filename> and processed <N> manifests.` (Using the same timezone).

Note: You must rely on standard Python 3 libraries (e.g., `configparser`, `datetime`, `zoneinfo`, `tarfile`, `yaml` or basic string manipulation if `yaml` isn't installed). Assume `pyyaml` is installed if you wish to use it, but since you are only adding a simple annotation, basic text processing is also acceptable.

Run your script to complete the process.