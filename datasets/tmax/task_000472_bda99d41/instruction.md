You are assisting a backup operator in testing automated restores securely. The operator needs a workflow that takes extracted backup paths, sanitizes them, and uses a custom mailing list tool to report the restore status.

Your task has two main parts:

1. **Fix the Vendored Mailing Package:**
There is a custom mailing package located at `/app/vendored/mail-sender-v2`. The backup operator tried to use it, but it has a deliberate perturbation: it fails to connect because `mail_sender/connection.py` references a non-existent environment variable `MAIL_PORT_OVERRIDE` instead of the standard `SMTP_PORT`, and the `setup.py` is missing a comma in its `install_requires` list. 
- Fix the package's source code so it can be installed.
- Install it into your local Python environment (`pip install -e /app/vendored/mail-sender-v2`).

2. **Create a Path Classifier / Sanitizer:**
Backup restore paths are extracted from untrusted manifests. You must write a Python classifier to determine if a restore path is safe to generate an `fstab` entry for.
- Create a file at `/home/user/path_checker.py`.
- It must contain a function with the exact signature: `def is_safe_backup_path(path: str) -> bool:`
- A path is ONLY safe (returns `True`) if it strictly meets ALL the following criteria:
    - Starts exactly with `/mnt/backup_restores/`.
    - Does NOT contain directory traversal sequences (`..`).
    - Does NOT contain any whitespace characters (spaces, tabs, newlines, etc.).
    - Does NOT contain shell metacharacters: `&`, `|`, `;`, `$`, `>`, `<`, `` ` ``, `\`, `!`.
    - Is at least 22 characters long (including the base directory).
- Returns `False` for any path that violates these rules (the "evil" paths).

Finally, write an interactive script at `/home/user/generate_restore_report.py` that imports your `path_checker` and the fixed `mail_sender`, though the automated verification will primarily test your `is_safe_backup_path` function against a hidden dataset of valid (clean) and malicious (evil) paths, and verify the vendored package installation.