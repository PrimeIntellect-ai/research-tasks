I am migrating an old legacy Python REST API to a modern Flask-based API, and I need an automated end-to-end test script to ensure the new API returns the exact same data as the legacy one.

There are two Python scripts located in your home directory:
1. `/home/user/legacy_api.py` (uses standard library `http.server`)
2. `/home/user/new_api.py` (uses Flask)

Your task is to create a shell script at `/home/user/run_e2e.sh` that orchestrates a test between these two APIs. 

The script must perform the following actions exactly in this order:
1. Create a Python virtual environment at `/home/user/venv`.
2. Install `Flask` into this virtual environment.
3. Start `/home/user/legacy_api.py` on port 8080 in the background. (It takes a port argument: `python3 legacy_api.py 8080`).
4. Start `/home/user/new_api.py` on port 8081 in the background using the virtual environment's python. (It takes a port argument: `/home/user/venv/bin/python new_api.py 8081`).
5. Wait up to 3 seconds to ensure both servers have fully started.
6. Make a GET request using `curl -s` to `http://localhost:8080/api/data`.
7. Make a GET request using `curl -s` to `http://localhost:8081/api/data`.
8. Compare the raw JSON response strings from both servers. 
9. If the outputs exactly match, write the word `PASS` to `/home/user/test_report.txt`. If they differ or fail, write `FAIL` to `/home/user/test_report.txt`.
10. Ensure both background server processes are killed before the script exits to avoid hanging ports.

Once you have written `/home/user/run_e2e.sh`, make it executable and run it to produce the `/home/user/test_report.txt` file.