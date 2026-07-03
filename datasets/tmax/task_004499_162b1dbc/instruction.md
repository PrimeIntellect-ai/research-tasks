You are a bioinformatics analyst managing a sequence processing pipeline. Our system accepts engineered DNA sequences and simulates their expression using a downstream Reaction-Diffusion (PDE) backend. 

Unfortunately, certain "evil" sequences produce parameters that cause our PDE simulator to experience numerical blow-up and crash. We need to implement a pre-screening filter to reject these sequences before they reach the simulation engine, and integrate this filter into our microservice architecture.

### 1. The C++ Filter
Write a C++ program at `/home/user/filter.cpp` and compile it to `/home/user/filter`. 
It must accept a single command-line argument: the path to a text file containing a single DNA sequence (A, C, G, T).

The filter must determine if the sequence is stable ("clean") or unstable ("evil") by calculating parameters and running a rapid ODE convergence test:
*   Calculate $r$ (growth rate) = (Count of 'G' + Count of 'C') / Total length of sequence.
*   Calculate $d$ (decay rate) = (Count of 'A' + Count of 'T') / Total length of sequence.
*   Simulate the following ODE using the Forward Euler method:
    $dy/dt = r \cdot y - d \cdot y^2 + \sin(t)$
*   Use initial condition $y(0) = 0.1$.
*   Use time step $\Delta t = 0.01$.
*   Simulate from $t = 0.0$ to $t = 10.0$.
*   If at any point during the simulation $y(t) > 10.0$, the sequence is numerically unstable ("evil").

**Output requirements:**
*   If the sequence is "clean", the program must exit with code `0`.
*   If the sequence is "evil", the program must exit with code `1`.

### 2. Microservice Integration
The pipeline consists of three services located in `/app/`:
1.  **Nginx Proxy** (Listens on port 8080) - Routes to Flask. Configured via `/app/nginx.conf`.
2.  **Sequence Ingress** (Flask, port 5000) - `/app/flask_app.py`. Receives `POST /submit` with a sequence string, currently forwards blindly to the PDE backend.
3.  **PDE Backend** (C++, port 5001) - A stub `/app/pde_backend.py` (simulating the C++ engine) that crashes on unstable input.

You must modify `/app/flask_app.py` to intercept the sequence string, save it to a temporary file, and invoke your `/home/user/filter` binary. 
*   If the filter exits with `0`, proceed to forward the sequence to the PDE backend.
*   If the filter exits with `1`, the Flask app must immediately return an HTTP 400 response with the text "Unstable sequence rejected".

A startup script `/app/start_services.sh` is provided. Modify files as needed and restart the services using this script to ensure the end-to-end flow works:
`curl -X POST -d "AGCT..." http://localhost:8080/submit` should return 200 for clean sequences and 400 for evil sequences.