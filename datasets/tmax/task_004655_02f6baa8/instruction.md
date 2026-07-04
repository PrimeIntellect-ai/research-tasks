You are an IT support technician assigned to resolve a high-priority ticket regarding our internal file-hashing pipeline. The pipeline consists of two services that communicate with each other, but it is currently completely broken.

Here is the situation:
1. We have a `frontend.sh` service listening on port 8000 that accepts a filepath, reads the file, and sends its content to our C-based backend processor listening on port 8001. However, the `frontend.sh` script breaks whenever a user requests a file that has spaces in its filename. You need to fix `/app/frontend.sh` so it correctly handles filenames with spaces.
2. The backend service is a C program located in the Git repository at `/app/backend-repo`. Currently, it fails to compile due to linker errors and a missing secret key. A developer accidentally removed the secret key in a previous commit. You need to use Git forensics to recover the secret key, fix the compilation errors (ensure it compiles to `/app/backend-repo/backend_processor`), and ensure it can link properly.
3. The C backend implements a custom rolling hash formula, but the implementation is mathematically flawed. It does not produce the correct output. We have provided a stripped, compiled oracle binary at `/app/oracle_processor` that implements the exact correct behavior. Your compiled C program must perfectly match the output of this oracle for any input. 
4. Once everything is fixed, you must configure and start both services. The frontend must listen on TCP port 8000, and the backend must listen on TCP port 8001. A provided startup script `/app/start_services.sh` is available, but you may need to adjust the ports or configuration so they communicate correctly.

Your final goal is:
1. The `frontend.sh` script is fixed and handles spaces in filenames.
2. The C program is fully compiled at `/app/backend-repo/backend_processor` and its stdout output bit-for-bit matches `/app/oracle_processor` for any given stdin input.
3. Both services are running and successfully integrated.

Please ensure the C executable is compiled exactly at `/app/backend-repo/backend_processor`.