You are an edge computing engineer tasked with restoring the telemetry processing pipeline on an offline IoT device. The previous engineer left abruptly, and the source code for the telemetry processor was lost. However, they left a voice memo detailing the system configuration and the exact algorithm used for the telemetry data transformation.

Your objectives are as follows:

1. **Extract the Specifications:**
   An audio file is located at `/app/voicemail.wav`. You must transcribe this audio to recover the system specifications. A pre-compiled version of Whisper is available on the system at `/opt/whisper/main` with the base English model located at `/opt/whisper/models/ggml-base.en.bin` to assist you in transcribing the file without needing internet access.

2. **Recreate the Directory Structure:**
   Based on the instructions in the voicemail, recreate the exact directory structure and symlinks required by the edge spooling system. All directories should be created within `/home/user/`.

3. **Rebuild the Telemetry Processor:**
   Based on the algorithm rules dictated in the voicemail, write a Python 3 script at `/home/user/telemetry_processor.py`. 
   - The script must read a single line of string input from standard input (`stdin`).
   - It must apply the precise sequence of transformations described in the audio.
   - It must print the final transformed string to standard output (`stdout`) and exit.
   - Make sure the script is executable.

The automated verification system will test your script's correctness by blasting it with thousands of random inputs and comparing its standard output bit-for-bit against a restored reference binary. It will also verify your connectivity diagnostic directory structure.