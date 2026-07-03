I need help migrating a legacy mathematical processing utility from Python 2 to Python 3. The project is located in `/home/user/math_migrator`.

The utility consists of a Python 2 script (`app.py`) that reads a list of mathematical expressions in Reverse Polish Notation (RPN), evaluates them using a custom C extension (`fastmath.c`), and logs the results to a SQLite database (`data.db`).

However, the migration requires several steps:
1. **Makefile Repair:** The `Makefile` currently uses Python 2 configuration utilities. Update it so it compiles the C extension for Python 3 (specifically Python 3.10 or whatever the default python3 is).
2. **C Extension Migration & Safety:** The `fastmath.c` extension is written using the Python 2 C API (using `Py_InitModule`). Migrate it to the Python 3 C API (`PyModuleDef` and `PyModule_Create`). 
   *Additionally*, there is a severe memory safety bug in the state machine parser inside `fastmath.c`: it does not check for stack underflow when processing operators. If an invalid RPN string (like `"5 + + +"`) is passed, it accesses memory out of bounds. Add a check to ensure there are at least 2 items on the stack before popping for an operation; if not, return `0`.
3. **Database Migration:** The SQLite database `data.db` needs to be updated. Apply the schema migration script `migrate.sql` to the database. It will rename the `equation` column to `math_expr` and add a `result` integer column.
4. **Python Script Migration:** Update `app.py` to be Python 3 compatible (fix print statements, iteration, etc.). Also, modify it so that it correctly uses the new database schema (inserting both the `math_expr` string and the evaluated `result` integer).

Finally, run the updated `app.py`. It will read expressions from `input.txt` and populate `data.db`. Once successfully run, dump the contents of the `history` table in `data.db` to `/home/user/math_migrator/success.log` in the format `id|math_expr|result`, one row per line.