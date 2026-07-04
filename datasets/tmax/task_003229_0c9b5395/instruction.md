We are migrating our infrastructure and have encountered a critical issue. A scheduled cron task that generates our reverse proxy configuration is failing because the legacy configuration generator binary is incompatible with our new OS architecture. We only have the stripped legacy binary available, and we lost its original source code. 

You need to reverse-engineer the behavior of this legacy binary and write a replacement script.

The legacy binary is located at `/app/legacy_lb_gen`. 
It accepts a single command-line argument: a comma-separated list of backend server definitions in the format `IP:PORT:WEIGHT` (e.g., `192.168.1.10:80:5,10.0.0.5:8080:12`).
It writes a load balancer configuration snippet to standard output.

Your task:
1. Analyze the output of `/app/legacy_lb_gen` by running it with various inputs.
2. Deduce the logic it uses to format the output, calculate backend parameters (like max connections and proxy weights), and sort the backend servers.
3. Write a replacement script (in Python, Perl, Ruby, Bash, or any language of your choice) located at `/home/user/lb_gen`.
4. Ensure `/home/user/lb_gen` is executable (`chmod +x /home/user/lb_gen`).

Your script must produce **bit-exact identical output** to `/app/legacy_lb_gen` for any valid input sequence. We will verify your solution by fuzzing both your script and the legacy binary with hundreds of random input combinations and asserting that their standard outputs match exactly.

Do not try to call the original binary from your script. You must reimplement its logic.