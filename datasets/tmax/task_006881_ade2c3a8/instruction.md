You are a cloud architect tasked with migrating a legacy service's file structure to a new storage volume. The migration must be fully automated, idempotent, and reproducible. 

To achieve this, you need to build a configuration management tool in Rust that reads a desired filesystem state and enforces it (creating directories, empty files, and symlinks, and setting standard UNIX permissions).

Your task is to:
1. Create a Rust source file at `/home/user/migrator.rs`.
2. The Rust program must define or read a specific desired filesystem state and enforce it within the target directory `/home/user/new_volume`. 
3. The program must be **idempotent**: running it multiple times should not result in errors or duplicate files, and it should correct any permissions or symlinks that deviate from the desired state.
4. The desired state to enforce inside `/home/user/new_volume` is:
    - Directory: `configs` (Permissions: 750)
    - Empty File: `configs/database.conf` (Permissions: 600)
    - Directory: `data` (Permissions: 700)
    - Directory: `data/v1` (Permissions: 755)
    - Symlink: `data/active` (Points to: `v1`)
    - Symlink: `current_config` (Points to: `configs/database.conf`)

Compile and run your Rust program to generate the required filesystem structure. 

After your Rust program has successfully run, execute the following command to generate a verification log:
`cd /home/user/new_volume && find . \( -type d -o -type f -o -type l \) -printf "%y %P %m\n" | grep -v "^\." | sort > /home/user/migration_verify.log`
*(Note: Symlink permissions typically show up as 777 in find, which is expected).*

Additionally, append the symlink targets to the log to verify link structure management:
`cd /home/user/new_volume && find . -type l -printf "%P -> %l\n" | sort >> /home/user/migration_verify.log`

Ensure all paths, permissions, and links match the exact specifications.