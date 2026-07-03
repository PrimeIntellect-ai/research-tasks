You are acting as a backup administrator managing an archiving system. 

We have a system with a couple of background services running in our container:
1. `wal-writer`: A simulated database writer that continuously writes Write-Ahead Log (WAL) records to `/app/wal_data/`. The active WAL file is pointed to by a symbolic link `/app/wal_data/active.wal`. When a file gets too large, it is rotated and the symlink is updated.
2. `nginx`: A web server configured as a reverse proxy, currently listening on port 8000, but its configuration is broken and missing the correct upstream routes.

The WAL format is a custom binary format. Each record consists of:
- A 4-byte header: `0x57 0x41 0x4C 0x52` ("WALR" in ASCII).
- A 4-byte unsigned integer (little-endian) representing the Record ID.
- A 4-byte unsigned integer (little-endian) representing the length of the data payload ($L$).
- The data payload ($L$ bytes of ASCII text).

Your task:
1. Write a C++ service located at `/home/user/archive_service.cpp` and compile it to `/home/user/archive_service`.
2. The C++ service must run as a daemon or background process listening on TCP port 8080.
3. When it receives an HTTP `GET /record/<id>` request (where `<id>` is the integer Record ID), it must parse the WAL files in `/app/wal_data/` (starting from the active symlink and traversing older files if necessary) to find the specified record.
4. It should respond with a `200 OK` HTTP response containing the exact data payload of the requested record as the body. If the record is not found, return `404 Not Found`.
5. Fix the nginx configuration located at `/etc/nginx/sites-available/default` (or create it and link to `sites-enabled`) so that any request to `http://127.0.0.1:8000/api/record/<id>` is proxied to your C++ service at `http://127.0.0.1:8080/record/<id>`.
6. Restart nginx to apply the changes and ensure your C++ service is running.

You must only use standard C++ libraries or `sys/socket.h` for the server (no external HTTP frameworks are provided). Ensure your parser handles the binary format correctly and manages the file links efficiently.