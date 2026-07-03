You are a bioinformatics analyst processing a batch of nanopore sequencing data. A field researcher has left an audio recording containing the exact mathematical model and parameters to use for the analysis.

Your task is to:
1. Transcribe the audio file located at `/app/field_notes.wav` to retrieve the analysis parameters and the specific nonlinear equation you need to solve. 
2. Read the scientific data file at `/app/sequence_data.h5`. This HDF5 file contains a dataset at `/nanopore/signal_1` representing a time-series voltage signal sampled at 1000 Hz.
3. Perform a Fourier transform (FFT) on this signal to find its dominant frequency (in Hz). You will use this dominant frequency as the `V_max` parameter in your equation.
4. Solve the nonlinear equation described in the audio note using the `V_max` you discovered and the constants provided in the recording to find the unknown concentration `S`. 
5. Bring up an HTTP API server listening on `0.0.0.0:8000`. 
    - The server must respond to `GET /solution`
    - The response must be a JSON payload in the format: `{"S": <float_value>}` where `<float_value>` is your solved concentration rounded to 3 decimal places.
    - The server must run continuously in the background so it can be queried by our verification systems.

Ensure your server is running and accessible before you consider the task complete. You may use any language (e.g., Python with `h5py`, `numpy`, `scipy`, and `flask` or standard HTTP libraries) to perform the analysis and host the service.