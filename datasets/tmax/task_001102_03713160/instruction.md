You are tasked with helping a configuration manager track and archive specific configuration files that are actively rotating.

There is a directory tree located at `/home/user/configs`. Inside this directory, there are multiple application configuration subdirectories (e.g., `/home/user/configs/app_alpha`, `/home/user/configs/app_beta`, etc.).

Each application directory contains two files:
1. `metadata.json`: A JSON file containing application metadata.
2. `config.xml`: An XML file containing the application's configuration.

Your goal is to write a Python script (or use bash commands) to do the following:
1. Recursively traverse the `/home/user/configs` directory.
2. Parse the `metadata.json` file in each subdirectory. Identify applications where the JSON key `"status"` is set to exactly `"rotating"`.
3. For the applications marked as "rotating", parse their `config.xml` file and extract the integer value from the `<version>` tag.
4. If the `<version>` is strictly greater than `1`, include this XML file in a newly created tarball archive located at `/home/user/rotated_configs.tar.gz`.
5. Inside the tarball archive, the XML files should be placed at the root of the archive and renamed to match the pattern: `<app_name>_v<version>.xml` (where `<app_name>` is the name of the application's directory, e.g., `app_beta_v3.xml`).

Ensure the final archive `/home/user/rotated_configs.tar.gz` is a valid gzipped tarball.