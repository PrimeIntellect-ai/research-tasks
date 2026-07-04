You are a FinOps analyst responsible for optimizing cloud storage costs. Unnecessary debug logs are consuming massive amounts of premium cloud storage, but we must strictly preserve compliance data and logs for certain exempt projects.

Your task is to build a log classifier and configure log rotation.

Step 1: Extract Exemption Data
There is a screenshot of a billing alert at `/app/billing_rules.png`. Use OCR (tesseract is preinstalled) to read this image. It contains the name of a specific exempt project in the format `EXEMPT_PROJECT: <PROJECT_NAME>`.

Step 2: Create the Log Classifier
Write a Bash script at `/home/user/log_filter.sh` that takes a single file path as its first argument. 
This script will be used as a pre-flight check before our automated deletion system removes files.
The script must classify the file by returning a specific exit code:
- Exit code `0` means **KEEP** the file.
- Exit code `1` means **DELETE** the file.

Classification Rules:
1. By default, **KEEP** all files.
2. **DELETE** the file IF it has a `.log` extension AND its contents include the exact string `[DEBUG]`.
3. OVERRIDE: **KEEP** the file, regardless of other rules, IF its contents include the exact string `[ERROR]`.
4. OVERRIDE: **KEEP** the file, regardless of other rules, IF its contents include the exact `EXEMPT_PROJECT: <PROJECT_NAME>` string you extracted from the image.

Step 3: Log Rotation Configuration
Create a valid logrotate configuration file at `/home/user/logrotate.conf` that applies to all `.log` files in `/home/user/logs/`. The configuration must:
- Rotate logs daily.
- Keep 7 rotated versions.
- Compress the rotated files.
- Missing log files should be ignored without throwing an error.

Ensure your `log_filter.sh` script is executable. Our automated verification system will run your script against two large corpora of mock log files: a "clean" corpus (files that must be kept) and an "evil" corpus (files that must be deleted).