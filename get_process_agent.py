import json
import os
def query_active_directory(query: str) -> str:
    """Queries the campus Windows Active Directory server using secure LDAP.
    Args:
        query: The Student ID or First and Last Name.
    """
    # Mock LDAP query for safety/development
    return f"Active Directory lookup for {query} failed: Connection timeout."
def query_local_users_fallback(query: str) -> str:
    """Queries the local fallback file users.json for a matching user.
    Args:
        query: The Student ID or First Name and Last Name.
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "users.json")
        with open(file_path, "r") as f:
            data = json.load(f)
            
        for user in data.get("users", []):
            if query.lower() in user.get("student_id", "").lower() or \
               query.lower() in user.get("full_name", "").lower():
                return json.dumps(user)
                
        return json.dumps({"error": "User not found in local fallback."})
    except Exception as e:
        return json.dumps({"error": str(e)})
# We will export the tools to be used by the orchestrator
get_process_agent_tools = [query_active_directory, query_local_users_fallback]
