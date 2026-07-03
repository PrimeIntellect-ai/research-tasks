You are a build engineer managing an artifact registry. We are migrating our internal artifact index to a new schema version, and we need to ensure that dependency resolution still works correctly with the new format.

Currently, we have a legacy index file located at `/home/user/legacy_index.json` with the following structure:
```json
{
  "packages": {
    "lib-alpha": { "v": "1.0", "deps": ["lib-beta", "lib-gamma"] },
    "lib-beta": { "v": "2.2", "deps": ["lib-delta"] },
    "lib-gamma": { "v": "1.1", "deps": [] },
    "lib-delta": { "v": "3.0", "deps": ["lib-gamma"] },
    "lib-core": { "v": "0.9", "deps": ["lib-alpha", "lib-epsilon"] },
    "lib-epsilon": { "v": "4.1", "deps": [] }
  }
}
```

Your task consists of two parts:

1. **Schema Migration**: Write a script (or use shell tools) to transform `/home/user/legacy_index.json` into a new file `/home/user/v2_index.json`. The new schema must be structured as a list of objects under an `artifacts` key, like this:
```json
{
  "artifacts": [
    {
      "name": "lib-alpha",
      "version": "1.0",
      "dependencies": ["lib-beta", "lib-gamma"]
    }
    // ... all other packages
  ]
}
```

2. **Graph Traversal & Test Fixture**: To verify the new schema, write a test script in any language (e.g., Python, Node.js) that reads `/home/user/v2_index.json`. The script must compute the complete, deduplicated set of transitive dependencies for the artifact named `lib-core`. 
The script must output the resolved transitive dependencies (excluding `lib-core` itself), sorted alphabetically, one per line, to the file `/home/user/transitive_deps.log`.

Requirements:
- Do not modify `/home/user/legacy_index.json`.
- The transformed JSON in `/home/user/v2_index.json` must be valid JSON.
- The output file `/home/user/transitive_deps.log` must contain exactly the names of the dependencies, sorted alphabetically, separated by newlines.