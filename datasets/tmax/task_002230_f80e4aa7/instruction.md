You are a deployment engineer tasked with rolling out a secure local media server that automatically processes and hosts compressed audio logs. 

We have a raw audio log located at `/app/input.wav`. You need to set up a pipeline that compresses this file, hosts it securely, and ensures the correct system permissions are applied.

Please complete the following steps:

1. **Audio Processing Application (Rust):**
   Create a Rust project in `/home/user/audiocompress`. Write a Rust program that uses `std::process::Command` to invoke `ffmpeg`. It should convert `/app/input.wav` into an MP3 file at `/home/user/srv/media/output.mp3`. 
   Configure the ffmpeg command to use a constant audio bitrate of `32k` and mix down to mono (`-ac 1`).

2. **Idempotent Setup & Configuration Script:**
   Write a bash script at `/home/user/deploy.sh` that performs the following system administration tasks idempotently (running it multiple times should not cause errors or duplicate config entries):
   - Creates the directories `/home/user/srv/media` and `/home/user/certs`.
   - Generates a self-signed RSA 2048-bit TLS certificate (`cert.pem`) and private key (`key.pem`) in `/home/user/certs/` valid for 365 days.
   - Configures Nginx (which is already installed) to serve the `/home/user/srv/media` directory over HTTPS on port `4433`. The server block should use the generated certificates. Disable HTTP.
   - Uses Access Control Lists (`setfacl`) to grant the `www-data` user read and execute permissions to `/home/user/srv/media` and read access to all files within it, ensuring the web server can read the processed audio.
   - Reloads or restarts the Nginx service to apply changes.

3. **Execution:**
   - Run your `deploy.sh` script to set up the environment.
   - Run your Rust application to process the audio.
   - Test connectivity by ensuring `curl -k https://127.0.0.1:4433/output.mp3` successfully downloads the compressed file.

Our automated verifier will download the audio file via the TLS endpoint and measure the Peak Signal-to-Noise Ratio (PSNR) of your output against the original audio to ensure quality is maintained while file size is reduced.