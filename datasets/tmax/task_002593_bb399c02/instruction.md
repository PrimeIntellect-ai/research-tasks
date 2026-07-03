You are a container specialist tasked with configuring a local deployment registry and microservice process supervisor. You must complete the following multi-stage setup on this system. You do not have root access. All your work must be done within `/home/user/`.

**Stage 1: Fix and Install Process Supervisor**
We use a lightweight, third-party process supervisor called `tinysupervisor`. The source code has been provided in the container at `/app/tinysupervisor-1.0`. 
However, the maintainer made a typo in the `Makefile` in the most recent release, which causes the installation to fail when specifying a custom installation directory. 
1. Identify and fix the typographical error in `/app/tinysupervisor-1.0/Makefile` that prevents correct resolution of the installation path variable.
2. Build and install the package into `/home/user/local/` (such that the executable ends up at `/home/user/local/bin/tinysupervisor`).

**Stage 2: Configure Git Deployment Server**
1. Initialize a bare Git repository at `/home/user/deploy.git`.
2. Configure the repository to accept pushes to the `main` branch.

**Stage 3: Write a Manifest Validator**
You must write a strict configuration validator in Bash. This script will eventually be used by our Git hooks to validate incoming microservice manifests.
Create a Bash script at `/home/user/validate_manifest.sh` that reads standard input line-by-line. 

Each line of input represents a microservice configuration formatted strictly as comma-separated values:
`service_name,replicas,port,image`

For each line, your script must validate the fields against the following strict rules:
*   `service_name`: Must exactly match the regex `^svc-[a-z0-9]{1,10}$` (starts with `svc-`, followed by 1 to 10 lowercase alphanumeric characters).
*   `replicas`: Must be a single non-zero digit (`1` through `9`).
*   `port`: Must be a 4-digit integer from `8000` to `8099`.
*   `image`: Must exactly match the pattern `registry.local/` followed by 1 to 20 lowercase alphanumeric characters, followed by `:v` and a single digit (e.g., `registry.local/backend:v2`).
*   The line must contain exactly 4 comma-separated fields.

**Output Formatting:**
*   If a line is completely valid, print exactly: `[VALID] <service_name>:<port>`
*   If a line violates ANY rule (or has the wrong number of fields), print exactly: `[INVALID] <exact_raw_line_content>`

Your script must be pure Bash (using standard built-ins or standard coreutils like `grep`/`sed`/`awk`). Make sure the script is executable (`chmod +x`). 

**Stage 4: Integration**
Symlink your validator script to the Git repository's pre-receive hook:
Link `/home/user/validate_manifest.sh` to `/home/user/deploy.git/hooks/pre-receive`. (Do not worry about the standard `pre-receive` stdin format for this exercise; the test suite will evaluate the script directly).