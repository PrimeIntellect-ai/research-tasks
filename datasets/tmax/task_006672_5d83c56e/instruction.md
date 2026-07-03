You are a container specialist migrating a set of microservices from traditional containers to lightweight QEMU virtual machines for enhanced isolation. To standardize the deployment, we need an automated way to generate the VM launch commands based on environment profiles.

Please perform the following tasks:

1. Environment Variable Setup:
Modify the user's shell profile at `/home/user/.bash_profile` to define and export two environment variables:
- `MICRO_MEM` set to `512M`
- `MICRO_VNC_PORT` set to `5`

2. Deployment Script:
Create a Python script at `/home/user/deploy_microservice.py`. This script must:
- Read the `MICRO_MEM` and `MICRO_VNC_PORT` environment variables. If they are not set, it should default to `256M` and `1` respectively.
- Construct the exact QEMU deployment command string replacing the placeholders with the environment variables. The command format must be exactly:
`qemu-system-x86_64 -m <MICRO_MEM> -vnc 127.0.0.1:<MICRO_VNC_PORT> -daemonize -display none`
- Write this constructed command string to a log file located at `/home/user/qemu_cmd.log`. Do not append a newline character to the end of the file unless your script natively does so (either is fine, but the core string must match). Do not actually execute the QEMU command.

After writing the script, execute it once in your terminal (make sure to source your profile first so the variables are present) to generate the `/home/user/qemu_cmd.log` file.