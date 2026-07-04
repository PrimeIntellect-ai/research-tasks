You are a data analyst optimizing a logistics network. You have been provided with network data in CSV format, but your querying system needs to be rebuilt in Rust to handle specialized routing constraints and aggregates.

Your environment contains the following CSV files in `/home/user/data/`:
1. `hubs.csv`: `hub_id` (integer), `hub_name` (string), `region` (string)
2. `routes.csv`: `src_hub_id` (integer), `dst_hub_id` (integer), `base_distance` (integer)
3. `cargo.csv`: `src_hub_id` (integer), `dst_hub_id` (integer), `shipment_id` (integer), `tonnage` (float)

Additionally, there is an image fixture at `/app/policy.png`. This image contains a printed text memo from the logistics director detailing a global "INTERMEDIATE_HUB_PENALTY" value (an integer distance penalty added to every *intermediate* hub traversed in a path, excluding the start and end hubs). You must extract this value using OCR.

Your task is to write a Rust program that acts as a query engine. 
1. Create a new Rust project at `/home/user/route_engine`.
2. The program must read lines from standard input (`stdin`). Each line will be a query in the format: `start_hub_id,end_hub_id`.
3. For each query, compute the shortest path (lowest total distance, incorporating the intermediate hub penalty extracted from the image) between the two hubs.
4. For the edges that make up this specific shortest path, perform a join with `cargo.csv` to calculate the total `tonnage` of all cargo shipments that flow directly over those exact individual route segments. (If the path is A->B->C, sum the tonnage of cargo on A->B plus the tonnage on B->C).
5. Print the result to `stdout` in EXACTLY this format for each query:
`Query: <start>-><end> | Path: <hub1>-<hub2>-<hub3> | Dist: <total_dist> | Cargo: <total_tonnage_rounded_to_1_decimal>`

If no path exists, print `Query: <start>-><end> | Path: NONE | Dist: 0 | Cargo: 0.0`.

Write, compile (in release mode), and ensure the binary is located at `/home/user/route_engine/target/release/route_engine`. It must be highly optimized as it will be tested against a high-volume fuzzing verifier.