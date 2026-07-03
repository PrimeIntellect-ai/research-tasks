You are managing a custom Kubernetes-like deployment system. There is a local daemon called `deployer-daemon` that manages container lifecycle and virtualization via QEMU. It reads JSON manifests to deploy applications. 

Currently, developers are submitting manifests with the `:latest` image tag, and without the required VNC sidecar for remote VM debugging. 

Your task is to write a Go CLI tool that mutates these JSON manifests, and then configure the `deployer-daemon` to use your tool in its pipeline.

Step 1: Write the Mutator in Go
Create a Go program at `/home/user/mutator.go` and compile it to an executable at `/home/user/mutator`.
The program must read JSON from `stdin` and write JSON to `stdout`.
The JSON will represent a resource. The program must apply the following rules:
1. Parse the incoming JSON.
2. If the `"kind"` field equals exactly `"Pod"`, inspect the `spec.containers` array.
3. For any container in that array where the `"image"` string ends with `:latest`, replace the `:latest` suffix with `:staged`.
4. If the `"kind"` field equals `"Pod"`, append a new container object to the `spec.containers` array exactly like this: `{"name": "qemu-vnc", "image": "localhost:5000/qemu-vnc:1.0"}`.
5. If the `"kind"` is NOT `"Pod"`, do not modify the JSON structure.
6. Output the resulting JSON on `stdout`. It must be valid JSON, minified (no extra whitespace, tabs, or newlines).

Step 2: Configure the Pipeline
The `deployer-daemon` uses an environment file located at `/home/user/deployer.env`.
Currently, it contains:
`FILTER_CMD=""`
Modify `/home/user/deployer.env` to set `FILTER_CMD="/home/user/mutator"`.

Finally, restart the deployer service by touching the reload trigger file: `touch /home/user/deployer.reload`.

Ensure your Go program handles arbitrary JSON cleanly without crashing, modifying only what is specified.