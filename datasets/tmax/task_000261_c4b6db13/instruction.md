I am a researcher organizing a messy dataset, and I need your help building a robust data-serving tool in C.

My dataset is located at `/home/user/dataset`. Unfortunately, a previous automated backup script went rogue and created recursive symlinks throughout the directory structure, forming infinite loops. 

Your task is to write a single C program at `/home/user/dataset_server.c` and compile it to `/home/user/dataset_server` (you may link against `zlib` and other standard libraries, e.g., `gcc -O2 dataset_server.c -o dataset_server -lz`). The compiled program must do the following when executed:

1. **Safe Traversal:** Recursively traverse `/home/user/dataset` while completely avoiding infinite symlink loops.
2. **Decompression & Parsing:** Identify all files ending in `.json.gz`. These are gzip-compressed files where each line is a JSON object. Read and decompress these streams in memory.
3. **Filtering:** Parse the uncompressed lines and retain only the JSON objects where the key `"is_research_target"` is set to the boolean value `true`.
4. **Authentication Extraction:** I have left an image file at `/app/dataset_auth.png` which contains our lab's API token text (e.g., `LAB-XYZ123`). You will need to extract this token text using OCR before or during your server setup.
5. **HTTP Server:** Bring up a basic HTTP server in your C program listening on `127.0.0.1:8080`.
   - It must expose a single endpoint: `GET /api/targets`.
   - It must require an `Authorization: Bearer <TOKEN>` header, where `<TOKEN>` is the exact string extracted from the image (ignoring any leading/trailing whitespace). If the header is missing or incorrect, return a `401 Unauthorized`.
   - If authenticated, return a `200 OK` with a `Content-Type: application/json` header, and the response body must be a single JSON array containing all the retained target JSON objects (order does not matter).

Please implement this, compile it, and leave the server running in the background so it can be queried.