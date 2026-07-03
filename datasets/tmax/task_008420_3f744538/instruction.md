You are tasked with building a lightweight Python-based "operator" script that manages simulated Virtual Machine manifests. Instead of a full Kubernetes environment, you will process a local JSON manifest file defining desired VM states, back it up, and generate executable shell scripts to manage the lifecycles of these VMs via simulated QEMU commands.

Your objective is to write and execute a Python script at `/home/user/vm_operator.py`. 

The script must perform the following tasks:

1. **Read Manifest**: Parse the JSON manifest located at `/home/user/manifests/vms.json`.
2. **Backup Strategy**: Before processing, create an exact copy of the manifest file at `/home/user/backup/vms.json.bak`. Your script should ensure the `/home/user/backup/` directory exists.
3. **Robust Processing & Error Handling**: Iterate over the VMs defined in the `vms` array. 
    - Each VM object will typically contain `name`, `memory`, `vnc_port`, and `image`.
    - If the `vnc_port` is missing, default it to `5900`.
    - If the `image` field is missing, the script must gracefully catch this error, skip the creation of the runner script for this VM, and log an error.
4. **Virtualization Management**: For every valid VM, generate an executable bash script (chmod +x) at `/home/user/runners/<vm-name>.sh`. Ensure the `/home/user/runners/` directory exists. 
    - The generated script must contain exactly one line simulating the start command: 
      `qemu-system-x86_64 -m <memory> -hda <image> -vnc :<display>`
    - The `<display>` value must be calculated as `vnc_port - 5900` (e.g., port 5902 becomes VNC display `:2`).
5. **State Logging**: Write the status of each VM to a log file at `/home/user/operator_state.log`.
    - If successful, append: `[SUCCESS] Created runner for <vm-name>`
    - If the `image` is missing, append: `[ERROR] Missing image for <vm-name>`

Write the script, run it, and ensure all directories, backups, runner scripts, and log files are successfully created with the correct formats.