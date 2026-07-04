You are a backup administrator for an industrial manufacturing facility. A critical machine control system continuously logs print telemetry and state data. 

Currently, a background process is constantly archiving this active state into a nested archive file at `/home/user/data.tar.gz`. Because the file is frequently overwritten, attempting to read it directly often results in an `EOFError` or corrupted archive errors. 

To prevent read/write collisions, the writer process exclusively locks a dedicated synchronization file located at `/home/user/shared.lock` during the write operation.

Your task is to write and execute a Python script that does the following:
1. Safely acquires an appropriate file lock (using `fcntl`) on `/home/user/shared.lock`.
2. While the lock is held, opens and extracts the contents of `/home/user/data.tar.gz`.
3. Inside the tarball, you will find a ZIP archive named `inner.zip`. Extract it in memory or to disk.
4. Inside `inner.zip` is a domain-specific machine file named `layer_data.gcode`.
5. Parse the `layer_data.gcode` file to find the maximum `Z` coordinate value across all `G0` and `G1` movement commands. (e.g., in `G1 X10 Y20 Z30.5`, the Z value is 30.5).
6. Save the maximum Z value you find as a plain number (e.g., `12.34`) to `/home/user/max_z.txt`.

Ensure your script handles the locking correctly, otherwise it will crash due to concurrent modification by the background process. All operations should be performed within the `/home/user` directory.