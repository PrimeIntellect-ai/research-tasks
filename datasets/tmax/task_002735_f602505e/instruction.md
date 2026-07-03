You are an infrastructure engineer automating the provisioning of virtual machines. You have a shell script that initiates the VM boot process, but it is known to be flaky and occasionally crashes due to timing issues. 

Your task is to write a C program that acts as a robust process supervisor and storage checker for this provisioning script.

Create a C program at `/home/user/provision.c` with the following requirements:

1. **Storage Monitoring & Environment Setup**:
   - The program must read the `VM_QUOTA_DIR` environment variable. 
   - If the variable is unset, the program should exit immediately with status `2`.
   - Use the `statvfs` system call (from `<sys/statvfs.h>`) to check the available free space in the directory specified by `VM_QUOTA_DIR`.
   - If the available space (`f_bavail * f_frsize`) is less than 1024 bytes, exit immediately with status `2`.

2. **Process Supervision & Restart Policy**:
   - The program must execute the shell script located at `/home/user/flaky_qemu.sh` (using `fork` and `exec` family functions, or `system()`).
   - Wait for the script to finish and check its exit status.
   - If the script exits with status `0`, append the exact string `"Provisioning Success\n"` to `/home/user/provision.log` and exit the C program with status `0`.
   - If the script exits with a non-zero status, append the exact string `"Provisioning Restart\n"` to `/home/user/provision.log` and execute the script again.
   - The program should attempt a maximum of 4 executions (1 initial run + up to 3 restarts). 
   - If the script fails on the 4th attempt, append the exact string `"Provisioning Failed\n"` to `/home/user/provision.log` and exit the C program with status `1`.

Once you have written the C program:
1. Compile it to an executable named `/home/user/provision_bin`.
2. Ensure the `VM_QUOTA_DIR` environment variable is exported and set to `/home/user`.
3. Run the `/home/user/provision_bin` executable so the log file is generated. 

Note: Assume `/home/user/flaky_qemu.sh` already exists and is executable. Do not modify it.