You are a deployment engineer tasked with rolling out a new C++ based mailing list dispatcher using a blue/green staged deployment strategy. 

The current dispatcher (v1) is installed at `/home/user/app/v1/dispatcher`, with a symlink `/home/user/app/current` pointing to `/home/user/app/v1`. 

Your task is to write, build, and deploy version 2 of this dispatcher, set up the required directory structure, and process a batch of pending emails.

**Phase 1: Write the v2 C++ Dispatcher**
Write a C++ program and save its source to `/home/user/workspace/dispatcher_v2.cpp`.
The program must:
1. Accept exactly one command-line argument: the absolute path to an email file.
2. Read the email's contents from `stdin`.
3. Parse the email headers to find two specific lines:
   - `To: <list_name>@localhost` (extract `<list_name>`)
   - `Message-ID: <msg_id>` (extract `<msg_id>`, ignoring any surrounding angle brackets if present).
4. Create a symbolic link pointing to the file specified in the command-line argument. The symlink should be created at: `/home/user/mail_queue/lists/<list_name>/<msg_id>.eml`.
5. If the required headers are missing, exit with code 1. Otherwise, exit with code 0.

**Phase 2: Directory Management & Build**
1. Create the `v2` application directory: `/home/user/app/v2/`.
2. Compile your C++ program using `g++` and output the executable to `/home/user/app/v2/dispatcher`.
3. Create the directory structure for the mailing lists: `/home/user/mail_queue/lists/announce/` and `/home/user/mail_queue/lists/discuss/`.

**Phase 3: Staged Deployment**
Perform an atomic deployment by updating the symlink `/home/user/app/current` to point to `/home/user/app/v2` instead of `v1`. The symlink update must be done such that there is no point in time where `current` does not exist (e.g., using `ln -sfn`).

**Phase 4: Process Pending Emails**
There are pending `.eml` files in `/home/user/mail_queue/incoming/`. 
Write a bash script at `/home/user/workspace/process_queue.sh` that iterates over all `.eml` files in `/home/user/mail_queue/incoming/` and processes them using the newly deployed `/home/user/app/current/dispatcher`. For each file, pass its absolute path as the argument and pipe its contents to the dispatcher's stdin.
Execute your script so that all emails are processed.

Ensure all directories have appropriate permissions (755) and the bash script is executable.