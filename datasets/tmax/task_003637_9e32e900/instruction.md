You are acting as a penetration tester and security engineer. We have intercepted an unencrypted VoIP transmission containing highly sensitive authentication material (a spoken password), but we need to properly redact it before including it in our audit report. 

An automated auditing service is running somewhere on the local host (between ports 8000 and 8100). 
Your task is to:
1. Scan the local host to locate the running HTTP auditing service.
2. Inspect the service. You will need to interact with it to retrieve the audit logs. The service expects a specific HTTP cookie to grant access (you can discover this by examining the service's initial responses or headers).
3. Once authenticated, the service will return an encoded payload containing the exact sample indices (start and end) where the sensitive data occurs in the audio file. Decode this payload (it may use multiple layers of standard encoding).
4. The intercepted audio file is located at `/app/intercept.wav` (it is a standard 16-bit PCM Mono WAV file).
5. Write a **C program** from scratch that reads `/app/intercept.wav`, redacts the sensitive portion by zeroing out (muting) the audio samples between the discovered start and end indices, and writes the resulting WAV file to `/home/user/clean_audio.wav`. 

Requirements for the C program:
- It must be written in C.
- It must correctly parse and preserve the standard 44-byte WAV header.
- The audio data is 16-bit integer PCM. Muting means setting the sample values to 0.

Your final output must be the correctly redacted WAV file located exactly at `/home/user/clean_audio.wav`. An automated verification script will compute the Mean Squared Error (MSE) between your output and a perfectly redacted reference file. Your output must achieve an MSE of less than 0.1.