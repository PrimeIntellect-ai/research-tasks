You are a data scientist fitting a 1D thermal diffusion model. We have a multi-service architecture running locally to manage the simulation data, but it requires setup, and the core optimization routine needs to be implemented in C for performance.

Your objectives:

1. **Service Configuration:**
   We have two services defined in `/app/services/`:
   - A Redis instance (port 6379)
   - A Python Flask API (port 8080) in `/app/services/api`
   The startup script `/app/start_services.sh` launches both. However, the Python API cannot connect to Redis because it lacks the proper environment configuration. Find the API's configuration file in `/app/services/api` and set the Redis host correctly so it connects to the local Redis instance. Restart the services if necessary so they are both fully functional.

2. **Library Compilation:**
   We have a custom scientific routine library in `/app/libthermal/`. Compile the C files in this directory into a shared library named `libthermal.so` in `/app/libthermal/`. This library provides a critical function: `int get_diffusion_rate(void);` which you will need.

3. **Core Mesh Optimization Routine (C):**
   Write a C program at `/app/mesh_step.c` and compile it to an executable named `/app/mesh_step`. It must link against your compiled `libthermal.so`.
   The program must read from standard input:
   - An integer `N` ($5 \le N \le 1000$), representing the number of nodes in the 1D mesh.
   - A sequence of `N` integers representing the current temperatures at each node.
   
   It must output a single line of `N` space-separated integers representing the temperatures after one time-step of diffusion.
   The update rule for an interior node $i$ (where $0 < i < N-1$) is:
   `V_new[i] = V[i] + (V[i-1] - 2*V[i] + V[i+1]) / K`
   where `K` is the integer returned by `get_diffusion_rate()`. Use standard integer division for the calculation.
   The boundary nodes ($i=0$ and $i=N-1$) must remain unchanged.
   
   *Note:* Your compiled `/app/mesh_step` binary must behave *exactly* (bit-for-bit) like our reference implementation.

4. **Integration:**
   Once your binary is working, write a shell script `/app/fit.sh` that:
   - Fetches the initial array of temperatures by making a GET request to `http://127.0.0.1:8080/init` (this returns `N` followed by `N` integers).
   - Pipes this array through your `/app/mesh_step` program exactly **5** times iteratively (the output of step 1 is the input to step 2, etc.).
   - Posts the final array (just the `N` integers as raw text) back to `http://127.0.0.1:8080/submit` using a POST request.

Ensure all files are created exactly at the specified paths.