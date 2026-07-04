I am trying to automate the startup of a local QEMU virtual machine environment using systemd user services, but I'm running into a dependency issue. 

I have created two user services:
1. `prepare-disk.service`: A oneshot service that prepares the directory structure and creates a symlink to the base disk image.
2. `vm-launcher.service`: A service that runs a Python script (`/home/user/scripts/launch_vm.py`) to launch the VM.

Currently, if I try to start `vm-launcher.service`, it fails because the disk symlink doesn't exist yet. The `vm-launcher.service` does not know that it needs to wait for `prepare-disk.service` to run first, nor does it automatically pull it in.

Your task is to fix this issue:
1. Modify the unit file for the VM launcher located at `/home/user/.config/systemd/user/vm-launcher.service`.
2. Add the correct systemd directives so that `vm-launcher.service` strictly requires `prepare-disk.service` to start successfully, and ensures it runs *after* it.
3. Reload the systemd user daemon.
4. Start `vm-launcher.service`.

If you do this correctly, the Python script will detect the prepared disk structure and write a success message to `/home/user/vm_run.log`.