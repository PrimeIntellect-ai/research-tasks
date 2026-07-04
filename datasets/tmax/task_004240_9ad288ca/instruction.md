You are a cloud architect tasked with migrating services from a proprietary legacy infrastructure to a modern cloud environment. 

In our legacy environment, server routing tags are generated dynamically based on the system's timezone, locale, disk capacity, and region. This is currently handled by a proprietary, compiled binary located at `/app/legacy_router_configurator`. As part of the migration, we must deprecate this binary and replace it with a native Python solution.

Your task has three parts:

**Part 1: Reverse-Engineer the Legacy Binary**
The executable `/app/legacy_router_configurator` takes exactly 4 positional arguments:
`./legacy_router_configurator <timezone> <locale> <disk_capacity_bytes> <region>`
Example: `./legacy_router_configurator UTC en_US.UTF-8 50000000 us-east-1`

Analyze the binary's behavior (you can run it, use `strings`, `strace`, `ltrace`, or `objdump`). Write a Python script at `/home/user/migrator.py` that precisely mimics the behavior and output of the legacy binary. It must accept the exact same four positional CLI arguments (using `sys.argv`) and print the resulting configuration string to standard output. Your Python implementation must be bit-exact equivalent for any input.

**Part 2: Text Processing & Environment Extraction**
Write a shell script at `/home/user/generate_tag.sh` that dynamically gathers the current system's metrics to feed to your Python script. The script must:
1. Extract the system's timezone from `/etc/timezone`.
2. Extract the `LANG` variable value from `/etc/default/locale` (e.g., `en_US.UTF-8`).
3. Determine the total 1K-blocks size of the root `/` filesystem (parse this dynamically using `df` and text processing tools like `awk` or `sed`).
4. Invoke your Python script (`/home/user/migrator.py`) passing the timezone, locale, root filesystem size, and a hardcoded region of `eu-west-2`.

**Part 3: Service Configuration**
To prepare for the new environment, create a standard systemd service unit file at `/home/user/routing-tag.service`. This file should define a `oneshot` service that executes `/home/user/generate_tag.sh`. It must include a `[Unit]` section with a basic description, a `[Service]` section specifying `Type=oneshot` and `ExecStart`, and an `[Install]` section with `WantedBy=multi-user.target`. 

Do not attempt to start or enable the service as you do not have root privileges, but ensure the configuration file is perfectly formatted.