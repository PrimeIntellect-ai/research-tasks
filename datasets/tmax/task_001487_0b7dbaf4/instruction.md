You are an ML engineer preparing training data for a sequence alignment model. You need to build a feature extraction pipeline and fix an existing multi-service data fetching setup.

Part 1: Service Configuration (Multi-Service Compose)
We have a data fetching architecture consisting of three services:
1. Redis (port 6379) - caching layer.
2. A Flask API (port 5000) - performs sequence alignment validation and primer design checks.
3. Nginx (port 8080) - acts as an API gateway.

The startup script `/app/start_services.sh` runs these services, but Nginx is misconfigured. 
1. Edit the Nginx configuration file located at `/app/nginx.conf`.
2. Configure it so that any HTTP request to `http://localhost:8080/api/...` is reverse-proxied to the Flask API at `http://localhost:5000/...`.
3. Configure it so that any request to `http://localhost:8080/cache/...` is proxied to a Webdis-like HTTP-to-Redis service running on port 7379 at `http://localhost:7379/...`.
4. Ensure Nginx starts successfully with your new configuration using the provided script.

Part 2: Feature Extraction (Fuzz Equivalence)
You must write a Go command-line program that extracts spectral features from a DNA sequence to measure its periodic regularities.
Create your Go source file at `/home/user/spectral_dist.go` and compile it to `/home/user/spectral_dist`.

The program must take exactly one argument: a DNA sequence string (containing only A, C, G, T).
It must perform the following operations:
1. Convert the sequence to a numeric array using the mapping: A = 1.0, C = 2.0, G = -1.0, T = -2.0.
2. Compute the 1D Discrete Fourier Transform (DFT) of this sequence.
3. Calculate the power spectrum (the squared magnitude of each complex DFT coefficient).
4. Normalize the power spectrum so it sums to 1.0, treating it as a probability distribution over the frequencies. (If the sum is 0, the distribution is uniform 1/N).
5. Calculate the L2 distance (Euclidean distance) between this normalized power spectrum distribution and a discrete uniform distribution (where each element equals 1/N, N being the sequence length).
6. Print exactly the final L2 distance rounded to 6 decimal places (e.g., `0.152345`), followed by a newline.

Your compiled Go program must perfectly match the output of our reference oracle binary located at `/app/oracle/spectral_dist_oracle` for any valid DNA string.