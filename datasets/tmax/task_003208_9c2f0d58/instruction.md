You are an ML engineer preparing an audio dataset for a specialized voice command recognition model. The recordings were captured using an underwater microphone with a severe, known non-linear distortion profile. 

The raw, distorted audio is located at `/app/distorted_commands.wav` (Sample rate: 16kHz, Mono).

The microphone's transfer function is:
`y[n] = x[n] - 0.15 * (x[n]^3)`
where `x[n]` is the true underlying acoustic pressure (normalized between -1.5 and 1.5) and `y[n]` is the recorded digital signal.

Your task is to:
1. Write a script to load the observational data (`/app/distorted_commands.wav`).
2. Reshape and process the data to recover the true underlying signal `x[n]` for every sample. Because the distortion is non-linear, you will need to solve the nonlinear equation `y = x - 0.15 * x^3` for `x` at each time step. (Hint: you can use numerical methods like Newton-Raphson or analytically solve the cubic equation).
3. Analytically validate your solution: The first 1.0 second of the audio is a pure 1kHz calibration sine wave. After undistortion, this segment should have virtually zero harmonic distortion (i.e., minimal energy at 3kHz compared to the original recorded file). 
4. Save the fully undistorted recovered audio (the entire file, including the calibration tone) to `/home/user/clean_data.wav`. Ensure it is saved as a 16-bit PCM WAV file at the original 16kHz sample rate. Watch out for proper scaling (float to int16) to avoid clipping. The maximum absolute amplitude of the true signal `x[n]` is guaranteed to be $\le 1.0$. Multiply by 32767 before saving to 16-bit PCM.

You may use any programming language you prefer (Python is highly recommended for `scipy`/`numpy` support). You can install any required packages.