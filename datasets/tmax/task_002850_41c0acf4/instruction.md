You are assisting a computational physics researcher in analyzing acoustic emission data to drive an adaptive mesh refinement simulation. 

Your objective is to build and start a local HTTP API service that processes experimental data, computes statistical density estimates, and serves as a backend for the simulation's regression test suite.

Here are the requirements:

1. **Acoustic Signal Processing**:
   There is an audio file located at `/app/signal.wav` containing an acoustic emission recording. The signal consists of three distinct dominant frequency tones mixed together. 
   You must analyze this audio file (e.g., using Fast Fourier Transform) to find the three peak frequencies (in Hz). Round the frequencies to the nearest integer.

2. **Density Estimation for Mesh Refinement**:
   There is a dataset of spatial particle coordinates at `/home/user/samples.csv` (one value per line, representing 1D positions).
   You must fit a Gaussian Kernel Density Estimate (KDE) to this data using Scott's Rule for the bandwidth estimator. This KDE represents the "mesh refinement weighting function".

3. **HTTP Service**:
   Create and run an HTTP service listening exactly on `127.0.0.1:8080`. The service must implement the following endpoints:
   - `GET /audio_peaks`: Returns a JSON response `{"peaks": [f1, f2, f3]}` where `f1, f2, f3` are the three peak frequencies found in the audio file, sorted in ascending order.
   - `GET /mesh_density`: Evaluates your Gaussian KDE at exactly 9 points: x = 10, 20, 30, 40, 50, 60, 70, 80, 90. Returns a JSON response `{"density": [d10, d20, ..., d90]}`.

4. **Regression Test**:
   Write a scientific code regression test script at `/home/user/test_api.py` that queries your running service and asserts that the HTTP status codes are 200 and the JSON keys exist. You do not need to run this script yourself, but it must be valid and executable.

5. **Visualization**:
   Create a script `/home/user/plot_data.py` that reads the audio file and the CSV, generates a 2-panel plot (top: audio waveform, bottom: KDE density curve from x=0 to x=100), and saves it to `/home/user/experiment_viz.png`.

Leave the HTTP service running in the background on port 8080 so that our automated verification suite can query it.