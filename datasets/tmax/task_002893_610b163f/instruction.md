As a system administrator, you need to automate a diagnostic routine inside a rootless containerized environment to troubleshoot a silent failure where network routes aren't mapping correctly to an in-memory filesystem.

Your task is to write a Python automation script at `/home/user/automate_container.py` that programmatically creates a container-like namespace, configures networking, sets up a temporary filesystem, and extracts the routing information.

Requirements for `/home/user/automate_container.py`:
1. Use Python (you may install and use the `pexpect` library if desired, or use standard libraries).
2. The script must spawn an interactive bash shell inside a new user, mount, and network namespace using the command: `unshare --user --map-root-user --net --mount --fork /bin/bash --noprofile --norc`
3. Programmatically interact with this shell to execute the following steps in order:
    a. Bring up the loopback interface (`lo`).
    b. Create a new dummy network interface named `net0`.
    c. Assign the IP address `192.168.100.1/24` to `net0`.
    d. Bring the `net0` interface up.
    e. Create a directory at `/mnt/ramdisk`.
    f. Mount a `tmpfs` filesystem at `/mnt/ramdisk`.
    g. Dump the current routing table in JSON format into a file inside the mount: `/mnt/ramdisk/routes.json` (Hint: use `ip -j route`).
    h. Copy the generated `/mnt/ramdisk/routes.json` file to the host environment at `/home/user/routes_output.json`.
    i. Gracefully exit the namespace shell.

The automated test will run `python3 /home/user/automate_container.py` as the standard `user`. It will then verify that the script completes successfully and that the file `/home/user/routes_output.json` exists, is valid JSON, and contains the correct route for the `192.168.100.0/24` subnet on the `net0` device. 

Ensure your script handles bash prompts correctly and adds suitable delays or waits for shell readiness to avoid silent execution failures.