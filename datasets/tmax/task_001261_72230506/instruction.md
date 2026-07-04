You are a developer organizing a large repository of 3D printing projects (GCode) and compiled firmware files (ELF). To streamline storage, your team uses a custom proprietary archive format called "GPAK" and an automated ingestion pipeline.

Your task has two parts:

### Part 1: Reverse Engineer and Implement the GPAK Archiver
A compiled reference binary for the GPAK format exists at `/app/bin/gpak-ref`.
You need to write a Python equivalent at `/home/user/gpak.py` that can pack a directory into a `.gpak` file. Your script must produce **bit-exact identical output** to the reference binary for any given directory. 

You can run `/app/bin/gpak-ref pack <output.gpak> <input_directory>` to observe its behavior.
By analyzing the outputs, reverse-engineer the binary format and write your Python script. It must support:
`python3 /home/user/gpak.py pack <output.gpak> <input_directory>`
`python3 /home/user/gpak.py unpack <input.gpak> <output_directory>`

*Hint on format:* The format includes a magic header, a file count, and a sequential list of file entries (path, sizes, compressed payload). The paths are stored alphabetically, and the compression uses standard zlib.

### Part 2: Fix the Ingestion Pipeline
Your team has an ingestion pipeline that accepts uploaded `.gpak` archives, extracts them, and counts the total number of movement commands (`G0` and `G1`) across all included `.gcode` files, caching the result.

The pipeline consists of:
1. **Nginx** (listening on port 8080)
2. **Flask API** (running via Gunicorn on port 5000, located in `/app/api/`)
3. **Redis** (listening on port 6379)

Currently, the pipeline is broken. You need to:
1. Fix the Nginx configuration at `/etc/nginx/sites-available/default` so that requests to `http://localhost:8080/api/` are correctly reverse-proxied to the Flask app.
2. Edit `/app/api/app.py` to:
   - Connect to the local Redis instance correctly.
   - Use your `/home/user/gpak.py` script to unpack the uploaded `.gpak` file into a temporary directory.
   - Iterate through all unpacked files. For every file ending in `.gcode`, count the total number of lines that begin exactly with `G0` or `G1` (ignoring leading whitespace).
   - Store the grand total in Redis under the key `gpak:<original_filename_without_extension>:movement_lines`.
3. Restart Nginx and the Flask application so they are fully operational.

Ensure all services are running and integrated before you finish.