You are a deployment engineer tasked with rolling out an automated update mechanism for a backend system. An architect has left a system diagram at `/app/diagram.png` with some configuration parameters. 

Your task is to set up a git repository and an idempotent deployment script based on the architectural diagram.

Perform the following steps:
1. Analyze the image at `/app/diagram.png` to extract the "Log File" path and the "Service Name". You will need these for your script.
2. Initialize a bare Git repository at `/home/user/repo.git`.
3. Create a Python script at `/home/user/deploy.py` that will handle deployments. This script must be executable.
4. Configure a `post-receive` git hook in `/home/user/repo.git` that executes your `/home/user/deploy.py` script. Note that git hooks run in a specific environment, so ensure your script handles paths correctly and uses absolute paths.

Requirements for `/home/user/deploy.py`:
- It must read the standard input provided by the git hook (which comes in the format: `<old-value> <new-value> <ref-name>`).
- It must determine which files were modified between the old commit and the new commit. (If it's the first push, compare against an empty tree).
- If any modified or added file has a `.conf` extension, the script must append the following line to the Log File (extracted from the image):
  `RESTART <Service Name> <new-value>`
- If no `.conf` files were modified, it must append:
  `UPDATE <Service Name> <new-value>`
- **Idempotency**: The script must keep track of processed commits. If the script is triggered multiple times for the same `<new-value>` commit hash, it must NOT write a duplicate entry to the Log File.

Ensure your Python script is robust and functions correctly when called by the git hook. Do not use any external dependencies outside of the standard library for the Python script.