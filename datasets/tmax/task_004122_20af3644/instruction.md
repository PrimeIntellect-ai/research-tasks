As a compliance officer, I need to audit our internal access control system to detect Separation of Duties (SoD) violations. Our system relies on a complex, hierarchical Role-Based Access Control (RBAC) model.

I have two data files:
1. `/home/user/user_roles.csv` - Maps users to their direct roles. (Format: `user_id,role_name`)
2. `/home/user/role_hierarchy.csv` - Defines the role and permission hierarchy. Roles can inherit from other roles, and eventually resolve into specific permissions. (Format: `parent,child` where parent can be a role and child can be a sub-role or a leaf permission).

We also have a proprietary, compiled binary provided by our legacy vendor located at `/app/sod_oracle`. This binary is stripped of debugging symbols. It evaluates combinations of permissions and determines if they constitute a toxic combination (an SoD violation). 
Usage: `/app/sod_oracle <perm1> <perm2> <perm3> ...`
It prints either `SAFE` or a violation message like `TOXIC: permA, permB`.

Your task is to build a query engine and expose it as an HTTP web service. You may use SQLite3 (for recursive CTEs and cross-query aggregation) and Python/Bash to implement the server.

You must start an HTTP server listening exactly on `127.0.0.1:8443` without any authentication. The server must implement the following REST endpoints:

1. `GET /api/v1/audit/<user_id>`
   - Project the graph to find *all* inherited leaf permissions for the given `user_id` using a recursive query on the hierarchy.
   - Pass the flattened list of unique leaf permissions to the `/app/sod_oracle` binary.
   - Return a JSON response with strict schema validation:
     ```json
     {
       "user_id": "<user_id>",
       "effective_permissions": ["perm1", "perm2", "..."],
       "is_compliant": false,
       "toxic_pair": ["permA", "permB"] 
     }
     ```
     (If SAFE, `"is_compliant": true` and `"toxic_pair": []`. Sort the `effective_permissions` alphabetically).

2. `GET /api/v1/stats/centrality`
   - Calculate the degree centrality of all leaf permissions across the *entire* projected user base (i.e., cross-query aggregation of how many users possess each leaf permission, factoring in inheritance).
   - Return the top 3 most widely assigned leaf permissions as a JSON array of objects:
     ```json
     [
       {"permission": "permX", "user_count": 15},
       {"permission": "permY", "user_count": 12},
       {"permission": "permZ", "user_count": 8}
     ]
     ```

Leave the server running in the foreground or background so I can run my automated verification queries against `127.0.0.1:8443`.