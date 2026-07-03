You are an edge computing engineer in charge of deploying firmware updates to a fleet of remote IoT devices. You need to set up a Git-based automated deployment pipeline that checks out code, sets strict permissions, interacts with an emulated edge device via an Expect-like script, and sends an email notification upon completion.

Your environment contains the following pre-existing components:
- A mock IoT device simulator at `/home/user/edge_vm.py`. This script acts like a QEMU serial console for an edge device.
- A local mock SMTP server running on `localhost:1025` which logs received emails to `/home/user/email_outbox.log`.
- A source directory at `/home/user/source_code` containing a file named `firmware.json`.

Perform the following tasks:

1. **Git Repository Setup:**
   Initialize a bare Git repository at `/home/user/edge-firmware.git`.

2. **Automated Pipeline (Git Hook):**
   Create a `post-receive` hook in Python (`/home/user/edge-firmware.git/hooks/post-receive`). When code is pushed to the `main` branch, this hook must:
   - Check out the pushed files to a staging directory at `/home/user/deploy_staging` (create this directory if it doesn't exist).
   - Enforce strict permissions: Change the permissions of `/home/user/deploy_staging/firmware.json` to exactly `0600` (read/write for owner only) for security.

3. **Expect Scripting (Device Interaction):**
   As part of the same `post-receive` hook, use Python's `pexpect` module to interact with the simulated edge device by spawning `/usr/bin/python3 /home/user/edge_vm.py`. 
   The device interaction flow must be:
   - Expect `login: ` -> send `admin`
   - Expect `password: ` -> send `edge_secure_99`
   - Expect `Device> ` -> send `update`
   - Expect `Ready for payload: ` -> send the exact string contents of `/home/user/deploy_staging/firmware.json` (on a single line)
   - Expect `Update SUCCESS` (this indicates the payload was accepted).

4. **Email Notification:**
   If the update is successful (i.e., `Update SUCCESS` is seen), the hook must send an email via the local SMTP server at `localhost:1025`.
   - Sender: `deploybot@edge.local`
   - Recipient: `alerts@edge.local`
   - Subject: `Deploy Success`
   - Body: `The firmware was successfully updated.`

5. **Trigger the Pipeline:**
   Initialize a standard git repository in `/home/user/source_code`, commit the `firmware.json` file, add the bare repository as a remote named `origin`, and push the `main` branch to trigger your hook.

Ensure the hook is executable. If everything is configured correctly, pushing the code will automatically deploy the payload to the emulator and log the email.