You are a performance engineer tasked with debugging a metric ingestion pipeline that keeps crashing under load.

The pipeline consists of two Bash-based services running via `socat`:
1. **Ingest Service** (`/app/ingest_service.sh`): Listens on TCP port 8000. It reads raw metric lines from clients, appends a timestamp, and forwards them to the DB service.
2. **DB Service** (`/app/db_service.sh`): Listens on TCP port 8001. It processes the metrics and calculates a "load score" (cpu + mem) before returning an "OK" response to the ingest service, which is relayed to the client.

Recently, the DB service started crashing and dropping connections. A packet capture was taken exactly when the crash occurred, saved at `/app/bottleneck.pcap`.

Your tasks:
1. Analyze `/app/bottleneck.pcap` (using `tcpdump` or similar) to identify the corrupted inputs being sent by legacy clients.
2. Modify `/app/ingest_handler.sh` (called by the Ingest Service) to properly sanitize incoming network data and strip out the corrupted characters seen in the pcap (e.g., carriage returns or null bytes) before forwarding to the DB service.
3. Modify `/app/db_handler.sh` (called by the DB Service) to handle edge cases in format parsing. If a metric value (like memory) is missing or non-numeric (e.g., `NaN` or `N/A`), the DB service must catch this edge case, default the corrupted value to `0`, and successfully process the metric without crashing its arithmetic evaluation.
4. Start both services in the background so they are listening on their respective ports (8000 and 8001).

Requirements:
- The services must run on `127.0.0.1`.
- The `Ingest Service` must listen on TCP port 8000.
- The `DB Service` must listen on TCP port 8001.
- An automated verifier will connect to `127.0.0.1:8000` via raw TCP and send a mix of healthy and corrupted payloads. Your fixed pipeline must respond with `OK\n` to all of them.