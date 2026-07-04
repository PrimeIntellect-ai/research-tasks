Wake up! It's 3 AM and the production data ingestion pipeline for our IoT telemetry cluster just went down. We are getting paged because the new Rust-based packet processor (`/home/user/telemetry_processor`) is crashing, dropping packets, and outputting incorrect query results compared to our legacy system. 

Here is what we know:
1. **Build Failure**: The junior engineer pushed a hotfix right before leaving, but the Rust code in `/home/user/telemetry_processor` is currently failing to compile. You need to fix the build errors. It seems to be related to some lifetime issues in the concurrent queue and a macro expansion error.
2. **Crash & Logs**: When it did build locally, it was panicking. Check the logs at `/home/user/logs/processor_crash.log` for the traceback. 
3. **Data Loss (PCAP)**: We captured the ingress traffic during the outage in `/home/user/data/ingress.pcap`. The processor is supposed to read these UDP packets, extract the payload, and compute a "Telemetry Hazard Score" using a specific formula.
4. **Incorrect Results (Formula & Query)**: The computed scores are wrong. We have the legacy processing engine as a stripped binary at `/app/legacy_oracle`. The legacy binary takes a hex-encoded packet payload as a command-line argument and prints the correct hazard score. You need to correct the mathematical formula in the Rust processor so its output matches the legacy oracle.
5. **Performance**: The Rust processor is severely bottlenecked due to a concurrency issue (likely a lock contention or deadlock). It needs to process the entire `ingress.pcap` file quickly.

Your tasks:
1. Fix the Rust code in `/home/user/telemetry_processor` so it compiles.
2. Fix the panic/crash identified in the logs.
3. Fix the hazard score formula in `src/formula.rs` by reverse-engineering or fuzzing against `/app/legacy_oracle`.
4. Fix the concurrency bottleneck in `src/worker.rs`.
5. Run your compiled processor on `/home/user/data/ingress.pcap`. Your processor must output a CSV file at `/home/user/output.csv` containing the parsed packet ID and the computed hazard score, like `packet_id,score`.

The automated pipeline will evaluate your fixed code by comparing your `output.csv` against the expected values, and it will measure the execution time. Your processor must achieve a mean squared error (MSE) of exactly 0.0 against the oracle's scores for the pcap, and process the 100,000 packets in the pcap in under 2.0 seconds.