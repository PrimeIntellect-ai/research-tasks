You are a Release Manager preparing a new deployment for a legacy system. The automated dependency resolver broke due to conflicting peer dependencies, and you need to manually calculate the deployment plan by interpreting an old operational script, comparing it to the current environment, and translating the results into a standardized JSON deployment manifest.

You have been provided with two files in `/home/user/`:
1. `/home/user/current_deps.txt` - A alphabetically sorted list of currently installed packages in the format `pkg_name@version`.
2. `/home/user/legacy_script.ops` - A sequence of legacy commands that build up the desired state of dependencies.

Your task consists of three parts:

**Part 1: Interpret the Legacy Script**
You must act as an interpreter for the `legacy_script.ops` file. The file processes a state of dependencies (initially empty) sequentially from top to bottom. It supports three commands:
* `INSTALL <pkg_name>@<version>`: Adds the package to the desired state. If a package with the same `<pkg_name>` already exists, it updates the version.
* `REMOVE <pkg_name>`: Completely removes the package from the desired state.
* `REPLACE <old_pkg_name> <new_pkg_name>@<version>`: Removes `<old_pkg_name>` and installs `<new_pkg_name>@<version>`.

Evaluate the script to determine the final desired state of packages. Save this desired state as an alphabetically sorted list to `/home/user/desired_deps.txt` (one `pkg_name@version` per line).

**Part 2: Diffing**
Compare the `/home/user/desired_deps.txt` state with the `/home/user/current_deps.txt` state.
* Packages (exact `pkg_name@version` string matches) present in `desired_deps.txt` but missing in `current_deps.txt` are marked for installation.
* Packages (exact `pkg_name@version` string matches) present in `current_deps.txt` but missing in `desired_deps.txt` are marked for uninstallation.

**Part 3: Translation to JSON**
Translate the diff results into a strict JSON file located at `/home/user/deployment_plan.json`. The JSON file must have exactly two keys, `install` and `uninstall`, each containing an alphabetically sorted array of strings representing the packages to be installed and uninstalled.

Example format for `/home/user/deployment_plan.json`:
```json
{
  "install": [
    "foo@2.0.0",
    "qux@1.1.0"
  ],
  "uninstall": [
    "bar@1.0.0",
    "foo@1.5.0"
  ]
}
```

Use whatever language or CLI tools you prefer to automate this process. Ensure the final `desired_deps.txt` and `deployment_plan.json` are created accurately.