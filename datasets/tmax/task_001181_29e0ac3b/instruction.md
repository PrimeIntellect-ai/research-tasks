You are a performance and scientific computing engineer tasked with profiling and fixing a molecular vibration simulation. The simulation currently produces non-reproducible results across runs due to a floating-point accumulation issue, and you must correct it, validate it against a reference experiment, and wrap it in a robust API.

**Background & Setup:**
1. Create a Python virtual environment in `/home/user/env` and use it for all your work.
2. A reference experiment video is located at `/app/reference_experiment.mp4`. This video records the displacement of a central atom in a test molecular graph. The signal is encoded as the mean grayscale value of the entire frame for each frame in the video. The video was recorded at 60 frames per second (fps).

**Your Objectives:**

1. **Signal Processing (Video to FFT):**
   - Extract the frame-by-frame mean grayscale values from `/app/reference_experiment.mp4`.
   - Perform a spectral analysis (FFT) on this time-series signal to identify the single dominant vibrational frequency of the reference molecule (in Hz).
   - Write this frequency to `/home/user/reference_freq.txt` (just the float value, rounded to 2 decimal places).

2. **Simulation Debugging (Graph Algorithms & Floating-Point Order):**
   - The simulation script `/home/user/sim/vibration_sim.py` models the vibrations of a molecular network using an explicit numerical integration over a graph structure. 
   - Currently, if you run the simulation multiple times with the exact same input, the calculated final dominant frequency slightly fluctuates, and the trajectory diverges over long integration times. This is caused by a non-deterministic reduction order when summing forces from neighboring nodes, leading to floating-point accumulation differences.
   - Fix `/home/user/sim/vibration_sim.py` so that the summation of forces is strictly deterministic, regardless of Python's hash randomization or memory layout. 
   - Verify that your fixed simulation, when run on the default test graph (provided in `/home/user/sim/test_graph.json`), deterministically produces a dominant frequency that closely matches the one you extracted from the video.

3. **Service Deployment:**
   - Wrap the fixed simulation into an HTTP API using a lightweight framework (e.g., FastAPI or Flask).
   - The service must listen on `0.0.0.0:8080`.
   - Implement a `POST` endpoint at `/simulate`.
   - The endpoint will receive a JSON payload representing a molecular graph:
     ```json
     {
       "nodes": [0, 1, 2, 3],
       "edges": [[0, 1], [1, 2], [2, 3], [3, 0]]
     }
     ```
   - The endpoint must return a JSON response containing the calculated dominant frequency:
     ```json
     {
       "dominant_frequency": 4.52
     }
     ```

Keep the service running in the background when you are finished so the automated verification system can test it with several new graph topologies. Do not exit your final process.