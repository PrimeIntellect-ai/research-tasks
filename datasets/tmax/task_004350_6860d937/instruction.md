You are an open-source maintainer reviewing a broken Pull Request. The PR adds a simple dependency resolution utility written in C (`resolve.c`). The utility is designed to read a list of available semantic versions and a list of constraints, and determine the highest available version that satisfies all constraints.

The contributor's code is failing the CI pipeline for two reasons:
1. **Character Encoding:** The test suite uses constraint files generated on a Windows system, which are encoded in UTF-16LE. The C program currently assumes UTF-8/ASCII.
2. **Semantic Version Comparison:** The contributor used `strcmp` to compare versions. This naive approach incorrectly evaluates `1.10.0` as older than `1.2.0` because `'1' < '2'`.

The project workspace is at `/home/user/semver-resolve/`. 
Inside, you will find:
- `resolve.c`: The broken C program.
- `available.txt`: A UTF-8 encoded file containing a list of available versions, one per line.
- `constraints.txt`: A UTF-16LE encoded file containing version constraints, one per line (e.g., `>= 1.0.0`).

Your task:
1. Fix the `resolve.c` program. Implement a proper semantic version comparison function to replace the `strcmp` logic. Assume all versions strictly follow the `X.Y.Z` format (no pre-release or build metadata).
2. Deal with the UTF-16LE encoding of `constraints.txt`. You may either modify the C program to handle it natively, or create a wrapper shell script `run.sh` in the same directory that transcodes the input files and runs the compiled C program.
3. Use the fixed setup to process `available.txt` and `constraints.txt`.
4. Write the highest version string that satisfies all constraints to a file exactly at `/home/user/resolved_version.txt`.

Here is the contributor's broken `resolve.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_VERSIONS 100
#define MAX_CONSTRAINTS 100

// BUG: Naive string comparison doesn't work for semver (e.g., "1.10.0" < "1.2.0")
int compare_versions(const char *v1, const char *v2) {
    return strcmp(v1, v2);
}

int check_constraint(const char *version, const char *op, const char *target) {
    int cmp = compare_versions(version, target);
    if (strcmp(op, "==") == 0) return cmp == 0;
    if (strcmp(op, "!=") == 0) return cmp != 0;
    if (strcmp(op, ">=") == 0) return cmp >= 0;
    if (strcmp(op, "<=") == 0) return cmp <= 0;
    if (strcmp(op, ">") == 0) return cmp > 0;
    if (strcmp(op, "<") == 0) return cmp < 0;
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <available.txt> <constraints.txt>\n", argv[0]);
        return 1;
    }

    FILE *f_avail = fopen(argv[1], "r");
    FILE *f_const = fopen(argv[2], "r");
    if (!f_avail || !f_const) {
        perror("Error opening files");
        return 1;
    }

    char available[MAX_VERSIONS][32];
    int avail_count = 0;
    while (fscanf(f_avail, "%31s", available[avail_count]) == 1) {
        avail_count++;
    }

    char ops[MAX_CONSTRAINTS][4];
    char targets[MAX_CONSTRAINTS][32];
    int const_count = 0;
    while (fscanf(f_const, "%3s %31s", ops[const_count], targets[const_count]) == 2) {
        const_count++;
    }

    char *best_version = NULL;

    for (int i = 0; i < avail_count; i++) {
        int valid = 1;
        for (int j = 0; j < const_count; j++) {
            if (!check_constraint(available[i], ops[j], targets[j])) {
                valid = 0;
                break;
            }
        }
        if (valid) {
            if (best_version == NULL || compare_versions(available[i], best_version) > 0) {
                best_version = available[i];
            }
        }
    }

    if (best_version) {
        printf("%s\n", best_version);
    } else {
        printf("None\n");
    }

    fclose(f_avail);
    fclose(f_const);
    return 0;
}
```