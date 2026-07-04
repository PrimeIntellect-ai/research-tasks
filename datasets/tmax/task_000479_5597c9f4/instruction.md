You are tasked with creating a configuration migration and tracking tool. We are migrating an older application that uses a mix of configuration formats (JSON, INI, and XML) to a new system that uses a single consolidated YAML configuration. As a configuration manager, you must track these changes by generating checksums and packaging the old and new states together for auditing.

Your objective is to write and execute a Python script at `/home/user/migrate_configs.py` that performs the following steps:

1. **Read Inputs:** Read all configuration files from the directory `/home/user/app_configs/`. You will find three files: `db.json`, `server.ini`, and `metrics.xml`.
2. **Format Conversion:** Parse the contents of these three files and consolidate them into a single Python dictionary. The root keys of this dictionary must be `db`, `server`, and `metrics`, corresponding to the parsed contents of `db.json`, `server.ini`, and `metrics.xml` respectively.
3. **Write YAML:** Write this consolidated dictionary out to a new file at `/home/user/backup/consolidated.yaml`.
4. **Manifest & Checksum Generation:** Calculate the SHA-256 checksum for the three original input files and the newly generated `consolidated.yaml`. Write these to a manifest file at `/home/user/backup/manifest.txt`. Each line in the manifest must follow the format: `<filename> <sha256_hex_digest>` (e.g., `db.json e3b0c442...`). Sort the lines alphabetically by filename.
5. **Archive Creation:** Create a compressed tarball archive at `/home/user/config_backup.tar.gz` that contains both the `app_configs` directory and the `backup` directory (and their contents).

You may need to install external Python packages (like `PyYAML` and `xmltodict`) using `pip` to accomplish this task. Once you have written the script, execute it so that `/home/user/config_backup.tar.gz` is generated.