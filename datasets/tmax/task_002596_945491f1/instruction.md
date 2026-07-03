You are a security researcher analyzing a suspicious audio-processing service written in Rust. We have captured a strange audio artifact `/app/intercepted_comms.wav`. 

Our intelligence indicates this audio file contains spoken instructions (a sequence of words) that act as an authentication token for a hidden backdoor in the service. You need to transcribe the audio to recover this secret phrase.

Furthermore, we have the source code for the service in a Git repository located at `/home/user/repo/audio-svc`. Recently, the service has been failing to process certain requests, getting stuck in an infinite loop (a convergence failure in its iterative smoothing algorithm). 

Your objectives are:
1. **Transcribe the Audio:** Analyze `/app/intercepted_comms.wav` (you may install and use tools like `whisper.cpp` or `ffmpeg` to process it) to extract the hidden English phrase. Write this exact phrase in lowercase to `/home/user/secret_token.txt`.
2. **Git Bisection:** Use git bisection in `/home/user/repo/audio-svc` to find the exact commit that introduced the convergence failure in the `src/smoothing.rs` module. The bad commit causes the function `smooth_signal` to hang indefinitely on negative inputs. Write the full hash of the offending commit to `/home/user/bad_commit.txt`.
3. **Fix the Bug:** Repair the convergence failure in the latest `master` branch of the Rust code so that `smooth_signal` correctly handles negative inputs by taking their absolute value before processing, ensuring the loop terminates.
4. **Deploy the Service:** Compile and run the fixed Rust service. It must listen on `127.0.0.1:8080`. The service provides an HTTP POST endpoint at `/process` that expects JSON containing `{"token": "<your_transcribed_token>", "data": [-1.0, 2.5, -3.2]}` and returns the smoothed data as JSON `{"result": [...]}`. 

Make sure the service is running in the background and is ready to accept HTTP requests on port 8080.