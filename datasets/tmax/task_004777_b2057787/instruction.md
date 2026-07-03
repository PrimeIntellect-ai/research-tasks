**Ticket #8842: ticket-db crashes on startup due to corrupted WAL**

Hi IT Support,

Our internal ticketing system backend (`ticket-db`) crashed after a recent power outage. Whenever we try to start it, it panics with a "slice index out of bounds" error. 

The application is written in Rust and is located at `/home/user/ticket-db`. It reads a Write-Ahead Log (WAL) located at `/home/user/ticket-db/data/wal.dat`. It appears the last entry in the WAL file is truncated/corrupted, causing the parser to read an incorrect length and panic when trying to access the slice.

We need you to do the following to resolve this ticket:
1. **Understand the codebase:** Inspect `/home/user/ticket-db/src/main.rs` to understand how the WAL is parsed.
2. **Fix the code:** Modify the parsing logic so that if it encounters an incomplete or corrupted entry (e.g., there are not enough bytes left in the file to satisfy the entry's length), it gracefully stops reading and returns the valid records parsed up to that point, rather than panicking.
3. **Write a regression test:** In `/home/user/ticket-db/src/main.rs`, add a new test function named `test_corrupted_wal_recovery` that asserts the parser correctly extracts valid entries and ignores the truncated tail from a dummy corrupted byte slice. Ensure `cargo test` runs and passes.
4. **Recover the data:** Once fixed, run the application to dump the database to a JSONL file:
   `cargo run -- export > /home/user/recovered_tickets.jsonl`

Please complete these steps. We will verify that `cargo test` passes (and includes your new test) and that `/home/user/recovered_tickets.jsonl` contains the successfully recovered valid entries.