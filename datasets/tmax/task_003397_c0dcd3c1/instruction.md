You are an infrastructure engineer automating the provisioning of a custom application's filesystem and logging structure. 

An interactive binary tool located at `/home/user/init_fs` is used to configure the application's logging parameters. Because this tool is strictly interactive and we need to automate the provisioning process, you must use `expect` to drive it. Furthermore, you need to write a C utility that enforces the filesystem structure based on the tool's output, and configure `logrotate` for the resulting logs.

Perform the following tasks:

1. **Automate Interactive Provisioning (`expect` script)**
   Write an `expect` script at `/home/user/run_init.exp` that executes `/home/user/init_fs`. The tool will prompt you for three values sequentially. You must provide the following responses:
   - "Enter log directory path: " -> Provide `/home/user/custom_logs`
   - "Enter log rotation size limit: " -> Provide `5M`
   - "Enter number of rotations to keep: " -> Provide `3`
   
   Once executed, the binary will generate a configuration file at `/home/user/provision_config.txt` containing these key-value pairs. Run your expect script to generate this file.

2. **Filesystem Setup Utility (C Code)**
   Write a C program at `/home/user/create_dirs.c`. This program must:
   - Read `/home/user/provision_config.txt`.
   - Parse the `LOG_DIR=` line to extract the directory path.
   - Use POSIX system calls (like `mkdir`) to create the specified directory (with `0755` permissions). Include robust error handling: it should print an error and exit gracefully if it fails for any reason other than the directory already existing.
   - Create an initial empty log file inside that directory named `setup.log` (e.g., `/home/user/custom_logs/setup.log`).
   
   Compile this C program to `/home/user/create_dirs` using `gcc` and execute it to create the directory structure and initial log file.

3. **Log Configuration**
   Write a user-space `logrotate` configuration file at `/home/user/custom_logrotate.conf` to manage the logs in the newly created directory. It must apply to all `.log` files in the directory specified above and enforce the following rules:
   - Rotate when the file size reaches `5M`
   - Keep `3` rotations
   - Do not throw an error if the log file is missing (`missingok`)
   - Do not mail log files (`nomail`)

Ensure all steps are complete and the files are exactly where specified.