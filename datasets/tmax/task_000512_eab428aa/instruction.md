You are an IT Support Technician escalating a critical recurring ticket. 

Our internal helpdesk ticket routing service, `ticket_router.py`, has been intermittently dropping incoming tickets during high-traffic bursts. The original developer left the company, leaving us with a buggy Python script and a compiled C binary (`auth_checker`) that the script uses for token validation. 

We have isolated a specific instance of the failure. In `/home/user/ticket_system/`, you will find:
1. `ticket_router.py`: The multi-threaded Python TCP server handling incoming tickets on port 8888.
2. `auth_checker`: A proprietary compiled Linux executable used by the script to validate incoming API tokens.
3. `capture.pcap`: A network packet capture of a recent traffic burst sent to port 8888.
4. `processed_tickets.log`: The log file generated during the exact timeframe of the `capture.pcap` recording.

Your task involves three steps to fully resolve this escalated incident:

**Phase 1: Packet Capture Analysis**
During the burst captured in `capture.pcap`, several tickets were transmitted as JSON payloads over TCP. Due to the server bug, one ticket was successfully transmitted over the network (ACKed by the server) but is entirely missing from `processed_tickets.log`. Identify the `id` of this missing ticket.

**Phase 2: Reverse Engineering**
Sometimes our internal services need to bypass the standard token generation for emergency tickets. The `auth_checker` binary contains a hardcoded "master override" token, but the documentation is lost. Decompile, disassemble, or reverse-engineer `/home/user/ticket_system/auth_checker` to recover this master token. 

**Phase 3: Concurrency Debugging**
The intermittent dropping of tickets is caused by a race condition in `/home/user/ticket_system/ticket_router.py` related to how it tracks and logs processed tickets. Identify and fix the race condition in the Python script. The fixed script must be able to handle 50 concurrent connections without dropping any successfully authenticated tickets or losing count. 

**Deliverables**
1. Fix the code in `/home/user/ticket_system/ticket_router.py`. Do not change the port (8888) or the log file name (`processed_tickets.log`).
2. Create a JSON report at `/home/user/resolution_report.json` with exactly the following structure:
```json
{
  "missing_ticket_id": "<ID of the ticket from Phase 1>",
  "master_token": "<The recovered master token from Phase 2>"
}
```