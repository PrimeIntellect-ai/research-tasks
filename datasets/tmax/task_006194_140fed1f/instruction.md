You are tasked with porting and optimizing a legacy data processing tool for a minimal Linux container environment. You need to write a C++ program that implements modern concurrency patterns, performs a database schema migration, and supports cross-compilation/conditional builds.

**Directory & Setup:**
Work in `/home/user/dataport/`. (Create this directory).
Before writing code, create a SQLite database `/home/user/dataport/data.db` with a single table `records (id INTEGER PRIMARY KEY, value TEXT)`. Insert 1000 rows into this table where `value` is simply the string `"item_" + id` (e.g., `"item_1"`, `"item_2"`, etc.).

**C++ Program Requirements (`/home/user/dataport/processor.cpp`):**
1. **Schema Migration:** On startup, the C++ program must connect to `data.db` and perform a schema migration to add a new column: `processed_value TEXT`. (Handle cases where the column might already exist gracefully, or assume it runs once).
2. **Concurrency Pattern:** Implement a Go-style worker pool pattern in C++. You must use `std::thread`, `std::mutex`, and `std::condition_variable` to create a thread-safe "channel" (queue). 
   - A single producer thread reads the rows from the database where `processed_value IS NULL` and pushes them into the channel.
   - 4 consumer (worker) threads pull from the channel, compute the processed value (which should be the original `value` appended with `"_processed"`), and update the database row.
3. **Conditional Builds:** The C++ code must check for a preprocessor macro `MINIMAL_CONTAINER`. 
   - If defined, the program should write a completion message strictly to `/home/user/dataport/minimal_run.log` with the format: `Processed X records.` (where X is the number of updated records).
   - If not defined, it should print the message to standard output.

**Build System Requirements (`/home/user/dataport/Makefile`):**
Write a Makefile with two targets:
1. `default`: Compiles `processor.cpp` into a dynamically linked executable named `processor_dyn` linking against `sqlite3` and `pthread`.
2. `minimal`: Compiles `processor.cpp` into a statically linked executable named `processor_static` linking against `sqlite3` and `pthread`, passing the `-DMINIMAL_CONTAINER` and `-static` flags.

**Execution:**
Once your code and Makefile are ready, run `make minimal`, then execute `./processor_static`. Ensure the database is successfully migrated and updated, and the log file is generated.