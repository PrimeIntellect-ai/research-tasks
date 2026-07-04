You are a build engineer managing web security artifacts for a legacy Node.js project. The project is currently failing its build pipeline due to a conflicting peer dependency, and security scans indicate vulnerable dependencies are being pulled in. 

The project uses a proprietary, custom lockfile format located at `/home/user/project/secure-lock.txt` and a standard `/home/user/project/package.json`.

Your objective is to build a vulnerability scanner pipeline in Bash, interface with a legacy C security database, parse the lockfile to find the vulnerable web components, and finally resolve the dependency conflict.

**Step 1: FFI Security Database Compilation**
A legacy C library source file is located at `/home/user/ffi/sec_check.c`. It contains a function `int check_vulnerability(const char* pkg, const char* version);` which returns `1` if the package is vulnerable to web exploits (like XSS or CSRF), and `0` otherwise.
1. Compile this C file into a shared library `libseccheck.so` in `/home/user/ffi/`.
2. Write a minimal bridge/wrapper (in C, Python with ctypes, or any standard Linux tool) so that your Bash script can query this shared library.

**Step 2: Lockfile Parser & State Machine (Bash)**
Write a Bash script at `/home/user/audit.sh` that implements a state machine to parse `/home/user/project/secure-lock.txt`.
The lockfile has a custom block-based format:
```
BEGIN [BlockType]
  pkgName version
  pkgName version
END [BlockType]
```
Your Bash script must:
1. Parse the file line-by-line.
2. Only process packages inside `BEGIN [Web-Components]` and `END [Web-Components]` blocks. Ignore packages inside `[Dev-Tools]` or `[System]` blocks.
3. For each package in the `[Web-Components]` block, use your FFI bridge to call `check_vulnerability` from `libseccheck.so`.
4. Output the vulnerable packages to `/home/user/vuln.log` in the exact format: `<pkgName>@<version>` (one per line, sorted alphabetically).

**Step 3: Resolve Artifact Conflicts**
The project's `/home/user/project/package.json` specifies a web framework that has a peer dependency conflict forcing the inclusion of the vulnerable packages. 
1. Identify the peer dependency conflict in `package.json`.
2. Modify the file to resolve the conflict by bumping the framework versions to their nearest secure, compatible releases (assume `express-router` version `4.5.0` is the secure standard).
3. Save the fixed file to `/home/user/project/resolved_package.json`.

Ensure `/home/user/audit.sh` is executable. You may run it to verify your `vuln.log`.