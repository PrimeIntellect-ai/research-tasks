As a backup operator testing our disaster recovery procedures, you need to automate the verification of our restored Git repositories. 

We have a set of backup archives in `/home/user/backups/`. Each archive is a tarball (e.g., `repoA.tar.gz`) containing a bare Git repository and a `manifest.txt` file detailing the repository's owners and group assignments. 

Additionally, our security team provided a proprietary validation tool located at `/app/repo-validator`. Unfortunately, the source code was lost, and it is a stripped binary. This tool checks the integrity of the commit history, but you need to figure out its required input format by analyzing it (objdump, strings, and standard debugging tools are available).

Your task is to write and run a Go web service that listens on `127.0.0.1:8080`. 
The service must implement the following:

1. **Endpoint `POST /restore`**: 
   - Accepts a JSON payload: `{"repo_name": "<name>"}` (e.g., `repoA`).
   - Extracts `/home/user/backups/<name>.tar.gz` to `/home/user/restored/<name>`.
   - Uses text processing utilities (like awk/grep) to parse `manifest.txt` inside the extracted folder to find the designated primary owner.
   - Executes the `/app/repo-validator` binary against the restored Git repository, passing the required arguments you reverse-engineered.
   - Returns an HTTP 200 JSON response `{"status": "success", "owner": "<parsed_owner>", "validator_output": "<output>"}` if everything is valid, or an HTTP 400 on failure.

2. **Git Hook Configuration**:
   - As part of the restore process in the Go service, dynamically create a `pre-receive` hook in the restored bare repository that prevents any user not listed in `manifest.txt` from pushing.

Write the Go service in `/home/user/backup_service.go` and start it in the background. Do not hardcode the names of the repositories, as the automated tester will submit arbitrary repository names from the backup directory.