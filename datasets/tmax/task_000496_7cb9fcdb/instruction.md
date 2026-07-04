You are a backup operator automating a restore testing pipeline. Our automated deployment nodes have an SSH configuration that is currently rejecting key-based logins, forcing us to use interactive password-based authentication for our specialized restore utility.

We have provided a vendored source package for our restore utility located at `/app/py-restore-util-1.2.0`. 

Your objectives are:
1. **Fix the Vendored Package:** The package has a bug preventing it from building/running properly. Identify the configuration error in its build files or source, correct it, and install it locally using `pip install --user /app/py-restore-util-1.2.0`.
2. **Automate Interactive Restore:** Create a Python script at `/home/user/auto_restore.py` that takes a single command-line argument representing a backup ID (an alphanumeric string). 
3. **Execution Logic:** Your script must invoke the newly installed CLI command `restore-util extract <BACKUP_ID>`. Because of the key-rejection issue, `restore-util` will always interactively prompt for a password with the exact string: `Archive Password: `. Your script must detect this prompt and send the static password `OperatorDeploy99!` followed by a newline.
4. **Output Parsing:** Capture the standard output of `restore-util`. It will emit a list of files. Your script must parse this and print to `stdout` a strict JSON object with a single key `"restored_files"` containing a sorted list of the file paths extracted. Do not print any other text.

Ensure your Python script is robust, cleanly handles the interactive prompt (you may use standard libraries or `pexpect`), and produces only the requested JSON output.