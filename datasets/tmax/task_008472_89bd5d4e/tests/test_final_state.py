# test_final_state.py

import os
import re
from collections import defaultdict

def test_cpp_file_exists_and_contains_required_headers():
    cpp_file = "/home/user/config_manager.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

    with open(cpp_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "<regex>" in content, "The C++ source code must include <regex>."

    has_threading = any(h in content for h in ["<thread>", "<future>", "omp.h", "<mutex>", "pthread"])
    assert has_threading, "The C++ source code must include multi-threading headers (e.g., <thread>, <future>, or omp.h)."

def test_deployment_plan_contents():
    log_file = "/home/user/data/config_events.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    # Recompute the expected output from the log file
    configs = defaultdict(dict)
    deps = defaultdict(set)
    services = set()

    pattern = re.compile(r"\[(.*?)\] SERVICE=(.*?) DEPENDS_ON=(.*?) CONFIG=(.*?):(.*)")

    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                timestamp, service, depends_on, key, value = match.groups()
                services.add(service)

                # Update config if newer or not present
                if key not in configs[service] or timestamp > configs[service][key][0]:
                    configs[service][key] = (timestamp, value)

                # Update dependencies
                if depends_on.strip():
                    for dep in depends_on.split(","):
                        dep = dep.strip()
                        if dep:
                            deps[service].add(dep)
                            services.add(dep)

    # Topological sort with alphabetical tie-breaking
    in_degree = {s: 0 for s in services}
    adj = {s: [] for s in services}

    for s, s_deps in deps.items():
        for dep in s_deps:
            adj[dep].append(s)
            in_degree[s] += 1

    queue = [s for s in services if in_degree[s] == 0]
    queue.sort()

    sorted_services = []
    while queue:
        u = queue.pop(0)
        sorted_services.append(u)

        next_nodes = []
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                next_nodes.append(v)

        for n in next_nodes:
            queue.append(n)
        queue.sort()

    expected_lines = []
    for s in sorted_services:
        s_configs = configs[s]
        sorted_keys = sorted(s_configs.keys())
        config_str = ",".join(f"{k}={s_configs[k][1]}" for k in sorted_keys)
        expected_lines.append(f"SERVICE:{s} CONFIG:{config_str}")

    expected_output = "\n".join(expected_lines)

    plan_file = "/home/user/deployment_plan.txt"
    assert os.path.isfile(plan_file), f"Deployment plan {plan_file} is missing."

    with open(plan_file, "r", encoding="utf-8") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Deployment plan contents are incorrect.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Actual:\n{actual_output}"
    )