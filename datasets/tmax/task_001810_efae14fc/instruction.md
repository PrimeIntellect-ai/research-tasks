You are a performance engineer tasked with debugging and finalizing a scientific profiling tool. 

We are monitoring a chemical reactor's vibrations via a high-speed camera. The raw footage is located at `/app/reactor_vibration.mp4` (video is exactly 60 FPS). 

Your predecessor started writing a Rust application to process this video, extract the vibration signal, run a Fast Fourier Transform (FFT) to find the dominant resonant frequency, and save the data to an HDF5 file. However, the current implementation (if any) or your new implementation must handle this efficiently and deterministically.

Your task:
1. Create or fix a Rust project in `/home/user/vibration_analyzer`.
2. The application must process `/app/reactor_vibration.mp4`. For *each frame* in order, compute the mean grayscale intensity of the top-left 100x100 pixel region (x: 0 to 99, y: 0 to 99). Note: Convert RGB to grayscale using the standard Rec. 601 Luma formula: `Y = 0.299*R + 0.587*G + 0.114*B` before averaging.
3. Collect this mean intensity for all frames to form a 1D time-series signal. 
4. Perform an FFT on this time-series to compute the amplitude spectrum.
5. Identify the dominant resonant frequency (in Hz). (Ignore the DC component / 0 Hz peak).
6. Save the results into an HDF5 file at `/home/user/analysis.h5`. The HDF5 file must contain:
   - A dataset named `time_series` (1D array of f64, the mean intensities).
   - A dataset named `dominant_frequency` (scalar f64, the found frequency in Hz).

**Crucial Profiling Constraint:**
Floating-point reduction order matters. Your time-series extraction and FFT must be 100% deterministic and numerically stable. We will evaluate your solution using an automated metric verifier that compares your `dominant_frequency` to the exact theoretical frequency of the video's underlying simulation.

Requirements:
- You may use any Rust crates you need (e.g., `ffmpeg-next`, `rustfft`, `hdf5`, `image`).
- Make sure necessary system dependencies (like `libhdf5-dev`, `ffmpeg`, etc.) are installed.
- Compile and run your code so that `/home/user/analysis.h5` is generated.