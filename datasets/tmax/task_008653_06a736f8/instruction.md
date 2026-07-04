You are a systems programmer debugging a deployment issue for a highly concurrent Go-based mathematical processing engine. The Go application, `/home/user/math_runner`, computes matrix determinants using a heavily optimized C shared library (`libmatrix.so`) distributed across multiple goroutines.

Currently, the system is failing due to two issues: a dynamic linking failure (ABI version mismatch) and a downstream data ingestion failure caused by concurrent output scrambling and an outdated data schema.

Your task is to fix the deployment entirely using Bash scripting.

**Phase 1: Dynamic Library Linking and Semantic Versioning**
The application requires `libmatrix.so`, but there are multiple versions of this library located in `/home/user/clibs/`. Due to a recent ABI breaking change, the application will only work with library versions `>= 1.5.0` and `< 2.0.0`. 

Write a bash script at `/home/user/run_app.sh` that:
1. Iterates through the libraries in `/home/user/clibs/` (named in the format `libmatrix.so.X.Y.Z`).
2. Uses pure Bash or standard coreutils to perform semantic version comparison and select the **highest** available version that satisfies `>= 1.5.0` and `< 2.0.0`.
3. Creates a symlink named `/home/user/clibs/libmatrix.so` pointing to the selected version.
4. Correctly sets `LD_LIBRARY_PATH` and executes `/home/user/math_runner`.

*(Note: `/home/user/math_runner` is already fully compiled and available. It will automatically write to `/home/user/output_v1.log` if it successfully links to the correct library version).*

**Phase 2: Concurrency De-scrambling and Schema Migration**
Because `/home/user/math_runner` utilizes Go channels to stream mathematical results concurrently from various worker threads, the resulting `/home/user/output_v1.log` is out of order. Additionally, the downstream analytics pipeline requires a schema migration from the old log-based format to a strict CSV format.

The `v1` log lines in `/home/user/output_v1.log` look exactly like this:
`[Worker <id>] Schema=v1 | Determinant=<value> | MatrixID=<id>`

Write a bash script at `/home/user/migrate.sh` that:
1. Parses `/home/user/output_v1.log`.
2. Extracts the `MatrixID`, `Worker`, and `Determinant` fields.
3. Migrates the data to a `v2` schema which is a CSV file saved at `/home/user/final_v2.csv`.
4. The `v2` schema format MUST strictly be: `MatrixID,Determinant,WorkerID` (with a header row).
5. Due to the concurrent nature of the Go engine, you must sort the output numerically in **descending order** based on the `Determinant` mathematical value to reconstruct a deterministic output.

Ensure both scripts are executable. Run `/home/user/run_app.sh` followed by `/home/user/migrate.sh` to produce the final `/home/user/final_v2.csv` file. Do not run any commands as root.