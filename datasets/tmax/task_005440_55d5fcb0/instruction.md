You are an infrastructure engineer tasked with automating the provisioning of a high-performance, load-balanced mail processing cluster. 

We have a proprietary upstream mail processing daemon located at `/app/mail_worker`. This is a stripped binary, and you must figure out how to launch it correctly. It acts as an SMTP-like sink.

Your objective is to write a single Bash provisioning script at `/home/user/provision.sh` that performs the entire environment setup, reverse proxy configuration, and service management.

Your script must accomplish the following when executed:
1. **Environment Setup**: Create a configuration file at `/home/user/.mail_env` containing the exported environment variables `CLUSTER_NAME=alpha_cluster` and `WORKER_TIMEOUT=15`.
2. **Reverse Proxy Configuration**: Dynamically generate an HAProxy configuration file at `/home/user/haproxy.cfg`. 
   - HAProxy must listen for raw TCP traffic on port `2525`.
   - It must distribute incoming connections evenly (round-robin) across four backend `mail_worker` instances.
   - It must be tuned for high concurrency (at least `maxconn 4000` in the global/defaults sections) to pass the automated benchmark.
3. **Process Management**: 
   - Source the `/home/user/.mail_env` environment.
   - Launch four instances of `/app/mail_worker` in the background. You must inspect the `/app/mail_worker` binary to determine how to specify the listening port. The workers should listen on local ports `9001`, `9002`, `9003`, and `9004`.
   - Launch HAProxy in the background using the generated `/home/user/haproxy.cfg`.
4. **Health Check**: Generate a secondary bash script at `/home/user/health_check.sh` that, when executed, sends a standard SMTP `EHLO benchmark` command to `127.0.0.1:2525` using `nc` or `bash` network redirections, and exits with status 0 if it receives a successful `250` response, and 1 otherwise.

Once your `provision.sh` is ready, execute it so the services are running in the background.

An automated performance benchmarking tool will be run against your load balancer on port `2525`. To pass, your HAProxy and worker configuration must handle a high-concurrency burst of traffic without dropping connections.