You are an ML engineer preparing training data for a biological sequence alignment model. As part of this, you need to extract and analyze binding kinetics from an experimental video.

The video artefact is located at `/app/binding_kinetics.mp4`. It shows a time-lapse of a fluorescent biosensor reacting to a DNA primer over time. 

Your tasks are:
1. **Frame Extraction**: Extract all frames from `/app/binding_kinetics.mp4`.
2. **Signal Generation**: Compute the average grayscale pixel intensity for each frame. This sequence of average intensities forms your time-series signal.
3. **Spectral Analysis & Deterministic Variance**: Write a C program (`/home/user/analyze.c`) that:
   - Computes the Discrete Fourier Transform (DFT) of the time-series signal. Find the dominant frequency (the index of the maximum magnitude in the power spectrum, excluding the DC component at index 0).
   - Computes the population variance of the signal. In the past, floating-point reduction order variations caused non-reproducible training data. To fix this, you *must* implement **Kahan summation** in double precision to calculate the sum of the intensities (to find the mean) and the sum of the squared differences from the mean (to find the variance).
4. **Service Integration**: The C program must also act as a TCP server listening on `127.0.0.1:9090`. 
   - When a client connects and sends the exact string `"GET_METRICS\n"`, the server must compute the metrics and respond with a comma-separated string: `<dominant_freq_index>,<variance_rounded_to_6_decimal_places>\n`.
   - Close the connection after responding.
   - The server must handle multiple sequential requests without crashing.

Compile your C program, start it in the background, and ensure it is listening on port 9090. Do not kill the server; the verification suite will connect to it.

Note:
- You may use standard tools like `ffmpeg` to extract frames.
- Use `gcc` to compile your C program. Standard libraries are fine (e.g., `<math.h>`, `<sys/socket.h>`, etc.).
- Population variance is $\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2$.