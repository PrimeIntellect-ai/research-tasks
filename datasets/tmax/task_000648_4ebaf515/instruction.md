You are an SRE on call. Our internal uptime-monitoring service went down hard during a power failure, leaving behind a heavily corrupted Write-Ahead Log (WAL) directory. We have a Go-based recovery tool designed to parse and salvage these records, but it is currently broken in multiple ways.

Your objective is to fix the recovery tool, ensure it compiles, debug its runtime execution, and successfully produce a working sanitizer binary. 

Here are the specific issues you must resolve:

1. **Dependency Conflict:** The source code for the recovery tool is located in `/home/user/recovery_src/`. If you try to build it, you will notice a Go module dependency conflict preventing compilation. Resolve the `go.mod` conflicts so the program builds successfully.
2. **Concurrency Deadlock:** The tool spins up multiple goroutines to process WAL chunks concurrently. However, it currently deadlocks under high contention when writing to the shared recovery channel. Debug and fix `recovery.go` so it no longer deadlocks.
3. **Magic Header Recovery:** The parser requires a specific 8-byte hexadecimal magic header to validate the start of a WAL record. The original developer left the company, but we have a screenshot of the internal wiki documenting this header at `/app/wiki_snapshot.png`. Extract the hex string from this image and update the `MAGIC_HEADER` constant in `recovery.go`.
4. **Adversarial Validation:** Once the tool is fixed, compile it as a standalone executable located at `/home/user/wal_sanitizer`. The binary must take a single file path as a CLI argument. We have provided two directories containing sample WAL files:
   - `/app/wal_clean/`: Contains intact, valid WAL files.
   - `/app/wal_evil/`: Contains malformed, heavily corrupted, or intentionally malicious WAL files that mimic extreme disk corruption.
   
Your compiled binary `/home/user/wal_sanitizer <filepath>` must:
- Print "VALID" to standard output and exit with code `0` for all files in `/app/wal_clean/`.
- Print "CORRUPTED" to standard output and exit with code `1` for all files in `/app/wal_evil/`.

You have standard Linux tools, `go` toolchain, and `tesseract-ocr` available. Do whatever is necessary to produce the correct `/home/user/wal_sanitizer` binary.