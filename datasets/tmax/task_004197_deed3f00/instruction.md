You are a container specialist configuring a local development environment to simulate a production ingress gateway for microservices. Since you do not have root access on this jumpbox, you need to configure environment variables, generate self-signed certificates, and write a standalone, user-level NGINX configuration that acts as an SSL-terminating reverse proxy and load balancer.

Complete the following steps:

1. **Environment Setup**
   Define the following environment variables by appending them to `/home/user/.bashrc`. These define the ports for your mock services:
   * `BACKEND_1="127.0.0.1:9001"`
   * `BACKEND_2="127.0.0.1:9002"`
   * `FRONTEND_PORT="8443"`

2. **TLS Configuration**
   Create a directory `/home/user/certs`. Generate a self-signed RSA (2048-bit) SSL certificate and private key. 
   * Save the certificate at `/home/user/certs/proxy.crt`
   * Save the private key at `/home/user/certs/proxy.key`
   * The Common Name (CN) must be `localhost`.

3. **Reverse Proxy and Load Balancer Setup**
   Write a complete NGINX configuration file at `/home/user/nginx-dev.conf`. To ensure it can be run (or syntax-checked) entirely as a non-root user, the configuration must:
   * Include the directive `daemon off;` at the top level.
   * Write its PID file to `/home/user/nginx.pid`.
   * Write error logs to `/home/user/error.log` (level: info).
   * Contain an `events {}` block (can be empty or contain standard worker connections).
   * Contain an `http {}` block that:
     * Writes access logs to `/home/user/access.log`.
     * Defines an `upstream` block named `microservices` containing the two backend addresses (`127.0.0.1:9001` and `127.0.0.1:9002`) for round-robin load balancing.
     * Defines a `server` block that listens on port `8443` with `ssl`.
     * Uses the `proxy.crt` and `proxy.key` generated earlier.
     * Proxies all requests (location `/`) to `http://microservices`.

Ensure the syntax of your configuration is valid. You do not need to start the NGINX server, but an automated test will validate your configuration file using `nginx -t -c /home/user/nginx-dev.conf`.