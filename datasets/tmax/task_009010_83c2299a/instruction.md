You are tasked with fixing a broken web architecture. Our Nginx server is currently returning a `502 Bad Gateway` error when accessing `http://127.0.0.1:8080/api`. 

The architecture is supposed to work as follows:
1. Nginx listens on `127.0.0.1:8080` and reverse-proxies requests to `127.0.0.1:8081`. 
2. A custom port-forwarding service (which you must write in Rust) listens on `127.0.0.1:8081` and forwards all raw TCP traffic to a Unix domain socket located at `/home/user/backend/app.sock`.
3. A backend service (already running) listens on `/home/user/backend/app.sock` and responds to the requests.

However, the system is currently broken due to several issues:
1. **Missing Forwarder:** The Rust port-forwarding service does not exist. You need to create a new Rust project at `/home/user/rust_forwarder` and write a high-performance TCP-to-Unix-Socket forwarder. It must accept connections on `127.0.0.1:8081` and seamlessly bridge bidirectional data to `/home/user/backend/app.sock`.
2. **Permission Issues:** The backend Unix socket is located in `/home/user/backend`, but the directory currently has the wrong permissions, preventing your Rust app from connecting to it. You need to identify and fix the permissions of the directory so that the Rust process can read and write to the socket.
3. **Directory Structure / Link:** The Rust application is required to write a simple startup log file named `startup.log` into the `/home/user/logs` directory. However, this directory does not exist. You must create `/home/user/logs` as a symbolic link pointing to `/home/user/backend/logs`.
4. **Testing:** Once everything is running, you must start the Nginx server using the provided configuration at `/home/user/nginx/nginx.conf`. Then, use `curl` to make a GET request to `http://127.0.0.1:8080/api` and save the raw HTTP response body to `/home/user/final_output.txt`.

To succeed, you must:
- Fix the permissions on `/home/user/backend`.
- Create the correct symlink for `/home/user/logs`.
- Initialize a Rust project at `/home/user/rust_forwarder`, write the port-forwarding code, and compile it (you may use standard library `std::net` and `std::os::unix::net` or crates like `tokio`).
- Run your Rust forwarder in the background.
- Start Nginx (e.g., `nginx -c /home/user/nginx/nginx.conf`).
- Save the successful `curl` response to `/home/user/final_output.txt`.

Note: You do not have root access. All services (including Nginx) are configured to run entirely in user-space (`/home/user`). The backend service is already running on the Unix socket.