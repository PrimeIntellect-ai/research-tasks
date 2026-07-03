apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest flask matplotlib requests

    mkdir -p /app/pde_solver

    cat << 'EOF' > /app/pde_solver/solver.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define IDX(i, j, N) (i + j)

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    int N = atoi(argv[1]);
    if (N <= 0) return 1;

    double *grid = (double *)calloc(N * N, sizeof(double));
    double *new_grid = (double *)calloc(N * N, sizeof(double));

    for (int i = 0; i < N; i++) {
        grid[IDX(i, 0, N)] = 1.0;
        new_grid[IDX(i, 0, N)] = 1.0;
    }

    int iters = 100;
    double max_err = 0.0;

    for (int it = 0; it < iters; it++) {
        max_err = 0.0;
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                new_grid[IDX(i, j, N)] = 0.25 * (
                    grid[IDX(i+1, j, N)] + grid[IDX(i-1, j, N)] +
                    grid[IDX(i, j+1, N)] + grid[IDX(i, j-1, N)]
                );
                double err = fabs(new_grid[IDX(i, j, N)] - grid[IDX(i, j, N)]);
                if (err > max_err) max_err = err;
            }
        }
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                grid[IDX(i, j, N)] = new_grid[IDX(i, j, N)];
            }
        }
    }

    printf("%f\n", 1.0 / N);

    free(grid);
    free(new_grid);
    return 0;
}
EOF

    cat << 'EOF' > /app/pde_solver/Makefile
all:
	gcc -O3 solver.c -o solver
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app