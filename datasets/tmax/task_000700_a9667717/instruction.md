You are tasked with debugging a failing C++ build for a data analysis tool and recovering its required dataset. The project is located in `/home/user/project`.

When you run `make`, the build fails due to linker errors. Furthermore, even if you fix the build, the resulting executable `./analyzer` is known to hang indefinitely (deadlock) when run. The original developer mentioned you might need to use system call tracing (`strace`) to figure out what file it is silently waiting for or failing to open before deadlocking.

Additionally, the tool reads from a SQLite database located at `/home/user/project/sensor_data.db`. Unfortunately, this database file was corrupted. You must recover the data from the corrupted database (you can use standard sqlite3 recovery tools/commands) into a working SQLite database at the same path.

Finally, the `calculate_pop_stddev` function in `stats.cpp` has a bug in its mathematical formula. It is supposed to calculate the **Population Standard Deviation** of the values in the database, but it currently returns an incorrect result.

Your tasks:
1. Fix the `Makefile` so the project compiles successfully into an executable named `analyzer`.
2. Diagnose and fix the hang (create any missing configuration files that `strace` shows the program trying to access before it hangs). The file just needs to exist; its contents don't matter.
3. Recover the SQLite database `/home/user/project/sensor_data.db`.
4. Correct the formula in `stats.cpp` to properly compute the Population Standard Deviation.
5. Run the fixed `./analyzer` and save its precise standard output to `/home/user/solution.txt`.

The final output in `/home/user/solution.txt` should look exactly like this:
`Result: <computed_value>`
(where `<computed_value>` is the correctly calculated population standard deviation formatted to 4 decimal places).