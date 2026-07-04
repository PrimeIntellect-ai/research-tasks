You are a data analyst optimizing a data pipeline that processes network topology and traffic telemetry.

We have a hierarchical network topology defined in `/app/topology.csv` with the format:
`node_id,parent_id,region`
If a node has no parent, `parent_id` is empty. 

Traffic data is encoded as frame sizes in a diagnostic video artefact located at `/app/traffic.mp4`. 

Your multi-stage pipeline must do the following:
1. **Data Extraction**: Use `ffprobe` (or similar bash tools) to extract the `pkt_size` of every video frame in `/app/traffic.mp4`. Save this as a CSV.
2. **Data Mapping**: Each frame corresponds to a traffic reading for a specific node. Map each 0-indexed frame to a node using the formula: `node_id = frame_index % 500`.
3. **Hierarchical Aggregation (C implementation)**: Write a C program (`/home/user/process_traffic.c`) that reads the topology and the mapped traffic data. 
   - First, sum the base traffic for each node.
   - Second, perform a recursive rollup: a node's total traffic is its own base traffic PLUS the total traffic of all its descendants (recursive children).
   - Finally, summarize the data by `region`. For each region, calculate the sum of the *rolled-up* traffic of only the **top-level** nodes (nodes with no `parent_id`) that belong to that region.
4. **Output**: Your C program should output the final aggregated data to `/home/user/region_traffic.csv` in the exact format:
   `region,total_region_traffic`
   (sorted alphabetically by region).

Compile your C code efficiently (e.g., `gcc -O3`). 

**Verification:**
Your final output `/home/user/region_traffic.csv` will be evaluated by an automated script that calculates the Mean Squared Error (MSE) of the computed traffic aggregates against the true values. To succeed, your MSE must be strictly less than 1.0.