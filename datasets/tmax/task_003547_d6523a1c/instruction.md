As a technical writer, I am organizing and migrating our old system documentation. The legacy documentation is stored in a proprietary binary format called "DocWAL". We have a compiled reference binary at `/app/bin/oracle_extractor` that perfectly reads this format from `stdin` and outputs the extracted markdown to `stdout`, but we've lost the source code and need to rewrite it in C for future maintenance.

Additionally, our documentation preview system relies on a microservice architecture (Nginx, Flask, and Redis) that is currently misconfigured. 

Your task consists of two parts:

**Part 1: Rewrite the DocWAL Extractor in C**
Create a C program at `/home/user/extractor.c` and compile it to `/home/user/extractor`. It must read a DocWAL binary stream from `stdin` and output the extracted text to `stdout`, mimicking `/app/bin/oracle_extractor` exactly.
The DocWAL format is defined as follows:
- **Header:** 4 bytes magic (`DOCW`) followed by 1 byte version (`0x01`). If these do not match exactly, print "INVALID" to `stderr` and exit with code 1.
- **Records:** A sequence of records immediately follows the header. Each record has:
  - 1 byte `type`
  - 2 bytes `length` (unsigned 16-bit integer, little-endian)
  - `length` bytes of `payload`
- **Record Types:**
  - `0x01`: Text chunk. You must extract and output this payload to `stdout`.
  - `0x02`: Author metadata (ignore, do not output).
  - `0x03`: Timestamp metadata (ignore, do not output).
  - `0xFF`: End of File. Stop parsing immediately and exit cleanly (code 0).
- You must exactly concatenate the text payloads (type `0x01`) in the order they appear without adding any extraneous newlines or spaces.

**Part 2: Fix and Start the Documentation Preview System**
The preview system code is located in `/home/user/doc_system/`.
It consists of three services that you must configure and start:
1. **Redis**: Needs to run on `127.0.0.1:6379`. The config file is at `/home/user/doc_system/redis.conf`.
2. **Flask API**: Located at `/home/user/doc_system/flask_app.py`. It currently tries to call the old oracle binary. Modify it to execute your new `/home/user/extractor` instead. It runs on port `5000`.
3. **Nginx**: The configuration file is at `/home/user/doc_system/nginx.conf`. It is supposed to run on port `8080`. Fix the Nginx configuration so that any requests to `/api/` are properly proxied to the Flask app running on `127.0.0.1:5000`. 

Once you have compiled the C program and fixed the configurations, start all three services in the background. Nginx should be started using `nginx -c /home/user/doc_system/nginx.conf -p /home/user/doc_system/`.