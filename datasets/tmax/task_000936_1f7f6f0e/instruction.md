You are a container specialist tasked with fixing a broken load balancer configuration pipeline for our microservices architecture. 

Currently, our configuration automation is failing. The script that generates the base configuration is writing to the wrong location due to an environment issue, and we are completely missing the dynamic backend ports because the legacy service requires interactive authentication to reveal its port.

Your objective is to fix the pipeline, extract the correct active ports, and generate a final HAProxy configuration file.

Here are the details of your environment located in `/home/user/microservices/`:

1. **Base Configuration Generator**: 
   There is a script at `/home/user/microservices/generate_base.py`. It is currently misconfigured. When run without the correct environment variables, it defaults to writing its output to `/tmp/base.cfg`. You must determine what environment variable it expects to write its output to `/home/user/microservices/lb/haproxy.cfg`, and execute it correctly so the base configuration is placed there.

2. **Standard Microservices**:
   The status of our modern containerized microservices is logged in `/home/user/microservices/registry.txt`. You need to use text processing tools to extract only the names and ports of the services whose status is exactly `UP`.

3. **Legacy Microservice**:
   We have a legacy microservice that does not write to the registry. Instead, it listens on a Unix domain socket at `/home/user/microservices/legacy.sock`. 
   To get its current port, you must interact with this socket. When you connect, it will prompt: `Enter PIN: `. You must provide the PIN `8472` and press Enter. It will then respond with `Backend port is <PORT>`. You must write a Python script using the `pexpect` module (or standard socket interaction) to automate this and extract the port.

4. **Final Assembly**:
   Append a backend definition block to the `/home/user/microservices/lb/haproxy.cfg` file you generated in step 1. The appended block must EXACTLY follow this format:
   ```
   backend web_cluster
       server <service_name> 127.0.0.1:<port>
       # ... (one line for each UP service from the registry)
       server legacy 127.0.0.1:<legacy_port>
   ```
   *Note: Ensure the standard services are listed in the order they appear in `registry.txt`, followed by the legacy service.*

Complete the configuration file correctly. All paths must be absolute.