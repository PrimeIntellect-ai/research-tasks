You are a cloud architect migrating services to a new infrastructure. As part of this migration, we have a legacy local daemon written in C that initiates data syncs, but it unfortunately only accepts interactive input. 

You need to automate interactions with this daemon using `expect` and schedule it.

Here are your tasks:
1. Compile the C source file located at `/home/user/legacy_daemon.c` using `gcc` and name the executable `/home/user/legacy_daemon`.
2. Write an `expect` script at `/home/user/trigger_migration.exp` that automates the following interaction with `/home/user/legacy_daemon`:
   - Wait for the prompt: `"Enter Auth Key: "`
   - Send the string: `"cloud_admin_99"` followed by a newline.
   - Wait for the prompt: `"Command: "`
   - Send the string: `"START_MIGRATE"` followed by a newline.
   - Wait for the prompt: `"Target IP: "`
   - Send the string: `"10.0.0.50"` followed by a newline.
   - Wait for the program to finish (expect eof).
3. Run your `expect` script once and redirect its standard output to `/home/user/migration_run.log`.
4. Create a crontab-format file at `/home/user/migration.cron` that schedules the `expect` script to run at exactly the top of every hour (minute 0). Use the absolute path `/usr/bin/expect /home/user/trigger_migration.exp > /home/user/migration_run.log` for the cron command.