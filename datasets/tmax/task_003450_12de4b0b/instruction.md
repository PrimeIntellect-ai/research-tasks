Wake up, you're on call! It's 3:00 AM and the `AeroAcoustics` telemetry decoding service is crashing in production. This service is responsible for decoding and serializing acoustic anomalies from flight data recorders.

The source code for the service is located in `/home/user/aero_service`. 
The proprietary encoded audio log that is causing the crash is located at `/app/blackbox_audio.wav`.

Here is your incident response plan:
1. **Fix the Environment:** The service currently fails to compile. A previous deployment messed up the library paths. Identify the misconfiguration and successfully build the service using `make`.
2. **Diagnose the Crash:** Running the compiled `aero_decoder` binary on `/app/blackbox_audio.wav` results in a Segmentation Fault. Use core dump analysis to identify where the crash occurs.
3. **Isolate the Bug:** The crash is triggered by specific anomalous audio frames that expose a flaw in the custom serialization/encoding logic. Use delta debugging principles to identify the exact conditions causing the memory corruption.
4. **Apply the Fix:** Modify the C++ source code in `/home/user/aero_service` to resolve the encoding/serialization bug (likely a missing bounds check or buffer overflow issue).
5. **Recover the Data:** Recompile and run the service on `/app/blackbox_audio.wav`. The service is designed to output a decoded, reconstructed audio file at `/home/user/output_reconstructed.wav`. 

The final `/home/user/output_reconstructed.wav` must be a valid WAV file. An automated test will measure the Mean Squared Error (MSE) between your reconstructed audio and our clean reference data. Make sure the output is as accurate as possible.