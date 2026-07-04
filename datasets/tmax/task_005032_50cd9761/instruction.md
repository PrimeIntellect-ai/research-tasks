As a backup administrator, you are tasked with replacing a legacy proprietary backup tool that creates differential archives using hardlinks based on complex configuration files. The legacy tool is available as a stripped binary at `/app/legacy_archiver`.

Your objective is to write a standalone Bash script at `/home/user/archiver.sh` that exactly replicates the data parsing and backup archiving logic of the legacy tool.

The legacy tool parses a configuration file (which specifies backup targets, exclude patterns, and link dest paths) and takes an input data directory. It then outputs a deterministic list of file actions (hard links, copies, skips) to standard output. 

Requirements for your script:
1. It must accept two arguments: `<config_file>` and `<data_directory>`.
2. It must parse the configuration file to determine which files to back up and which to exclude.
3. It must simulate a differential backup by printing the exact sequence of actions it would take to standard output, matching the formatting of `/app/legacy_archiver`.
4. You may test your script against the provided `/app/legacy_archiver` to reverse-engineer its configuration parsing rules and output format.
5. Your script must handle arbitrary combinations of files, symbolic links, and nested directories within the input.

Output format (must match the legacy binary exactly):
ACTION PATH -> DESTINATION

Example:
LINK /data/app.log -> /backup/inc/app.log
COPY /data/new.txt -> /backup/inc/new.txt
SKIP /data/temp.tmp

Write your final Bash implementation to `/home/user/archiver.sh` and ensure it is executable.