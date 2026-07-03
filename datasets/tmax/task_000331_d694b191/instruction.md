You are a mobile build engineer responsible for maintaining our app's asset delivery pipeline. Our mobile application ships with thousands of localized assets that need to be grouped into download bundles. 

Currently, we use a proprietary, closed-source tool located at `/app/legacy_packer` to generate these bundles. It takes a JSON list of assets and outputs a packing configuration. However, it is incredibly slow and single-threaded. 

Your task is to write a highly optimized replacement solver (in any language you prefer, though Go is highly recommended for its concurrency patterns) that replicates the constraint satisfaction logic of the legacy tool, but runs significantly faster and produces an equally good or better packing layout.

The constraints are:
1. **Capacity Limit**: The sum of the `size` of all assets in a single bundle must not exceed 10,000.
2. **Conflict Limit**: No two assets in the same bundle can have the same `category` value.

The input file will be provided at `/home/user/assets.json`. Its structure is:
```json
[
  {"id": "asset_001", "size": 450, "category": 12},
  {"id": "asset_002", "size": 1200, "category": 5}
]
```

Your program must write the optimized bundle configuration to `/home/user/optimized_bundles.json`. The output must be a JSON array of arrays, where each inner array contains the `id` strings of the assets assigned to that bundle:
```json
[
  ["asset_001", "asset_005"],
  ["asset_002"]
]
```

You can reverse-engineer or black-box test `/app/legacy_packer` (which acts as an oracle) to understand its baseline performance. 

To complete the task:
1. Write and run your solver to produce `/home/user/optimized_bundles.json`.
2. Set up a local reverse proxy (e.g., using Nginx or a custom Go proxy) listening on port 8080. When a `GET /latest_build` request is made to the proxy, it must serve the contents of `/home/user/optimized_bundles.json` from a backend static file server.

An automated verifier will pull your results via the proxy, validate all constraints, and score your packing efficiency based on the total number of bundles used. You must minimize the number of bundles.