You are helping a developer migrate a legacy codebase from Python 2 to Python 3. As part of the testing phase, you need to write a Bash test harness that evaluates dependency constraints and identifies syntax incompatibilities.

Your task is to create a Bash script at `/home/user/check_migration.sh` that performs two main tasks and writes the results to `/home/user/migration_report.txt`.

**Part 1: Dependency Version Constraint Satisfaction**
You will be provided with two files:
1. `/home/user/deps.current` contains the currently installed packages and their versions in the format `package=x.y.z`.
2. `/home/user/deps.required` contains the minimum required versions for Python 3 compatibility in the format `package>=x.y.z`.

Your script must read both files and compare the semantic versions. For every package listed in `deps.required`:
- If the package is present in `deps.current` but its version is strictly less than the required version, it needs an upgrade.
- If the package is completely missing from `deps.current`, it needs to be installed (treat it as needing an upgrade to the required version).
- If the installed version is greater than or equal to the required version, no action is needed.

*Note: You must use Bash (e.g., `sort -V` or custom logic) to properly compare semantic versions. Do not use Python for the version comparison.*

**Part 2: Syntax Compatibility Testing**
There is a directory of Python scripts located at `/home/user/src`. 
Your script must recursively find all `.py` files in this directory and attempt to compile them using Python 3 to check for syntax errors. You can do this by running `python3 -m py_compile <file>`.
Keep track of any file that fails to compile (returns a non-zero exit code).

**Output Format**
Your script must generate a report at `/home/user/migration_report.txt` exactly matching this structure:

```
UPGRADES:
<package1> <required_version>
<package2> <required_version>
...

FAILURES:
<failed_script1.py>
<failed_script2.py>
...
```

**Constraints and Rules:**
- The list of packages under `UPGRADES:` must be sorted alphabetically by package name.
- The list of scripts under `FAILURES:` must contain **only the base filename** (e.g., `legacy.py`, not the full path), and must be sorted alphabetically.
- Ensure the script is executable (`chmod +x /home/user/check_migration.sh`).
- You can assume `python3` is available on the system.
- Run your script once before finishing the task to ensure `/home/user/migration_report.txt` is populated correctly.