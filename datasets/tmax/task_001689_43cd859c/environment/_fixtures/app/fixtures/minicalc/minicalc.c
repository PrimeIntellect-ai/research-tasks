#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc != 3) return 1;
    long a = atol(argv[1]), b = atol(argv[2]);
    printf("%ld\n", a + b);
    return 0;
}
