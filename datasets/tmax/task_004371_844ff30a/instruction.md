You are assisting a compliance officer auditing a highly secure data center. We suspect unauthorized access occurred during a lockdown, but our current auditing tools are malfunctioning.

Your objective is to complete the following multi-stage workflow using Bash and standard Linux utilities:

1. **Fix the Audit Script:**
   You will find an SQLite database at `/app/compliance.db` containing `employees` and `room_access` tables.
   There is a bash script at `/home/user/run_audit.sh` that queries this database to list all employees without 'TOP_SECRET' clearance who entered the server room. However, it currently outputs thousands of incorrect results due to a poorly written SQL query (an implicit cross join).
   Fix the SQL query inside `/home/user/run_audit.sh` so it correctly joins the tables and returns only the genuine unauthorized accesses. Save the corrected output to `/home/user/db_breaches.txt` (one employee ID per line).

2. **Video Fixture Processing:**
   A security camera recorded the server room door during the lockdown. The video is located at `/app/server_room_cam.mp4`.
   The video shows employees scanning their badges (represented as QR codes).
   Using `ffmpeg` and `zbarimg` (both pre-installed), extract the employee IDs from the QR codes shown in the video.
   The lockdown occurred strictly between the 00:00:10 and 00:00:25 marks of the video. Any employee ID detected in this time window is considered a "lockdown breach".
   Store these unique employee IDs in `/home/user/video_breaches.txt` (one ID per line).

3. **Cross-Representation Mapping (Graph):**
   We need to map our relational breach data into a graph structure for the forensics team.
   Write a Bash script at `/home/user/generate_graph.sh` that reads both `/home/user/db_breaches.txt` and `/home/user/video_breaches.txt` and generates a valid Cypher script named `/home/user/import.cypher`.
   For every unique employee ID found in *either* file, the Cypher script must contain a parameterised-style or hardcoded statement exactly matching this format:
   `MERGE (e:Employee {emp_id: "ID_HERE"}) MERGE (r:Room {name: "ServerRoom"}) MERGE (e)-[:UNAUTHORIZED_ACCESS]->(r);`

4. **Multi-Protocol Verification Service:**
   Finally, build a simple HTTP server using pure Bash (using `socat`, `nc`, or similar standard tools) listening on `127.0.0.1:8080`.
   The server must:
   - Accept `GET` requests to the endpoint `/check?emp_id=<EMPLOYEE_ID>`
   - Require an `Authorization: Bearer AUDIT_SECURE_99` header. If missing or incorrect, return `HTTP/1.1 401 Unauthorized`.
   - If the requested `<EMPLOYEE_ID>` is present in *either* the DB breaches or the video breaches, return `HTTP/1.1 200 OK` with the exact body `STATUS: BREACH`.
   - If the requested `<EMPLOYEE_ID>` is NOT a breach, return `HTTP/1.1 200 OK` with the exact body `STATUS: CLEAR`.
   - The server must run continuously in the background. Start it and ensure it is listening before completing your task.