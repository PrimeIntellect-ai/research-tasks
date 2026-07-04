We are in the process of migrating our polyglot build system's infrastructure. Currently, we use a proprietary, locally-compiled C++ binary to validate and filter package dependency requests before they are reverse-proxied to external registries (like npm and Go proxy). 

The legacy binary is located at `/app/build_sec_proxy`. It is a stripped binary. 
It takes a single argument: the path to a JSON file containing a serialized batch of dependency requests. It then outputs a JSON string to `stdout` detailing whether the request batch is allowed, rate-limited, or blocked, along with the filtered list of safe dependencies. 

Your task is to write a Go replacement for this tool.
1. You must orchestrate a series of tests to probe `/app/build_sec_proxy` and reverse-engineer its request validation, rate limiting, and deserialization/serialization logic.
2. Based on your findings, write a Go program at `/home/user/build_sec_proxy.go`.
3. Your Go program must take a single command-line argument (a path to a JSON file) and output the exact same JSON response to `stdout` as the legacy binary for any given input.

The input JSON format generally looks like this:
```json
{
  "client_ip": "192.168.1.5",
  "packages": [
    {"name": "express", "version": "4.17.1", "ecosystem": "npm"},
    {"name": "gin", "version": "1.7.0", "ecosystem": "go"}
  ]
}
```

Write the code in `/home/user/build_sec_proxy.go`. Make sure your Go code produces bit-exact equivalent output to the reference C++ binary.