You are a build engineer responsible for setting up a mock CI/CD pipeline and artifact management system. You need to create a Python script that resolves build dependencies using a custom Directed Acyclic Graph (DAG) data structure, performs "conditional builds" based on the target platform, and a Bash script that acts as the CI trigger.

There is a manifest file located at `/home/user/manifest.json` with the following format:
```json
{
  "artifacts": [
    {"name": "base", "platforms": ["linux", "windows", "mac"], "deps": []},
    {"name": "crypto", "platforms": ["linux", "windows"], "deps": ["base"]},
    {"name": "gui_mac", "platforms": ["mac"], "deps": ["base"]},
    {"name": "gui_x11", "platforms": ["linux"], "deps": ["base"]},
    {"name": "app", "platforms": ["linux", "windows", "mac"], "deps": ["crypto", "gui_mac", "gui_x11", "base"]}
  ]
}
```

**Step 1: The Build Manager (Python)**
Write a Python script at `/home/user/build_manager.py` that takes two arguments: `--manifest` (path to the JSON manifest) and `--platform` (the target platform string).
The script must:
1. Read the manifest.
2. Filter the artifacts: an artifact is only valid if the requested `--platform` is in its `platforms` list.
3. Build a custom DAG data structure and perform a topological sort to determine the build order.
4. "Build" each valid artifact by creating a file at `/home/user/artifacts/<platform>/<artifact_name>.out`. (Create the directories if they don't exist).
5. The content of the `.out` file should strictly follow this format:
   - If the artifact has no valid dependencies for the requested platform: `<artifact_name>`
   - If it has valid dependencies: `<artifact_name>(<dep1_content>,<dep2_content>,...)`
   - **Important:** The valid dependencies inside the parentheses must be sorted alphabetically by the dependency's artifact name. Invalid dependencies (those not supporting the current platform) must be ignored and excluded.

For example, if `app` depends on `base` and `crypto`, and both are valid, the content for `app` might be: `app(base,crypto(base))`.

**Step 2: The CI Pipeline (Bash)**
Write a Bash script at `/home/user/run_ci.sh` that takes a single argument: a commit message string.
The script must:
1. Parse the commit message for CI tags in the format `[ci:<platform>]`. A message can have multiple tags (e.g., `"Update docs [ci:linux] [ci:windows]"`).
2. For each platform tag found, execute the Python script: `python3 /home/user/build_manager.py --manifest /home/user/manifest.json --platform <platform>`

Constraints:
- Use Python 3.
- Do not use external libraries for the DAG or topological sort; implement the custom data structure yourself.
- Ensure files and directories are created with standard permissions.

When you are done, ensure both scripts are fully functional and correctly handle the logic described.