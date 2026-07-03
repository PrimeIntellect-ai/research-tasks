You are an infrastructure engineer automating the provisioning of a custom load balancer for our QEMU VM fleet. Our CI/CD pipeline requires a standalone Go script that can process health-check states and make deterministic routing decisions. 

Unfortunately, our internal vendored copy of the YAML parsing library has been broken by a recent malformed commit, and you need to fix it before you can write the routing script.

Part 1: Fix the Vendored Package
We vendor our dependencies locally. The package `gopkg.in/yaml.v3` is located at `/app/vendor/yaml.v3`. 
A recent commit introduced a deliberate panic in the `Unmarshal` function inside `yaml.go` (around line 95). 
Find the broken code, remove the `panic("TODO: implement")` perturbation, and restore the proper function call to the internal unmarshal logic so the package builds and functions correctly.

Part 2: Write the Routing Decision Script
Create a Go program at `/home/user/lb_decision.go`. 
This program must read a YAML payload from STDIN (using the fixed `/app/vendor/yaml.v3` package) and print the correct routing decision to STDOUT.

The input YAML will have the following structure:
```yaml
request:
  path: "/api/data"
  method: "GET"
vms:
  - id: "qemu-node-1"
    status: "online"
    cpu: 65.5
  - id: "qemu-node-2"
    status: "offline"
    cpu: 10.0
```

Your script must implement the following load balancing and health check logic:
1. Filter out any VMs that do not have `status: "online"`.
2. Filter out any VMs with a `cpu` load greater than or equal to `80.0`.
3. If no VMs remain, your program must print exactly: `503 Service Unavailable`
4. If valid VMs remain, select the one with the lowest `cpu` load.
5. If there is a tie for the lowest `cpu` load, select the VM with the lowest `id` (lexicographically ascending).
6. Print the routed destination exactly as: `ROUTE: <id>`

Requirements:
- Your script must compile successfully using `go build /home/user/lb_decision.go`.
- Make sure to point your `go.mod` to use the local vendored path `/app/vendor/yaml.v3`.
- Do not output anything else to STDOUT besides the final routing decision (e.g. `ROUTE: qemu-node-1`).