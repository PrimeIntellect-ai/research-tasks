You are tasked with helping a developer organize and clean up project files by identifying and quarantining corrupted binary artifacts based on multi-line log records.

Your goal is to write a Rust program that automates this process. You must create your Rust project in `/home/user/organizer` (e.g., using `cargo new /home/user/organizer`). 

Here is the current state of the filesystem:
- `/home/user/project_logs/`: Contains several `.log` files.
- `/home/user/artifacts/`: Contains binary artifact files named with the pattern `[ArtifactID].dat`.
- `/home/user/quarantine/`: An empty directory where corrupted artifacts must be moved.

**Log Format:**
The log files contain multi-line records separated by a line containing exactly `---`.
A record looks like this:
```
[2023-10-24T12:00:00Z]
Level: ERROR
Event: ArtifactValidation
ArtifactID: bin-12345
Reason: Checksum mismatch
```
Note: A record block might not have all these fields, or they might be in a different order, but they always pertain to the same event until the next `---` separator or EOF.

**Your Rust program must perform the following actions:**
1. **Parse the logs:** Read all `.log` files in `/home/user/project_logs/`. Extract the `ArtifactID` for any log record block where the `Level` is `ERROR` AND the `Reason` is `Checksum mismatch`. Both conditions must be present in the same block.
2. **Move corrupted binaries:** For each identified corrupted `ArtifactID`, locate the corresponding `[ArtifactID].dat` file in `/home/user/artifacts/` and move it to `/home/user/quarantine/`.
3. **Generate a report atomically:** Create a report containing the `ArtifactID`s of all the quarantined files, sorted alphabetically, with one ID per line. To prevent partial reads by other systems, you *must* write this report to a temporary file (e.g., `/home/user/quarantine_report.txt.tmp`) first, and then use an atomic rename operation to rename it to `/home/user/quarantine_report.txt`.

Write, compile, and run your Rust program to complete these file operations. Do not leave any `.tmp` files behind.