You are an artifact manager tasked with curating a local binary repository. 

You have been provided with an incoming directory of compressed archives (`/home/user/incoming`), which contain nested binary packages. You also have a configuration file (`/home/user/repo_config.json`) that outlines the curation rules.

Write and execute a Python script that performs the following tasks:

1. **Configuration Parsing:** Read `/home/user/repo_config.json`. It contains the target output directory, allowed architectures, and allowed file extensions.
2. **Nested Archive Extraction:** The `/home/user/incoming` directory contains standard `.zip` files. Inside these `.zip` files are various nested files, including binary archives (e.g., `.tar.gz`, `.zip`) and metadata files.
3. **Filtering:** Identify which of the nested files meet the curation criteria:
   - The file extension must match one of the `allowed_extensions` in the config.
   - The filename must contain one of the `allowed_architectures` as a substring (e.g., `toolX-1.0-x86_64.tar.gz` contains `x86_64`).
4. **Organization:** For each valid nested file, copy it to the target output directory specified in the config, structured in subdirectories by architecture: `<output_dir>/<architecture>/<filename>`.
5. **Manifest Generation:** Calculate the SHA-256 checksum of each valid file. Then, create a JSON manifest file at the path specified by `manifest_path` in the config. The manifest must have the following exact schema:
```json
{
  "artifacts": [
    {
      "filename": "...",
      "architecture": "...",
      "checksum": "<lowercase sha256 hex digest>",
      "path": "<architecture>/<filename>"
    }
  ]
}
```
*Note: The `artifacts` list can be in any order. The `path` should be the relative path from the output directory.*

Do not hardcode paths, architectures, or extensions in your script; read them dynamically from `/home/user/repo_config.json`.

Ensure your script processes all `.zip` files in `/home/user/incoming` and writes the final manifest to the designated location.