**URGENT: 3AM PAGE - AUDIO PIPELINE OUTAGE**

Hey, wake up. We're getting blasted with customer complaints. The real-time noise suppression service is currently outputting garbage audio (loud static and clipping). It looks like the adaptive filter algorithm is failing to converge, but this was working fine yesterday. 

Here is what we know:
- The codebase for the noise suppression filter is in the Git repository at `/home/user/noise-filter`.
- We have captured a snippet of the problematic raw audio at `/app/noisy_input.wav`.
- The binary processes audio using a standard LMS (Least Mean Squares) adaptive filter.
- There have been multiple commits pushed to the `main` branch by the junior team over the last 48 hours. 

Your tasks:
1. Identify the regression. You need to find the specific commit that broke the convergence of the adaptive filter.
2. Debug the C code. Use `gdb` or your preferred interactive debugger to inspect the memory and convergence states. We suspect a memory corruption or floating-point instability during the weight update phase.
3. Fix the algorithm. Patch the C code so that the filter converges properly again.
4. Compile the fixed binary and process the `/app/noisy_input.wav` file.
5. Save the processed, clean output to `/home/user/fixed_output.wav` (must be a 16-bit PCM WAV file, matching the input format).

This is a critical path. Please ensure your final output is fully fixed. We will evaluate the quality of `/home/user/fixed_output.wav` using an automated Mean Squared Error (MSE) metric against our reference clean audio.