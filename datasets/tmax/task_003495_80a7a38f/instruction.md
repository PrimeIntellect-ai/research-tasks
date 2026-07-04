You are an SRE tasked with restoring our internal uptime monitoring pipeline. 

We have two services running locally:
1. `status_emitter` listening on TCP port 9001. When connected, it outputs raw text health metrics in the format: `UPTIME:<seconds>:CPU:<usage>:MEM:<usage>\n`
2. `metrics_collector` listening on TCP port 9002. It expects to receive formatted metric packets.

The previous formatting utility was lost, but we have a stripped, compiled backup located at `/app/bin/oracle_parser`. We need you to write a replacement in C.

Your tasks:
1. Write a C program at `/home/user/metric_parser.c` and compile it to `/home/user/metric_parser`. 
   - It must read a single line of raw text metric from `stdin`.
   - It must output the formatted metric to `stdout`.
   - The output format is: `[STAT] U:<seconds> C:<cpu> M:<mem> <STATUS>\n`
   - `<STATUS>` should be `OK` if both CPU and MEM are strictly less than 90. Otherwise, it should be `WARN`.
   - Your compiled program's behavior must exactly match `/app/bin/oracle_parser` for all valid inputs.
2. Create a bridge script at `/home/user/bridge.sh` that uses text processing and networking tools (like `nc` or `expect`) to continuously read from `127.0.0.1:9001`, pipe the output through your `/home/user/metric_parser`, and send the result to `127.0.0.1:9002`.
3. Ensure `/home/user/bridge.sh` has executable permissions.
4. Create a log file at `/home/user/setup_complete.log` containing the text "DONE" when you have finished.