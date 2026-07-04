We have a custom application stack managed by a lightweight Python-based service manager because we do not have root access on this environment to use `systemd`. However, our bootstrap process is currently failing. 

When you run `python3 /home/user/mini_init.py start`, the service `app_worker.service` crashes immediately on startup. 

You need to perform the following tasks:

1. **Diagnose and Fix the Service Startup:**
   Examine `/home/user/mini_init.py` and the service definitions in `/home/user/services/`. You will find that `app_worker.service` is failing because it tries to start before `auth_server.service` is fully initialized. Fix the service definition for `app_worker.service` by adding the correct dependency directive so that `mini_init.py` starts `auth_server.service` first.
   Once fixed, start the services using `python3 /home/user/mini_init.py start > /home/user/startup_success.log`.

2. **Application User Administration via Scripting:**
   The `auth_server` relies on a local JSON database of users located at `/home/user/auth_db.json`. You need to populate this database based on a raw user export found at `/home/user/raw_users.txt`.
   
   Write a robust, idempotent Python script at `/home/user/sync_auth_users.py` that does the following:
   * Reads `/home/user/raw_users.txt`.
   * Uses text processing logic to filter out invalid lines. A valid line strictly follows the format `username:role:uid` (e.g., `alice:admin:1001`). Lines missing fields, having too many fields, or where `uid` is not an integer must be safely ignored/skipped.
   * Updates or creates the JSON file `/home/user/auth_db.json` ensuring the state matches the valid entries in the text file. 
   * The structure of `/home/user/auth_db.json` must exactly be a JSON object mapping usernames to their details:
     ```json
     {
       "alice": {
         "role": "admin",
         "uid": 1001
       }
     }
     ```
   * The script must be idempotent: running it multiple times should not corrupt the file or produce duplicate entries.

Execute your script to generate the correct `/home/user/auth_db.json` file. Ensure both `/home/user/startup_success.log` and `/home/user/auth_db.json` exist and are correct before finishing.