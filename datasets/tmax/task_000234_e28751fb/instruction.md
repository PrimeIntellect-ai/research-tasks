You are tasked with building an automated configuration backup processing tool for a legacy fleet of servers. The system currently dumps all configuration changes into a single, massive, multi-line log file. Your job is to parse this file, extract the configurations, generate a checksum manifest, and package them for cold storage.

The input file is located at `/home/user/fleet_audit.log`. 

The log file contains multi-line configuration records. Each record begins with a header line exactly in this format:
`@@@ CONFIG_START | HOST: <hostname> | TIME: <epoch_timestamp> @@@`
This is followed by the actual configuration lines.
The record ends with exactly this line:
`@@@ CONFIG_END @@@`

Any lines outside of these blocks (e.g., general system logs, warnings) should be completely ignored.

Perform the following operations, primarily using a Python script:
1. **Parse & Extract**: Read `/home/user/fleet_audit.log`. For every valid configuration block, extract the configuration lines (excluding the START and END markers) and save them to a file at `/home/user/configs/<hostname>/<epoch_timestamp>.conf`. You must create the necessary subdirectories.
2. **Generate Manifest**: Create a JSON manifest file at `/home/user/configs/manifest.json`. The JSON should be a single dictionary where the keys are the relative paths of the config files (e.g., `db_server_01/1672531200.conf`) and the values are their SHA-256 checksums (as hex strings).
3. **Archive**: Create a gzipped tarball of the entire `/home/user/configs/` directory at `/home/user/configs_backup.tar.gz`. When extracted, the root directory in the archive must be `configs/`.
4. **Chunking**: The cold storage system requires files to be split into small chunks. Split `/home/user/configs_backup.tar.gz` into exactly 1024-byte (1KB) chunks. Save these chunks in the directory `/home/user/cold_storage/` with the prefix `backup.part_` and a two-letter alphabetical suffix (e.g., `backup.part_aa`, `backup.part_ab`, etc.). 

Ensure you create `/home/user/cold_storage/` before splitting. Only the final output files (the `configs` directory tree, the tarball, and the `cold_storage` directory) will be evaluated.