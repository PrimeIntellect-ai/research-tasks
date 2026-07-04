You are acting as a support engineer collecting diagnostics from a customer's edge device. The device experienced a critical failure. The system's diagnostic daemon, provided to you as `/home/user/logger_bin`, intercepts failures and serializes a proprietary crash report to a file named `crash.dat` on a dedicated partition. 

Unfortunately, a flawed cleanup cron job immediately deleted `crash.dat` before the device was powered off. The customer has provided a raw filesystem image of this partition at `/home/user/diag_fs.img`.

Your task is to:
1. Recover the deleted `crash.dat` file from the unmounted filesystem image `/home/user/diag_fs.img`. Save the recovered file to `/home/user/recovered.dat`.
2. Reverse engineer the provided `/home/user/logger_bin` (an ELF binary) to understand the serialization format of the diagnostic payload. Look for how it structures the binary data it writes.
3. Write a Minimal Reproducible Example (MRE) in C, saved as `/home/user/mre.c`, that reads `/home/user/recovered.dat`, parses the custom serialization format, and extracts the numeric error code.
4. Compile your MRE and run it so that it outputs the extracted error code to `/home/user/error.log` strictly in the following format:
`Error: <integer_value>`

You must use standard bash utilities, binary analysis tools (like `strings`, `objdump`, `gdb`), and filesystem debuggers (like `debugfs`) to complete this task. Do not attempt to mount the image, as you do not have root privileges.