You are a QA engineer tasked with setting up a performance and security test environment for a modernized authentication microservice. The old system used insecure plain-text passwords and a legacy Node.js hashing utility. You need to migrate the database schema, translate the hashing logic to Python, compile it for performance testing, and benchmark it.

Here is the step-by-step requirement:

1. **Environment Setup**
   Work within `/home/user/qa_env/`. 

2. **Schema Migration & Code Translation**
   The legacy database is located at `/home/user/qa_env/db/users_v1.db`. It contains a single table `old_users` with columns: `id` (INTEGER), `username` (TEXT), `password` (TEXT - plain text).
   
   The new authentication system requires a more secure hash. The legacy Node.js migration script defined the new hashing algorithm as:
   `sha256(username + password + "QA_SECURE_SALT_2024")` (returning a lowercase hex string).
   
   Create a Python module `/home/user/qa_env/src/auth_hash.py` containing a function `generate_hash(username, password)` that implements this logic.
   
   Then, write and execute a migration script to create a new database at `/home/user/qa_env/db/users_v2.db`. The new schema must be:
   `CREATE TABLE secure_users (user_uuid TEXT PRIMARY KEY, username TEXT, pass_hash TEXT);`
   
   Migrate all users from `users_v1.db`. For each user, generate a standard UUID4 string for `user_uuid`, keep the `username`, and use your `generate_hash` function to compute the `pass_hash`.

3. **Cross-Compilation**
   To test if we can optimize the hashing throughput in production, we will use Cython.
   Write a `setup.py` in `/home/user/qa_env/src/` to compile `auth_hash.py` into a C-extension module (e.g., `auth_hash.c` and a compiled `.so` file) using Cython. Compile it in place so it can be imported as a standard Python module.

4. **Performance Benchmarking**
   Write a benchmarking script `/home/user/qa_env/bench.py`. 
   The script should:
   - Measure the time it takes to compute `generate_hash("testuser", "testpass")` 50,000 times using the standard Python execution (you can run this before compilation or use the `.py` source explicitly).
   - Measure the time it takes to run the exact same loop using the compiled Cython extension.
   - Save the results in a JSON file at `/home/user/qa_env/results/metrics.json` strictly matching this format:
     ```json
     {
       "python_duration_seconds": 1.25,
       "cython_duration_seconds": 0.85,
       "cython_is_faster": true
     }
     ```
   
Ensure all directories are created if they don't exist, and that `metrics.json` and `users_v2.db` are successfully generated with the correct data.