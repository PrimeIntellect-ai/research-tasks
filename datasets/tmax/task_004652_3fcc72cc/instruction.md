You are an AI assistant helping a machine learning engineer prepare an automated feature extraction pipeline for video data. We need a lightweight microservice that reads frames from an experimental video, performs array manipulations to isolate the region of interest, and simulates a physical decay process based on the frame's initial state using an Ordinary Differential Equation (ODE).

Your task is to implement this service. 

Requirements:
1. **Video Source:** The video is located at `/app/experiment.mp4`.
2. **Bash Web Server:** Write a Bash script at `/home/user/server.sh` that acts as an HTTP server listening on port `8080`. You may use `nc` (netcat) or `socat` to handle the socket connections. The script must remain running and handle incoming requests.
3. **Endpoint:** The server must accept requests of the form: `GET /feature?frame=<N>&rtol=<R> HTTP/1.1` where `<N>` is an integer frame index (0-indexed) and `<R>` is a float representing the relative tolerance for the ODE solver.
4. **Data Processing:** For each request, the server should (likely by calling a helper Python script):
   - Extract the exact frame `<N>` from the video.
   - Convert the frame to grayscale.
   - Perform a multi-dimensional array manipulation to crop out the central 50% of the image (i.e., remove the outer 25% from the top, bottom, left, and right borders).
   - Calculate the mean pixel intensity of this central cropped region. Let this value be $V$ (a float).
5. **ODE Simulation:** Treat $V$ as the initial condition $x(0) = V$ for the following ODE:
   $$ \frac{dx}{dt} = -0.05x + 10e^{-t} $$
   Solve this ODE from $t=0$ to $t=5.0$. You must use a numerical ODE solver (e.g., `scipy.integrate.solve_ivp` in Python) and pass the requested `<R>` as the relative tolerance (`rtol`). Set the absolute tolerance (`atol`) to `1e-6`.
6. **Response:** The HTTP response must be a valid HTTP `200 OK` response. The response body must contain *only* the final evaluated value of $x(5.0)$, rounded to exactly 4 decimal places (e.g., `123.4567`).

Start the server in the background once it is ready so it can be tested. Make sure your bash script gracefully extracts the query parameters from the raw HTTP GET request.