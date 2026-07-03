You are tasked with fixing a non-reproducible scientific simulation, analyzing its output, and exposing the results via a web service. 

We have a C simulation (`/home/user/sim.c`) that generates a damped sine wave signal using OpenMP and saves the result to an HDF5 file. It also computes the total "energy" (sum of absolute values of the signal array). However, the researcher noticed that the total energy printed and saved by the simulation changes slightly between runs due to the non-deterministic floating-point reduction order caused by OpenMP thread scheduling.

Your workflow:
1. **Extract Parameters:** There is an image at `/app/params.png` containing the simulation parameters (base frequency and decay rate). Extract these parameters (using OCR, e.g., `tesseract`). 
2. **Fix the Simulation:** Edit `/home/user/sim.c` to make the energy sum perfectly deterministic and reproducible across runs, regardless of thread count or scheduling. (For example, allocate a thread-local sum array or perform the sum sequentially after the parallel signal generation). 
3. **Compile:** Compile the fixed C code into an executable named `/home/user/run_sim`. You will need to link OpenMP, HDF5, and the Math library.
4. **Run Simulation:** Run `./run_sim <F0> <DECAY>` using the values extracted from the image. This will generate `signal.h5`.
5. **Spectral Analysis:** Write a Python script to read the `signal` dataset from `signal.h5`. The simulation simulates 10,000 points with a time step of `dt = 0.001` seconds. Perform an FFT on the signal to find the dominant frequency (the positive frequency with the highest magnitude).
6. **Serve Results:** Create a web server (e.g., using Python's `http.server`, `Flask`, or `FastAPI`) listening on `0.0.0.0:8080`. It must expose an HTTP GET endpoint at `/api/report` that returns a JSON response with the following format:
   ```json
   {
     "energy": <deterministic_total_energy_float>,
     "dominant_freq": <dominant_frequency_float>
   }
   ```

Keep this web server running in the foreground as your final command so that our automated verifier can query the endpoint.