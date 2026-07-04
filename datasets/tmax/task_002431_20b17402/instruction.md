You are a security researcher analyzing a suspicious C++ botnet infrastructure. You have intercepted a bundle of services and source code, but the environment is broken and the payload decoder is a compiled black box. Your goal is to restore the integration environment, identify a regression in the botnet's source code, and reverse-engineer its payload decoder.

**Stage 1: Infrastructure Recomposition**
The botnet relies on three cooperating services located in `/app/services/`:
1. `sensor.py`: A Python script generating mock sensitive data on TCP port 9001.
2. `cache`: A local Redis instance (default port 6379).
3. `c2_server.py`: A Flask command-and-control server on port 9002.

The botnet bridges these services, but the configuration is missing. 
- Create a startup script at `/home/user/start_infrastructure.sh` that launches Redis, `sensor.py`, and `c2_server.py` in the background.
- You must create a configuration file `/home/user/bridge_config.json` (used by the bot later) that specifies the host and ports for "sensor", "cache", and "c2" so that the expected end-to-end flow works: the bot will read from the sensor, store in cache, and forward to C2.

**Stage 2: Git Bisection and Anomaly Investigation**
You have the source code for the bot that bridges these services in a local Git repository at `/home/user/bot_repo`. 
- The `main` branch contains a bug that causes an *intermittent* segmentation fault (crashing roughly 5% of the time under load).
- The commit tagged `v1.0` is known to be good.
- Create a regression test script to reliably trigger the intermittent failure, use Git bisection to find the exact commit hash that introduced the crash, and write the full 40-character commit hash to `/home/user/bad_commit.txt`.

**Stage 3: Payload Decoder Reverse Engineering**
The repository does not contain the source code for the bot's custom payload decoder. Instead, you only have a stripped binary at `/app/oracle_decoder`. 
- The binary reads raw binary data from standard input, applies a custom decryption algorithm, and writes the decrypted data to standard output.
- You must reverse-engineer the cryptographic transformation by analyzing its input/output behavior (e.g., by feeding it null bytes or sequential patterns).
- Write a clean C++ reimplementation of this algorithm in `/home/user/decoder.cpp` and compile it to `/home/user/decoder.bin`.
- Your reimplementation must be BIT-EXACT equivalent to `/app/oracle_decoder` for any arbitrary byte stream up to 1 MB in length. 

Ensure your `decoder.bin` reads from `stdin` and writes to `stdout` identically to the oracle.