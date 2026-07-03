You are an IT support technician responding to an escalated ticket. 

Ticket details:
"Our background worker process has been experiencing severe memory bloat. We suspect it is caching sensitive customer payloads indefinitely. We took a raw memory dump of the crashed process before it was killed, located at `/home/user/dump.bin`. The worker's source code is located at `/home/user/app/worker.py`. We need to identify the leaked secret token for the user 'admin_01' and create a minimal reproducible example (MRE) of the memory leak."

Your objectives:
1. **Analyze the Memory Dump**: Use standard Linux CLI tools to extract strings from `/home/user/dump.bin`. Find the JSON payload associated with `"user_id": "admin_01"`. Extract the value of the `"token"` field (which starts with `SECRET_TOKEN_`) and save this exact token string to `/home/user/leaked_token.txt`.
2. **Understand the Codebase**: Review `/home/user/app/worker.py` to identify the global variable that is functioning as a cache and causing the memory leak.
3. **Create a Minimal Reproducible Example**: Write a Python script at `/home/user/mre.py` that demonstrates the bug. 
   - Your script must import the leaky function and the global cache variable from `app.worker`.
   - It must call the function three times, using the `user_id`s: `"test1"`, `"test2"`, and `"test3"`, passing `"dummy_data"` as the payload each time.
   - Finally, the script must calculate the number of items (keys) in the global cache dictionary and write that integer to `/home/user/cache_size.txt`.

Run your `mre.py` script to ensure it generates the `/home/user/cache_size.txt` file correctly.