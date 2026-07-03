You are acting as a site administrator managing user accounts for our local custom mailing list system. 

We have a Python script, `/home/user/update_users.py`, that is scheduled to run via cron to synchronize our user database (`/home/user/user_db.json`) with our mailing list aliases and our custom firewall rules file. 

However, because cron runs with a minimal environment, the script has been writing its outputs to the wrong directories (it uses relative paths), and worse, it is not idempotent—it blindly appends the configuration every time it runs, causing massive duplicate entries.

Your task is to fix the Python script and run it to configure the system correctly.

Requirements:
1. Fix `/home/user/update_users.py` so that it uses the absolute paths `/home/user/aliases` and `/home/user/firewall.rules` instead of relative ones.
2. Make the script idempotent:
   - For `/home/user/aliases`: It should append `list-<user>: <user>@localdomain.internal` only if the line does not already exist in the file.
   - For `/home/user/firewall.rules`: It should append `-A PREROUTING -p tcp --dport <port> -j REDIRECT --to-ports 2525` only if that exact rule does not already exist in the file.
3. The script reads from `/home/user/user_db.json` which contains a list of dictionaries with keys `"username"` and `"port"`.
4. Run your fixed script.
5. To test idempotency, run your fixed script a second time. There should be absolutely no duplicate entries in either `/home/user/aliases` or `/home/user/firewall.rules`.

Initial State:
- `/home/user/aliases` exists and contains an existing entry: `list-admin: admin@localdomain.internal\n`
- `/home/user/firewall.rules` exists and contains: `-A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-ports 2525\n`
- `/home/user/user_db.json` contains:
```json
[
  {"username": "alice", "port": 8081},
  {"username": "bob", "port": 8082}
]
```

Please correct the Python script and execute it so that the alias and firewall files are updated to their correct, deduplicated states.