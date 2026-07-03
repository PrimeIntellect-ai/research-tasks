You are a FinOps analyst tasked with optimizing our cloud infrastructure and storage costs. We have a massive archive of raw audio recordings from our call center that we need to compress heavily to save on S3 costs, while retaining enough quality for automated transcription. Furthermore, we are migrating the transcription processing to lightweight QEMU virtual machines.

You need to complete the following objectives:

1. **Audio Compression Optimization**: 
   You will find a sample raw audio file at `/app/recording.wav`. Compress this file into an Ogg Opus format at `/home/user/recording.opus`. 
   - Your goal is to aggressively reduce the file size (to save cloud storage costs) while maintaining speech intelligibility. 
   - Our automated verification will transcribe your `.opus` file using Whisper and compute the Word Error Rate (WER) against the ground truth.
   - You must achieve a file size reduction ratio (opus_size / wav_size) of **<= 0.10**, while maintaining a WER of **<= 0.15**.

2. **Transcription & VM Setup Requirements**:
   The audio file `/app/recording.wav` contains a voicemail from the Lead Architect detailing the precise specifications for the new lightweight transcription VMs. 
   - Listen to or transcribe `/app/recording.wav` (you can use `ffmpeg`, `whisper-cli`, or python to transcribe it locally) to extract the required **RAM size**, **disk size**, and a **specific SSH security rule** mentioned in the message.
   - Create a script at `/home/user/setup_node.sh` (make it executable).
   - The script must take one argument: the VM instance name.
   - When run, the script must:
     a) Export an environment variable `QEMU_VM_NAME` set to the provided instance name.
     b) Generate a QEMU `qcow2` disk image named `<instance_name>.qcow2` with the exact disk size specified in the audio.
     c) Generate a `cloud-init` user-data file named `<instance_name>_user-data` that configures the SSH daemon to implement the specific SSH security rule mentioned in the audio (which silently rejects key-based login).
     d) Print the final `qemu-system-x86_64` command line required to launch the VM with the specified RAM size, the created disk image, and no graphical interface (headless).

Use only standard Linux tools and Bash. You may install standard Ubuntu packages (like `ffmpeg`, `opus-tools`, `qemu-utils`) if needed.