We are hardening our server configurations and migrating away from an old, undocumented legacy binary used to validate our custom firewall configuration files. The legacy binary, located at `/app/firewall_validator_oracle`, takes a single configuration string as a command-line argument and outputs an integer validation score to stdout. If the score is above 0, the configuration is considered valid; otherwise, it is invalid.

Unfortunately, we lost the source code for this binary. Your task is to:
1. Analyze the `/app/firewall_validator_oracle` binary to understand its scoring algorithm. (Tools like `objdump`, `gdb`, and `strings` are available).
2. Reimplement the exact same scoring logic in C.
3. Save your C source code to `/home/user/validator.c` and compile it to `/home/user/validator`. Your compiled binary must accept a single string as a command-line argument and print only the resulting integer score to stdout, exactly matching the behavior of the legacy binary for any input.
4. Create a systemd service unit file at `/home/user/validator.service` (do not attempt to install or start it system-wide, just create the file) that executes `/home/user/validator "test_string"` and restarts always on failure with a 5-second delay.

Please ensure your C program behaves identically to the oracle for all possible string inputs, as it will be rigorously tested against random strings.