We are migrating our legacy trajectory analysis system from Python 2 to Python 3. The system consists of a Python migration script, an SQLite database, a C-based constraint solver, and a WebSocket service. 

Your objective is to complete the migration and end-to-end integration by following these steps:

1. **Schema Migration**: 
   The script `/home/user/project/migrate_db.py` was written in Python 2. Update its syntax to be compatible with Python 3, then run it to apply the schema migration to our database located at `/home/user/project/db.sqlite3`. This will add a required column.

2. **C Compilation & Debugging**: 
   We use a C program (`/home/user/project/solver.c`) to solve a constraint satisfaction problem: finding the optimal launch angle for a projectile to hit a target.
   - The `Makefile` in the directory is currently broken. Fix it so that running `make` compiles `solver.c` into an executable named `solver`.
   - The `solver.c` code has a logical mathematical bug related to standard numerical API usage (trigonometric functions expect a specific unit). Fix the bug so it correctly evaluates the constraints (Distance `R` between 99m and 101m, Max Height `H <= 25m`) and prints the maximum valid integer angle.

3. **Database Update**: 
   Take the integer angle output by your fixed C solver and UPDATE the `configurations` table in `/home/user/project/db.sqlite3` for the row where `id = 1`. Set the newly migrated `max_angle` column to this value.

4. **WebSocket Communication**: 
   A local WebSocket server is running in the background at `ws://localhost:8080`. Send a JSON payload exactly matching `{"angle": <YOUR_ANGLE>}` (replace `<YOUR_ANGLE>` with the integer value) to this endpoint using any tool or script you prefer. If the payload is correctly formatted, the server will log an acknowledgment.

5. **Solution Record**: 
   Finally, write the raw integer angle directly into a file at `/home/user/project/solution.txt`.

Ensure all operations are confined to the `/home/user/project` directory.