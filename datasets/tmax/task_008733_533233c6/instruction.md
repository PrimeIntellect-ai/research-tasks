You are a container specialist managing a custom microservice environment. Since you do not have root access in this containerized environment, you must implement a user-space C-based microservice that processes mailing list submissions, handles timezone conversions, and simulates group-based administration.

Your objective is to build and run an automated email processing system.

Step 1: Idempotent Setup Script
Write an idempotent bash script at `/home/user/setup_microservice.sh` that:
- Creates the following directories if they do not exist: `/home/user/mail/inbox`, `/home/user/mail/processed`, `/home/user/mail/archive`.
- Creates a mock group database at `/home/user/groups.db` containing exactly the following lines (recreating it if it doesn't match):
  alice:admin
  bob:staff
  charlie:guest

Step 2: C Mail Processor Microservice
Write a C program at `/home/user/mail_processor.c` and compile it to `/home/user/mail_processor`.
The program must:
1. Scan the `/home/user/mail/inbox/` directory for files ending with `.eml`.
2. For each file, parse the contents. The files will have the following format:
   Sender: <name>
   Date: <YYYY-MM-DDTHH:MM:SSZ> (This is in UTC)
   Subject: <text>
3. Look up the `<name>` in `/home/user/groups.db` to find their group. If not found, default to `unknown`.
4. Convert the parsed UTC date to the `America/New_York` timezone.
5. Append a log entry to `/home/user/mail/processor.log` EXACTLY in this format:
   `[YYYY-MM-DD HH:MM:SS] Processed email from <Sender> (Group: <Group>)`
   *(Note: The timestamp in the log MUST be the converted America/New_York time).*
6. If the Group is `admin` or `staff`, move the `.eml` file to `/home/user/mail/processed/`. Otherwise, move it to `/home/user/mail/archive/`.

Step 3: Execution
- Run your setup script.
- Compile your C program (ensure you handle timezone appropriately, for example by using `setenv("TZ", "America/New_York", 1)` and `tzset()`).
- Assume there are `.eml` files already placed in `/home/user/mail/inbox/` (do not delete or overwrite existing `.eml` files before your program runs).
- Run your compiled `/home/user/mail_processor` program so it processes the inbox.

Verify your work by ensuring `/home/user/mail/processor.log` is generated with the correct localized timestamps and that the files have been moved to their respective directories.