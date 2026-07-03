You are a data analyst working with user telemetry time-series data. You need to process a stream of CSV records containing location data.

You have been provided with a local, vendored C package located at `/app/geo_mask-1.2`. This package contains a utility designed to process these CSV lines from standard input. 

For each line of input formatted as `timestamp,user_id,x,y,notes`, the utility is supposed to:
1. **Mask** the `user_id` by replacing it entirely with the string `MASKED`.
2. **Compute Distance**: Calculate the Euclidean distance of the point `(x, y)` from the origin `(0, 0)`.
3. **Encoding Validation (Quality Gate)**: Check if the `notes` field contains exclusively valid ASCII characters (values 0-127). If the `notes` field contains any non-ASCII characters (e.g., UTF-8 special characters or emojis), the entire record must be dropped.

If the record passes the quality gate, it should output: `timestamp,MASKED,distance,notes`, where the distance is rounded to 2 decimal places.

Unfortunately, the vendored package is slightly broken. The `Makefile` fails to compile the application due to a missing linker flag for the math library.

**Your task:**
1. Navigate to `/app/geo_mask-1.2`.
2. Fix the perturbation in the `Makefile` so that the program compiles successfully.
3. Compile the application.
4. Copy the successfully compiled executable to `/home/user/processor`.

Your final compiled binary at `/home/user/processor` must perfectly match the intended behavior. An automated verifier will strictly fuzz your executable against a known-good oracle with thousands of random CSV inputs to ensure absolute bit-exact equivalence of the standard output.