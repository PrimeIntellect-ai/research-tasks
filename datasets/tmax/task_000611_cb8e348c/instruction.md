You are an AI assistant helping a scientific researcher recover and organize a corrupted sensor dataset. 

Here is the situation:
We had a system crash that corrupted our main sensor data dump, mixing the valid binary data chunks with random garbage bytes. Fortunately, the valid chunks are structured, and I have a scanned lab note that contains the specific magic header bytes used for our data chunks, as well as the API authentication token required to access the processed data.

Your objectives are:

1. **Extract Metadata from the Lab Note:**
   Read the image located at `/app/lab_note.png`. This image contains a handwritten/typed note that specifies a 4-byte hexadecimal magic header and an alphanumeric `AUTH_TOKEN`. You will need to extract these values (e.g., using `tesseract`).

2. **Recover the Binary Dataset (C++):**
   The corrupted dump is located at `/home/user/raw_sensor.bin`. 
   Write a C++ program to parse this binary file and extract the valid chunks. 
   A valid chunk is defined as:
   - The 4-byte magic header (recovered from the image).
   - Followed immediately by a 4-byte unsigned integer (little-endian) representing the `payload_size`.
   - Followed immediately by `payload_size` bytes of actual data.
   
   Your C++ program should scan the file, extract all the payload bytes (omitting the headers and size fields), and concatenate them sequentially into a single output file named `/home/user/recovered.tar.gz`.

3. **Extract and Clean the Dataset:**
   Extract `/home/user/recovered.tar.gz` into the directory `/home/user/dataset/`.
   Inside, you will find multiple text files containing sensor logs. 
   Perform a large-scale text edit across all extracted files in that directory:
   - Find every instance of the exact string `[ERR_CALIBRATION_LOSS]` and replace it with `NaN`.
   - Find every instance of the string `SENSOR_NODE_00` and replace it with `NODE_0`.

4. **Serve the Cleaned Data (C++):**
   Write and run a C++ HTTP server listening on `127.0.0.1:8000`. 
   The server must handle HTTP GET requests.
   When a client requests `GET /data/<filename>`, the server should return the contents of `/home/user/dataset/<filename>` with a `200 OK` status.
   Crucially, the server MUST require authentication. It must check for the HTTP header:
   `Authorization: Bearer <AUTH_TOKEN>`
   where `<AUTH_TOKEN>` is the token you recovered from the lab note. 
   If the header is missing or incorrect, return a `401 Unauthorized` response.
   Keep this server running in the background.

Please complete all these steps. You may use standard Linux utilities and C++ standard libraries.