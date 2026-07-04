You are acting as a build engineer managing a large repository of build artifacts. Our CI pipeline produces thousands of artifact manifest files, and we need a fast, concurrent tool to process them and calculate a custom storage metric used for build tiering.

I need you to write a Go program that processes a directory of JSON manifests concurrently. 

Here are the details:
1. **Input Data**: The manifest files are located in `/home/user/artifacts/`. There are exactly 1,000 JSON files named `manifest_0.json` through `manifest_999.json`.
2. **File Format**: Each JSON file has the following structure:
   ```json
   {
     "artifact_id": "string",
     "timestamp": "string",
     "dependencies": [
       {
         "name": "string",
         "size_bytes": <integer>
       }
     ]
   }
   ```
3. **Numerical Algorithm**: For each manifest, you need to calculate a `manifest_metric`. 
   The `manifest_metric` is calculated as the sum of `(size_bytes * (index + 1)) % 9973` for all dependencies in that file's `dependencies` array. (Note: `index` is the 0-based index of the dependency in the array, so the first dependency uses index+1 = 1).
4. **Concurrency**: Because of the high I/O latency on our actual NFS (simulated here), your Go program MUST process these files concurrently using goroutines and channels. A worker pool or a simple spawn-per-file pattern communicating the partial sums back to a main channel is required.
5. **Output**: Sum the `manifest_metric` for all 1,000 files to get the `total_metric`. Serialize and write this final result to `/home/user/build_report.json` with the following exact format:
   ```json
   {
     "total_metric": <integer>
   }
   ```

Please write and execute the Go program to produce the `/home/user/build_report.json` file.