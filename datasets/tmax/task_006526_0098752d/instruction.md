You are a platform engineer maintaining a custom CI/CD pipeline. Our dependency resolution step is currently failing because we need a standalone tool to resolve semantic versions based on minimum version constraints.

Please perform the following steps:

1. **Write a Go program** at `/home/user/resolve.go`.
   - The program must accept a single command-line argument: a URL (e.g., `http://ci.local/resolve?pkg=worker&min_version=v1.0.0`).
   - It should parse this URL to extract the `pkg` and `min_version` query parameters.
   - It must read a JSON file at `/home/user/catalog.json` (which contains a mapping of package names to arrays of available version strings, e.g., `{"worker": ["v0.9.0", "v1.0.0", "v1.5.0", "v2.0.0"]}`).
   - It must find and print to standard output the **highest available version** for the requested `pkg` that satisfies these constraints:
     - The version must be greater than or equal to `min_version` according to semantic versioning.
     - The version must have the **same major version** as `min_version`.
   - If no version satisfies the constraint, it should print `none`.
   - *Hint:* You may initialize a Go module in `/home/user` and use `golang.org/x/mod/semver` to assist with semantic version parsing and comparison.

2. **Cross-compile the program** into two standalone binaries:
   - `/home/user/resolve_linux_amd64` (for Linux amd64)
   - `/home/user/resolve_windows_amd64.exe` (for Windows amd64)

3. **Create a database schema migration file** at `/home/user/migration.sql`.
   - Write standard SQL to add two new columns to an existing table named `deployments`:
     - `resolved_version` (type VARCHAR(50))
     - `target_os` (type VARCHAR(50))

Make sure all files are created exactly at the specified paths. Do not include any extra text in the output of the Go program besides the resolved version string.