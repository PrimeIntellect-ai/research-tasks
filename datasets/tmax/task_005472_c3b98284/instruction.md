You are an edge computing engineer deploying local configuration management to a remote IoT device. Due to network isolation constraints, this device receives updates via a local Git push over a reverse-tunneled SSH connection. You need to set up the receiving repository and the automation hook that applies the configuration.

Perform the following tasks on the device:

1. Initialize a bare Git repository at `/home/user/iot-hub.git`.
2. Create a `post-receive` hook inside this repository (`/home/user/iot-hub.git/hooks/post-receive`). Ensure the hook is executable.
3. The `post-receive` hook must execute the following steps every time new code is pushed:
   a. Check out the pushed files into the directory `/home/user/iot-active` (the hook should create this directory if it doesn't already exist).
   b. Read the contents of the file named `TIMEZONE` located in the root of the newly checked-out code in `/home/user/iot-active`.
   c. Find the process ID of any currently running background process exactly named `edge-daemon` and terminate it gracefully (SIGTERM). Wait for it to exit or give it a moment to terminate.
   d. Start the executable `/home/user/bin/edge-daemon` in the background. Crucially, you must start this process with the `TZ` environment variable set to the exact string read from the `TIMEZONE` file.
   e. Redirect both standard output and standard error of the new `edge-daemon` process to `/home/user/daemon-status.log`.

Do not modify or execute `/home/user/bin/edge-daemon` yourself directly; a dummy version of this script already exists on the system. Your task is only to create the Git repository and write the Git hook. 

Make sure the hook uses robust bash commands to find and stop the daemon, and to parse the `TIMEZONE` file.