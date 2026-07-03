You are acting as a bioinformatics analyst analyzing the fluorescent signal from a novel sequencing-by-synthesis flow cell. We recorded a video of a reaction chamber during a continuous flow phase. 

Your tasks are to extract the signal data, fit it to a biological growth model, and serve the results via an HTTP API written in C.

Step 1: Signal Extraction
You are provided with a video file at `/app/fluor_seq.mp4`. The video runs for exactly 100 frames at 10 frames per second (so frame 0 is t=0.0s, frame 1 is t=0.1s, up to t=9.9s).
Extract the frames and calculate the average grayscale pixel intensity across the *entire image* for each frame. This time-series represents the fluorescent intensity `I(t)`. 

Step 2: ODE Modeling & Fitting
The fluorescent intensity models the concentration of a reporter molecule that follows a standard logistic growth ordinary differential equation:
`dI/dt = r * I(t) * (1 - I(t)/K)`
Where:
- `r` is the growth rate.
- `K` is the carrying capacity (maximum intensity).
- The initial condition `I(0)` is the observed mean intensity of the very first frame (t=0.0s).

You must estimate the parameters `r` and `K` that best fit the empirical data extracted from the video by minimizing the Sum of Squared Errors (SSE). Note: `r` should be within [0.1, 5.0] and `K` within [50, 255].

Step 3: C HTTP Server
Write a C program (`/home/user/server.c`) that implements an HTTP server listening on `0.0.0.0:8050`. It must handle raw TCP connections and parse standard HTTP GET requests to serve the following endpoints:

1. `GET /fit`
   Returns a JSON payload with your fitted parameters rounded to 3 decimal places.
   Example: `{"r": 1.523, "K": 204.102}`

2. `GET /simulate?t=<time_in_seconds>`
   Returns a JSON payload with the simulated intensity `I(t)` at the requested time (e.g., `t=4.5`), based on your fitted parameters. 
   **Integration Requirement:** To compute `I(t)` for this endpoint, your C code MUST numerically integrate the ODE from `t=0` to the requested `t` using the 4th-order Runge-Kutta (RK4) method with a fixed time step of exactly `h = 0.01` seconds.
   Example: `{"I": 120.450}`

Requirements:
- Compile your server to `/home/user/server` (e.g., `gcc server.c -o server -lm`).
- Start the server in the background so it continues running.
- Ensure the server correctly forms HTTP/1.1 200 OK responses with the `Content-Type: application/json` header.
- Do not use external HTTP libraries like `libmicrohttpd`; standard POSIX sockets (`<sys/socket.h>`) must be used.