You are an artifact manager responsible for safely packaging binary artifacts into curated repositories. 

Your task is to write a Go program at `/home/user/curate.go` that processes a binary file according to a JSON configuration.

The configuration file is located at `/home/user/config.json` and has the following structure:
```json
{
  "source_file": "/home/user/firmware.bin",
  "chunk_size": 1000,
  "chunk_prefix": "part_",
  "dest_archive": "/home/user/repo/firmware_packaged.tar.gz"
}
```

Your Go program must perform the following steps:
1. Parse the JSON configuration file to determine the parameters.
2. Read the binary file specified by `source_file`.
3. Split the file into chunks of exactly `chunk_size` bytes (the final chunk may be smaller). The chunks must be named `<chunk_prefix>00`, `<chunk_prefix>01`, `<chunk_prefix>02`, etc. (e.g., `part_00`, `part_01`). 
4. Create a `.tar.gz` archive containing *only* these chunk files at the root of the archive (no parent directories). You can use Go's standard `archive/tar` and `compress/gzip` packages, or invoke shell commands using `os/exec` with stream redirection and piping.
5. **Critical Requirement**: To prevent partial reads by clients, you must write the resulting archive to a temporary file first, and then perform an atomic rename to the final `dest_archive` path.
6. Clean up any temporary files or directories created during the process.

Once you have written `/home/user/curate.go`, execute it so that `/home/user/repo/firmware_packaged.tar.gz` is created.

Assume the system already has Go installed. The working directory is `/home/user`. Do not hardcode the paths or values from the JSON in your logic; they must be parsed dynamically.