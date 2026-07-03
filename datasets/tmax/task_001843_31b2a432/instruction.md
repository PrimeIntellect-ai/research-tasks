You are acting as a Database Administrator and Systems Engineer. We are currently experiencing a severe deadlock in our custom database engine, and our standard diagnostic tools are failing. 

We have dumped the internal lock manager's state into a SQLite database located at `/home/user/db/locks.db`. The database contains the following tables:

1. `transactions`
   - `tx_id` (INTEGER PRIMARY KEY)
   - `query` (TEXT)

2. `locks`
   - `resource_id` (INTEGER)
   - `tx_id` (INTEGER)
   - `status` (TEXT) - Can be either 'HELD' or 'WAITING'

A deadlock occurs when there is a cycle in the "wait-for" graph. A transaction $T_a$ is waiting for $T_b$ if $T_a$ is 'WAITING' for a `resource_id` that is currently 'HELD' by $T_b$.

Your task is to write a C program that maps this relational data into an in-memory graph representation, traverses it to find the deadlock cycle, and outputs the result in a strictly validated JSON schema.

Here are the requirements:
1. Create a C file at `/home/user/workspace/detect_deadlock.c`.
2. The program must connect to `/home/user/db/locks.db` using the SQLite C API (`sqlite3.h`).
3. You must construct a Wait-For Graph (WFG) from the database records.
4. Detect the directed cycle in the graph. There is guaranteed to be exactly one connected cycle.
5. Once the cycle is found, the program must output a JSON file to `/home/user/workspace/deadlock_report.json`.
6. The JSON file must strictly follow this schema:
   ```json
   {
     "cycle": [tx_id_1, tx_id_2, ..., tx_id_n]
   }
   ```
   *Constraint:* The array of `tx_id`s in the cycle must start with the **numerically lowest** `tx_id`, and then follow the directed path of the cycle (i.e., `tx_id_1` waits for `tx_id_2`, which waits for `tx_id_3`, etc.).
7. You must compile the program and run it to produce the `deadlock_report.json` file. Ensure `sqlite3-pcre` or `libsqlite3-dev` is installed if you need it. You can install standard packages using `sudo apt-get` if necessary, though typical dev tools are present. (Run without `sudo` if permissions permit, or use `apt` as root via standard means if available; in this environment, you have the required access to install standard libraries).

Ensure the output file exactly matches the schema and logical ordering, as it will be validated by an automated parser.