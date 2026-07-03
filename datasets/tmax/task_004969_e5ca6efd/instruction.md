You are a machine learning engineer preparing a multimodal training dataset that maps protein structures to acoustic sonifications. 

You have been provided with two input files:
1. `/app/molecule.pdb`: A Protein Data Bank (PDB) file.
2. `/app/vibration.wav`: An audio file containing the synthesized vibration signal of the molecule.

Your task is to extract specific features from these files and serve them via a lightweight HTTP API orchestrated by a Bash script. 

Specifically, you must write a Bash script at `/home/user/start_server.sh` that does the following:
1. Computes the `atom_count`: The exact number of lines starting with the exact word `ATOM` (uppercase) in `/app/molecule.pdb`.
2. Computes the `peak_frequency_hz`: The dominant (peak) frequency in Hertz of the `/app/vibration.wav` file using a Fast Fourier Transform (FFT) or spectral analysis. Round this value to the nearest integer.
3. Starts a network service listening on `127.0.0.1:8080`.
4. Whenever an HTTP `GET` request is made to the `/features` endpoint, the service must return an `HTTP/1.1 200 OK` response with a `Content-Type: application/json` header and a JSON body formatted exactly like this:
   `{"peak_frequency_hz": <freq>, "atom_count": <count>}`

Requirements:
- Your script `/home/user/start_server.sh` must be executable (`chmod +x`).
- You may use any standard Linux tools (e.g., `awk`, `grep`, `socat`, `nc`, `python3` for FFT/HTTP serving) as long as the entry point and orchestration is handled by your Bash script.
- The server must be able to handle multiple sequential requests (it should not crash or exit after the first request).
- Start the server in the background or leave it running so the automated tests can query it.