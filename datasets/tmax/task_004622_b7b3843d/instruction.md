You are tasked with implementing the ingestion pipeline for a secure configuration manager. This manager tracks state changes across our fleet by processing custom-compressed configuration updates, filtering out malicious or invalid updates, and converting the approved ones into standard YAML format for downstream deployment.

Our proprietary configuration compression library, `lzconfig`, is provided as a vendored package at `/app/vendored/lzconfig_v1.0.0`. Unfortunately, the latest archive was corrupted by a bad commit before it was vendored, and it currently fails to decompress data due to a missing standard library import in its core module.

Your objectives:
1. **Fix and Install the Vendored Package**: Inspect `/app/vendored/lzconfig_v1.0.0`, identify the trivial missing import bug causing `NameError`s during decompression, fix it, and install the package in your Python environment.
2. **Implement the Filter**: Create a Python script at `/home/user/config_filter.py` with the following CLI signature:
   `python3 /home/user/config_filter.py <input_file.lzc>`
   The script must use the `lzconfig` library to decompress the binary `.lzc` file into a Python dictionary.
3. **Validation Rules**: The script must analyze the decompressed dictionary and REJECT the configuration (exit with status code `1`) if ANY of the following "evil" conditions are met:
   - Any key in the configuration starts with `_internal_`.
   - The key `role` exists and its value is anything other than `"user"`.
   - Any key ending with `_dir` or `_path` contains an absolute path (starts with `/`) or a path traversal (contains `../`).
4. **Format Conversion & Approval**: If the configuration is perfectly CLEAN, the script must:
   - Convert the configuration dictionary into standard YAML format.
   - Save the YAML file to `/home/user/approved_configs/` using the original base filename but with a `.yaml` extension (e.g., processing `update_1.lzc` should produce `/home/user/approved_configs/update_1.yaml`).
   - Exit with status code `0`.

To help you develop and test your script, we have provided two corpora of compressed configuration files:
- `/app/corpus/clean/`: Contains strictly valid configuration updates.
- `/app/corpus/evil/`: Contains configurations with various malicious payloads or unauthorized modifications violating the rules above.

Your script must correctly accept 100% of the clean corpus (saving the converted YAMLs and exiting 0) and reject 100% of the evil corpus (exiting 1 without saving a YAML file).