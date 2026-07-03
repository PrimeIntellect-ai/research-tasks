You are a site administrator tasked with building an automated system to manage user network provisioning. You need to set up a Git-based workflow where pushing a configuration file triggers a Rust-based tool to generate network routing rules and audit logs, and configure log rotation for the system.

You must implement the following components entirely within `/home/user/`:

1. **Git Repository & Hook:**
   - Create a bare Git repository at `/home/user/accounts.git`.
   - Create a `post-receive` hook in this repository that does the following:
     - Checks out the pushed code into a worktree at `/home/user/accounts_worktree/` (create this directory).
     - Compiles the Rust project located at `/home/user/src/network_provisioner/` in release mode.
     - Executes the compiled Rust binary, passing the path to `/home/user/accounts_worktree/users.json` as the first command-line argument.

2. **Rust Provisioning Tool:**
   - Create a new Rust project at `/home/user/src/network_provisioner/`.
   - The tool must read a JSON file (the path is provided as the first argument) containing an array of user objects. Example format:
     `[{"username": "alice", "subnet": "10.0.1.0/24"}, {"username": "bob", "subnet": "10.0.2.0/24"}]`
   - For each user in the JSON array, the tool must:
     - Append a line to `/home/user/logs/provision.log` (create the directory if it doesn't exist) exactly in this format: 
       `[YYYY-MM-DD HH:MM:SS] Provisioned user <username> with subnet <subnet>` 
       *(Use UTC time for the timestamp)*.
     - Append a routing command to an `iproute2` batch file located at `/home/user/network/routes.batch` (create the directory/file if needed) in this format:
       `route add <subnet> dev dummy0`
   - The tool must clear/truncate the `/home/user/network/routes.batch` file at the start of its execution so it only contains the routes from the current JSON file.

3. **Log Rotation:**
   - Create a logrotate configuration file at `/home/user/logrotate.conf`.
   - The configuration must target `/home/user/logs/provision.log`.
   - It should specify: daily rotation, keep 5 rotated backups, compress the rotated logs, and missing ok.
   - Set it to create a new file with permissions `0644`.

Ensure your scripts and Rust code handle missing directories gracefully or that your setup script creates them before execution. All paths must be absolute and within `/home/user/`.