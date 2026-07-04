You are tasked with building a configuration management tracking service for a DevOps team. The team exports server configurations as wide-format CSV files, but they need to be normalized, anonymized, and served via a secure local TCP service. 

Here are your requirements:

1. **Extract Authentication Code**: 
   There is an image file located at `/app/auth_code.png`. Use OCR (e.g., `tesseract`) to extract the 6-digit passcode from this image. This passcode will be used to authenticate requests to your service.

2. **Data Processing (C++)**:
   Write a C++ program at `/home/user/config_svc.cpp` that processes the configuration files found in `/app/configs/`. 
   - **Parallel Processing**: The program should read and process the files concurrently.
   - **Encoding**: Some files are standard UTF-8, but others might be exported from legacy Windows systems in UTF-16LE. Your C++ code must correctly parse both encodings into standard UTF-8 strings.
   - **Wide-to-Long Reshaping**: The input CSVs are in wide format: `ServerName,ConfigKey1,ConfigKey2,...` with the second row containing the values. You must reshape this into a long format: `ServerName,ConfigKey,ConfigValue`.
   - **Anonymization**: If a `ConfigKey` contains the substrings `PASSWORD`, `TOKEN`, or `SECRET` (case-insensitive), its `ConfigValue` must be replaced entirely with the literal string `***`.

3. **Serve the Data**:
   The same C++ program must spawn a TCP server listening on `127.0.0.1:8888`. 
   - When a client connects, it must wait for the client to send the extracted 6-digit passcode followed by a newline character (`\n`).
   - If the passcode is incorrect, the server should drop the connection.
   - If the passcode is correct, the server should respond with the processed long-format data in CSV format, sorted alphabetically by `ServerName` and then by `ConfigKey`, and then close the connection.
   - The CSV response must have the header: `ServerName,ConfigKey,ConfigValue`.

Compile and run your C++ service in the background so that it is actively listening on port 8888 when you complete the task. You may install any standard package via `apt` if needed.