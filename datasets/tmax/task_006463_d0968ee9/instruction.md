You are an edge computing engineer managing automated deployments for IoT devices running via QEMU. A recent deployment pipeline misconfiguration has caused VMs to fail during boot because their `fstab` mount entries are out of order (e.g., trying to mount `/mnt/data/logs` before `/mnt/data` is mounted). 

Your task is to fix this by creating a robust Git-based deployment pipeline that automatically corrects the `fstab` ordering using a custom Rust utility.

Step 1: Create the fstab sorting utility
Create a Rust project in `/home/user/fstab-fixer`. Write a Rust CLI tool that takes two file paths as arguments: an input fstab file and an output fstab file. 
The program must:
- Read the input file.
- Ignore empty lines and lines starting with `#`.
- Parse the valid `fstab` lines (which have 6 whitespace-separated fields). The second field is the mount point.
- Sort the entries topologically based on the mount point length (shortest path first, so parent directories are mounted before their subdirectories). Lexicographical sorting of the mount paths is sufficient for this simple scenario.
- Write the sorted lines to the output file.
- Compile the program for release (`cargo build --release`).

Step 2: Initialize the Deployment Repository
- Create a bare Git repository at `/home/user/iot-repo.git`.

Step 3: Configure the Git Hook
- Write a robust `post-receive` hook in `/home/user/iot-repo.git/hooks/post-receive`.
- The hook must have error handling (e.g., `set -e`).
- The hook receives the `oldrev newrev refname` via standard input.
- It must extract the contents of a file named `device_fstab` from the newly pushed commit (`newrev`).
- Save the extracted content to a temporary file.
- Run the compiled Rust `fstab-fixer` utility on this temporary file to generate the sorted configuration, and save the output exactly to `/home/user/latest_deployment.fstab`.
- On success, the hook must append a single line exactly formatted as `DEPLOY_SUCCESS: <newrev>` to `/home/user/deploy_status.log`.

Step 4: Trigger the Pipeline
- Clone the bare repository to `/home/user/local-repo`.
- In the cloned repository, create a file named `device_fstab` with the following exact content:

```
/dev/vdb /mnt/data/logs ext4 defaults 0 2
/dev/vdc /mnt/data/logs/archive ext4 defaults 0 2
/dev/vda /mnt/data ext4 defaults 0 2
```

- Commit this file with the message "Initial IoT config".
- Push the commit to the `master` branch of the bare repository (which should trigger your hook, process the file, and write the logs).