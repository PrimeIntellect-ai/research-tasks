You are a deployment engineer tasked with automating the rollout of a new Rust-based audio processing service. You need to set up a git-based rolling deployment system, implement the audio processing logic, and deploy the service.

Here are your instructions:

1. **Environment Setup & Git Configuration:**
   - Create a bare Git repository at `/home/user/audio_service.git`.
   - Configure a `post-receive` hook in this repository. The hook must:
     a) Extract the latest pushed commit into a new deployment directory located at `/home/user/releases/release_<commit_hash>`.
     b) Compile the Rust project in that directory using `cargo build --release`.
     c) Perform a health check: run the newly built binary, piping the contents of the provided audio fixture `/app/voice_record.wav` into its standard input, and redirecting standard output to `/dev/null`. If the binary crashes or returns a non-zero exit code, the hook must abort the deployment and exit with a non-zero code.
     d) If the health check passes, atomically update a symlink at `/home/user/releases/current` to point to this new release directory (`/home/user/releases/release_<commit_hash>`).

2. **Implement the Audio Processing Service:**
   - On your local workspace (e.g., `/home/user/workspace`), initialize a new Rust binary project.
   - The Rust application must read binary data from `stdin` until EOF, apply a specific byte-level transformation, and write the result to `stdout`.
   - **Transformation Logic:** For every byte read, perform a bitwise Right Rotate by 3 bits, and then apply a bitwise XOR with `0x8C`.
   - The application must exit with code `0` on success.

3. **Deployment:**
   - Commit your Rust project to your workspace repository.
   - Add the bare repository `/home/user/audio_service.git` as a remote.
   - Push your code to the bare repository to trigger the deployment.
   - Ensure the hook executes successfully, the health check passes using the `/app/voice_record.wav` fixture, and the symlink `/home/user/releases/current` correctly points to the deployed version containing the built binary at `target/release/audio_service`.

Ensure your deployment script uses standard shell commands and properly handles directory creation. The automated verifier will aggressively fuzz your deployed executable at `/home/user/releases/current/target/release/audio_service` to ensure it is bit-exact equivalent to a reference implementation.