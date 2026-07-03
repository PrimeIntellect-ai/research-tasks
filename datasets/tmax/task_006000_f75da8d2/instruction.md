You are acting as a cloud architect migrating a legacy notification service. We need to implement a lightweight, idempotent CI/CD pipeline using a bash script to handle the build, storage validation, staged deployment, and mock email notification for a C-based microservice.

I have placed the source code for the new service at `/home/user/src/mailer_daemon.c`. 

Your task is to create a deployment script at `/home/user/pipeline.sh`. The script must perform the following actions exactly when executed:

1. **Compilation**: Compile the C source file `/home/user/src/mailer_daemon.c` using `gcc`. 
2. **Storage/Quota Monitoring**: Check the file size of the compiled binary. The allowed quota is 100,000 bytes. If the binary exceeds this size, the script should exit with code 1 and not proceed.
3. **Idempotent Setup**: Ensure the directory `/home/user/deploy/releases` and `/home/user/alerts` exist. Create them if they do not.
4. **Staged Deployment**: 
   - Calculate the SHA-256 checksum of the compiled binary (using `sha256sum`, extracting just the hash).
   - Move the compiled binary into `/home/user/deploy/releases/mailer_daemon_<sha256_hash>`.
   - Update a symlink at `/home/user/deploy/current` to point to this new release binary. Make sure this step handles existing symlinks gracefully (idempotent configuration).
5. **Email Server Configuration (Mock Alert)**: Generate a deployment alert file at `/home/user/alerts/deploy_email.txt` containing exactly the following lines:
   ```
   To: devops@company.local
   Subject: Deployment successful
   Binary-Size: <size_in_bytes>
   Checksum: <sha256_hash>
   ```
   (Replace `<size_in_bytes>` and `<sha256_hash>` with the actual computed values).

Ensure the bash script `/home/user/pipeline.sh` has executable permissions. 

Run your script to complete the deployment and ensure the final state matches the requirements.