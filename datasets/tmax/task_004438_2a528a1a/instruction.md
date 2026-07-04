You are assisting a researcher in organizing a large-scale audio dataset. To distribute the audio files across different storage buckets efficiently, the researcher relies on a "routing model" that maps basic audio features to a specific storage shard. 

Currently, the researcher is using a legacy, black-box compiled tool located at `/app/oracle_router`. This tool takes exactly three integer arguments—representing an audio file's extracted "embedding" (Sample Rate, Channels, and Duration in Seconds)—and outputs the name of the storage bucket. 

Your task is to modernize this workflow using pure Bash:

1. **Model Reconstruction:** Reverse-engineer the routing logic of `/app/oracle_router`. It implements a simple decision tree with some modulo arithmetic based on its three inputs. Write a pure Bash replacement script at `/home/user/router.sh` that takes three integer arguments (`$1`, `$2`, `$3`) and prints the exact same bucket name as the oracle for *any* valid input combination. 
   - Valid inputs: `$1` (Sample Rate) ranges from 8000 to 48000. `$2` (Channels) is either 1 or 2. `$3` (Duration) ranges from 1 to 1000.

2. **Feature Extraction:** Write a script `/home/user/extract.sh` that takes a single argument (the path to an audio file) and extracts its embedding using `ffprobe`. It must output exactly three space-separated integers: `<sample_rate> <channels> <duration_rounded_down_to_nearest_integer>`.

3. **Storage Integration:** We have a new incoming audio sample at `/app/recording.wav`. Process this file using your `extract.sh` script, feed the resulting embedding into your `router.sh` script to get the target bucket name, and finally create a symlink to `/app/recording.wav` at `/home/user/dataset/<bucket_name>/recording.wav` (you will need to create the bucket directory).

Constraints:
- Both `/home/user/router.sh` and `/home/user/extract.sh` must be executable.
- Your `/home/user/router.sh` must behave perfectly identically (bit-exact output) to `/app/oracle_router` across the specified input space, as it will be subjected to rigorous automated fuzz testing.
- Do not attempt to decompile the oracle. You can query it via the terminal to reconstruct the logic.