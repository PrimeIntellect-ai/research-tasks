You need to develop a Python-based simulated Kubernetes Operator that manages system configurations based on Custom Resource manifests.

We are simulating an environment where an operator reads YAML manifests and translates them into system-level bash scripts and configuration files for a host node. 

Your task is to write a Python script at `/home/user/operator.py` that processes all `.yaml` files in the directory `/home/user/manifests/` and generates three configuration files in `/home/user/output/`.

The manifests have the following structure:
```yaml
apiVersion: v1
kind: CustomService
metadata:
  name: <service_name>
spec:
  image: <container_image_url>
  ports:
    - port: <port_number>
      protocol: <tcp_or_udp>
  mounts:
    - source: <host_path>
      destination: <container_path>
      fstype: <fs_type>
```

Your script `/home/user/operator.py` must do the following:
1. Ensure the output directory `/home/user/output/` exists.
2. Clear any existing files in `/home/user/output/` before processing.
3. Parse all `.yaml` files in `/home/user/manifests/`. You may use the `yaml` module (PyYAML is installed).
4. For every mount specified across all manifests, append a standard `fstab` format line to `/home/user/output/fstab.conf`. Use `defaults` for options, `0` for dump, and `0` for pass. 
   Format: `<source> <destination> <fstype> defaults 0 0`
5. For every port specified, append an iptables rule to `/home/user/output/firewall.sh`.
   Format: `iptables -A INPUT -p <protocol> --dport <port> -j ACCEPT`
6. For every manifest, append a container startup command to `/home/user/output/containers.sh`.
   Format: `podman run -d --name <service_name> <image>`
7. Order the entries in all output files alphabetically based on the `<service_name>` of the manifest they originated from. If a single manifest has multiple ports/mounts, output them in the order they appear in the YAML.

Run your script to generate the output files. We will verify the contents of the files in `/home/user/output/`.