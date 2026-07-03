You are tasked with organizing and fixing a partially built backend service in `/home/user/project`. The previous developer left things in a messy state, and the application cannot start.

Currently, the application relies on a custom C binary that fails to run due to missing shared libraries. Additionally, the SQLite database needs to be migrated, and a simple REST API interface needs to be written in Bash to handle incoming requests.

Your goal is to write a bash script `/home/user/project/setup_and_run.sh` that performs the following tasks:

1. **Shared Library Management:**
   There is a pre-compiled binary at `/home/user/project/bin/calculator` and two versions of a shared library it might need:
   `/home/user/project/libs/v1/libcalc.so`
   `/home/user/project/libs/v2/libcalc.so`
   The binary specifically requires the `v1` ABI. You must create a wrapper script at `/home/user/project/run_calc.sh` that correctly sets the environment so that when `./run_calc.sh 5` is executed, it successfully runs the `calculator` binary with the `v1` shared library, passing the argument `5` to it.

2. **Schema Migration:**
   There is a SQLite database at `/home/user/project/data.db` and several SQL migration files in `/home/user/project/migrations/`.
   Your `setup_and_run.sh` script must apply all `.sql` files found in the `migrations` directory to `data.db` in alphabetical order.

3. **REST API Construction (Bash):**
   Your `setup_and_run.sh` must generate a script at `/home/user/project/api_handler.sh`. This script will act as a CGI-like handler. It will receive a raw HTTP GET request on standard input.
   If the request line starts with `GET /calculate HTTP/1.1`, the script should:
   - Query the `data.db` database for the value of `factor` from the `settings` table (you can assume there's only one row).
   - Execute the `/home/user/project/run_calc.sh` wrapper, passing the retrieved `factor` as the argument.
   - Output a valid HTTP/1.1 200 OK response with a JSON body containing the result: `{"result": <output_of_calculator>}`.
   If the request is anything else, it should return an `HTTP/1.1 404 Not Found` with an empty body.

Make sure your `setup_and_run.sh` script is executable. You do not need to start a long-running web server; an automated test will pipe raw HTTP requests directly into your `api_handler.sh` to verify its correctness.