You are tasked with building a binary artifact ingestion pipeline for a local artifact manager. The system relies on three components: an Nginx reverse proxy, a Flask artifact registry, and a Redis metadata store.

Your task has two main parts:

### Part 1: The C++ Artifact Normalizer
You must write a C++ program at `/home/user/artifact_ingestor.cpp` and compile it to `/home/user/artifact_ingestor`.
This program acts as a binary normalizer. It must read raw binary data from standard input (`stdin`) until EOF, and write the normalized binary data to standard output (`stdout`).

The normalization protocol is as follows:
1.  **Magic Header:** The output must begin with the 4-byte ASCII string `ARTI` (Hex: `0x41 0x52 0x54 0x49`).
2.  **Size Header:** Followed by a 4-byte unsigned integer (little-endian) representing the total number of bytes read from stdin.
3.  **Data Payload:** Followed by the input data, but with a byte-stuffing algorithm applied:
    *   Any occurrence of the byte `0xFF` in the input must be replaced with the two bytes `0xFE 0x01`.
    *   Any occurrence of the byte `0xFE` in the input must be replaced with the two bytes `0xFE 0x00`.
    *   All other bytes are passed through unmodified.

Your compiled program must be bit-exact in its output compared to our reference implementation.

### Part 2: The Glue and Services
There is a multi-service setup located in `/app/services/`.
1.  Start the services by running `bash /app/services/start_services.sh`. This will spin up Redis on port 6379, a Flask backend on port 5000, and Nginx on port 8080.
2.  Create a bash script at `/home/user/watcher.sh`. This script must:
    *   Recursively watch the directory `/home/user/incoming/` for newly created files (e.g., using `inotifywait`).
    *   Whenever a new file is created in this directory, it must pipe the file's contents through your `/home/user/artifact_ingestor` program.
    *   The stdout of the ingestor must be piped into an HTTP POST request (e.g., using `curl`) to `http://127.0.0.1:8080/upload?name=<filename>` where `<filename>` is the basename of the new file. Make sure to send the binary data in the body of the request.
3.  Ensure your watcher script is running in the background and executable. 

Create the `/home/user/incoming/` directory before starting your watcher. The testing framework will drop new binary files into this directory and query Redis to verify the end-to-end integration was successful.