You are a security researcher analyzing artifacts left by a suspicious steganography malware. The malware captured frames from a local surveillance feed, injected a mathematically generated noise pattern into specific frames, and exfiltrated the corrupted data over the network. 

You have been provided with the following artifacts:
1. `/app/surveillance.mp4`: The raw, uncorrupted surveillance video feed captured prior to the malware's modifications.
2. `/app/traffic.pcap`: A network packet capture containing the exfiltrated payloads. The malware sent out UDP packets to port 1337. Each packet payload contains a 4-byte integer (frame index, little-endian) followed by the corrupted grayscale pixel data (flattened 64x64 float32 array) of the center crop of that frame.
3. `/app/memory.dmp`: A raw memory dump of the malware process. The malware uses a fixed 64x64 float32 noise matrix to corrupt the frames. This exact 16,384-byte block of data is stored sequentially in the memory dump, immediately following the magic string signature `NOISE_SEED_V1_8899`.
4. `/home/user/analysis_env`: A directory containing a partially written Python tool that you need to use. However, its `requirements.txt` has conflicting dependencies (e.g., incompatible versions of `scapy`, `numpy`, and `opencv-python` that fail to install together).

Your task:
1. Resolve the dependency conflicts in `/home/user/analysis_env/requirements.txt` so that the required libraries can be installed in a virtual environment.
2. Extract the 64x64 float32 noise matrix from `/app/memory.dmp`.
3. Parse the UDP payloads from `/app/traffic.pcap` to recover the frame indices and the corrupted 64x64 center crops.
4. Extract the exact center 64x64 crop of the corresponding frames from `/app/surveillance.mp4` (converted to grayscale, normalized to 0.0 - 1.0 floats).
5. The malware generated the corrupted payload using the formula: `Corrupted = (Original_Crop * 0.5) + (Noise_Matrix * 0.5)`. 
6. Your goal is to reverse this mathematical operation to perfectly reconstruct the original `Noise_Matrix` using the data from the pcap and the clean video. Because of floating-point inaccuracies, you should calculate the reconstructed noise matrix for every exfiltrated frame and compute the element-wise average of all reconstructed matrices to get the highest accuracy prediction.
7. Save your final averaged 64x64 float32 noise matrix to `/home/user/reconstructed_noise.npy` using `numpy.save`.

Ensure your final output is strictly a 64x64 numpy array saved to `/home/user/reconstructed_noise.npy`. The automated testing suite will evaluate your result by calculating the Mean Squared Error (MSE) between your reconstructed matrix and the true noise matrix.