You are a site administrator tasked with configuring the user account management system. 

Your tasks are:
1. **Instruction Extraction**: We have received a screenshot from the lead admin with configuration details. Read the image at `/app/server_instructions.png` (using OCR tools like `tesseract`, which is installed). Extract the timezone and the internal backend port mentioned in the image.
2. **Timezone Configuration**: Write the extracted timezone exactly as it appears in the image into the file `/home/user/timezone.txt`.
3. **Reverse Proxy Setup**: Set up a reverse proxy that listens on local port `8080` and forwards all TCP traffic to the internal backend port you extracted. Run this proxy in the background (you may use `socat`, `nginx` configured for a non-root user, or any other standard tool).
4. **Adversarial Bio Filter**: The site is receiving spam and malicious payloads in user profiles. You must create a Bash script at `/home/user/bio_filter.sh` that reads a user bio from standard input and exits with status `0` if the bio is clean, and status `1` if it is malicious.
   - Malicious bios contain any of the following shell metacharacters: `|`, `;`, `>`, `<`, `$`, or backticks (`` ` ``).
   - Malicious bios also include those containing the word "admin" (case-insensitive).
   - Clean bios contain normal alphanumeric characters, spaces, and safe punctuation (like `.`, `,`, `!`, `?`).
   - The script must correctly classify 100% of the files in `/app/clean_bios/` (must exit 0) and 100% of the files in `/app/evil_bios/` (must exit 1).
5. **Cron Job Fix**: The script `/home/user/sync_users.sh` is triggered by a cron job, but it is currently failing to write its logs properly because it uses a relative path (`echo "Synced" > sync.log`), which writes to the home directory of the cron process instead of `/home/user/`. It also occasionally fails because it relies on the `jq` binary without a proper PATH. Modify `/home/user/sync_users.sh` so that it sets `PATH` to include `/usr/bin` at the top, and uses an absolute path to write its log specifically to `/home/user/sync.log`.

Complete all steps and ensure your background proxy is running.