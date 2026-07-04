You are an assistant helping a backup operator test the restore procedure of a legacy mailing list architecture. The system relies on a local SMTP receiver, a Redis instance, and an archive worker. We need to restore the environment, set up process supervision, and recreate a missing piece of legacy C code used for backup obfuscation.

Here are your tasks:

1. **User and Group Administration**
   Create a local group named `archive_grp`.
   Create a user named `archive_usr` belonging to the `archive_grp` group.

2. **Legacy Obfuscator Recovery (C Programming)**
   The legacy backup system used a custom C utility to obfuscate and de-obfuscate mailing list archive chunks. We have a compiled, stripped binary at `/app/oracle/obfuscator_oracle`, but the source code was lost. 
   Write a C program at `/home/user/obfuscator.c` and compile it to `/home/user/obfuscator`. 
   It must exactly match the behavior of the oracle. The oracle reads binary data from `stdin` until EOF (up to 1024 bytes) and writes the transformed data to `stdout`. 
   The algorithm specification is:
   - Read all input bytes.
   - Reverse the entire sequence of bytes.
   - XOR every byte in the reversed sequence with the hex value `0x5A`.
   - Write the result to `stdout`.

3. **Process Supervision & Service Composition**
   We use `supervisord` to manage the services. A skeleton configuration file is located at `/home/user/supervisord.conf`. 
   Configure it to run the following three services (all must run in the foreground under supervisor, without daemonizing):
   - `redis`: Start the redis server using `/usr/bin/redis-server --port 6379`.
   - `smtp_receiver`: A Python script at `/app/smtp_receiver.py` (listens on port 2525).
   - `archive_worker`: A Python script at `/app/archive_worker.py`. This worker relies on the `obfuscator` binary you created. You must set the environment variable `OBFUSCATOR_BIN=/home/user/obfuscator` in the supervisor config for this specific program.
   Ensure that `smtp_receiver` and `archive_worker` run as the user `archive_usr`.

4. **Rolling Restarts Script**
   Write a bash script at `/home/user/rollout.sh` that safely restarts the mailing list services in a staged manner using `supervisorctl` (assume supervisor is running on the default unix socket).
   The script must:
   - Restart `archive_worker` first.
   - Sleep for 2 seconds.
   - Restart `smtp_receiver`.
   Make the script executable.

Ensure that `/home/user/obfuscator` compiles successfully using `gcc /home/user/obfuscator.c -o /home/user/obfuscator`. Do not start the supervisord daemon yourself; the automated verifier will launch it using your configuration file and test the end-to-end mail flow by sending an email to port 2525.