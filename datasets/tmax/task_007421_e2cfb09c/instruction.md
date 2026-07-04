You are a container specialist managing a lightweight local microservice deployment. We have a custom Python-based process supervisor that starts our services defined in `/home/user/services.json`. However, it currently has a bug: it launches all services simultaneously. The backend service frequently crashes because it tries to connect to the database mock before the database port is actually open.

Additionally, we need to expose the backend service on a public-facing port using user-space port forwarding, as we do not have root access to configure iptables.

Your tasks are:

1. **Fix the Supervisor Script**:
   Modify the existing Python script at `/home/user/supervisor.py`. Update it so that if a service definition in `/home/user/services.json` contains a `depends_on_port` key, the supervisor will actively poll that local port (using a TCP socket) and wait until it is accepting connections BEFORE launching the dependent service process.

2. **Construct the Backend Service**:
   Write a Python script at `/home/user/backend.py` that starts a simple HTTP web server on `127.0.0.1` port `9000`. 
   - When it receives a GET request, it must respond with the exact text `SYSTEM_OK` and a 200 status code.
   - It must run continuously until terminated.
   - It must print `Backend service listening on 9000` to standard output immediately upon successful binding.

3. **Configure User-Space Port Forwarding**:
   Use `socat` to create a background process that listens on `127.0.0.1` port `8080` and forwards all incoming TCP connections to the backend service on `127.0.0.1` port `9000`. Save the exact `socat` command you used as a single line in `/home/user/port_forward.sh` and make the script executable. 
   *(Note: You must actually run this `socat` command or script in the background to fulfill the routing requirement).*

4. **Execute and Log**:
   Run your fixed `supervisor.py` script. The supervisor is configured to launch `db_mock.py` (which takes a few seconds to bind to port 5432) and your `backend.py`. 
   Redirect the entire standard output of `supervisor.py` to `/home/user/startup.log`.

**Verification:**
To succeed, `/home/user/startup.log` must show that the database mock bound to its port *before* the backend service was launched. Furthermore, an HTTP GET request to `http://127.0.0.1:8080/` must return `SYSTEM_OK`.