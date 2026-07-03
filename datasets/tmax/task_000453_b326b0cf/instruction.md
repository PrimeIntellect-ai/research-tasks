As an observability engineer, you are tuning the Prometheus dashboards for our staging environment's backup infrastructure. The dashboards rely on a custom C utility that parses backup mount usage logs and outputs Prometheus-formatted metrics.

We recently received the source code for the latest version of this utility, which has been extracted to `/app/backup-metric-parser-1.0.0`. However, the deployment pipeline is failing because the vendor accidentally shipped a broken `Makefile` (the compiler is hardcoded to a non-existent compiler alias, `my-gcc-99`).

Your task is to:
1. Locate the vendored package at `/app/backup-metric-parser-1.0.0`.
2. Fix the `Makefile` so that the program successfully compiles using standard `gcc`.
3. Build the utility.
4. "Deploy" the compiled binary by copying it to exactly `/home/user/backup_parser` and ensuring it has executable permissions.

The binary reads a space-separated log string from standard input in the format `<mount_point> <used_bytes> <total_bytes>` and outputs a floating-point metric. You do not need to modify the C source code itself, only the build configuration, and deploy the final executable to the required path.