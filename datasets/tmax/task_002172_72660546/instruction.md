You are a Cloud Architect migrating legacy applications to a GitOps-based orchestration system. The old system relies heavily on direct filesystem mounts and custom network link definitions, which now need to be dynamically parsed upon code deployment.

Your task is to set up a local Git-based deployment workflow that processes mock system configurations automatically.

Perform the following steps:

1. Create a bare Git repository at `/home/user/git-server/deploy.git`.
2. Create the target deployment directories: `/home/user/deploy/src/` and `/home/user/deploy/out/`.
3. Create a Git `post-receive` hook in the bare repository. This hook must:
    a. Check out the latest pushed files into `/home/user/deploy/src/`.
    b. Read a file named `virtual_fstab` (which uses standard Linux fstab format) from the pushed files. Extract the mount point (the second column) for every entry where the filesystem type (the third column) is strictly `xfs`. Write these mount points, sorted alphabetically, to `/home/user/deploy/out/xfs_volumes.txt`, one per line.
    c. Read a file named `network_links.txt` from the pushed files. Each line will contain three space-separated fields: `source_service target_service port`.
    d. Generate a strict JSON file at `/home/user/deploy/out/mesh.json` representing a dictionary where each key is a `source_service`, and its value is a list of strings formatted as `"target_service:port"`.

4. After configuring the hook, clone the bare repository to `/home/user/workspace`.
5. Inside the cloned repository, create the following two files:

`virtual_fstab`:
```text
/dev/sda1 /mnt/data ext4 defaults 0 0
/dev/sdb1 /app/logs xfs defaults 0 0
10.0.0.5:/nfs /nfs/shared nfs rw 0 0
/dev/sdc1 /app/cache xfs noatime 0 0
/dev/sdd2 /opt/db xfs rw,noexec 0 0
```

`network_links.txt`:
```text
api-gateway user-service 8080
api-gateway payment-service 8443
user-service postgres-db 5432
payment-service postgres-db 5432
```

6. Commit these files to the repository's `master` branch and push them to the bare repository.
7. Ensure your hook correctly executes and generates the expected `/home/user/deploy/out/xfs_volumes.txt` and `/home/user/deploy/out/mesh.json`. You can use any language (Bash, Python, etc.) to write the `post-receive` hook, but make sure it is fully self-contained and executable.