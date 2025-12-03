import re

DANGEROUS_PATTERNS = [
    r"ignore previous instruction",
    r"delete all",
    r"delete the repository",
    r"delete the github repository",
    r"drop database",
    r"rm -rf",
    r"system override",
    r"reveal your system prompt"
]

def validate_safety(user_query: str) -> dict:
    """
    Simple heuristic guardrail to prevent obvious prompt injections
    or destructive commands.
    """
    # 1. Check length
    if len(user_query) > 1000:
        return {"safe": False, "reason": "Query too long (potential buffer overflow/spam)."}

    # 2. Check for dangerous keywords
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, user_query, re.IGNORECASE):
            return {"safe": False, "reason": f"Security Alert: Malicious pattern detected ('{pattern}'). Request blocked."}

    # 3. Domain Restriction (Optional: Ensure it's about DevOps)
    # Simple keyword check to ensure relevance
    valid_context = ["jira", "github", "repo", "code", "deploy", "bug", "sprint", "ticket", "dev", "fix"]
    if not any(word in user_query.lower() for word in valid_context):
         # Soft warning, maybe don't block, but flag it
         pass 

    return {"safe": True, "reason": "Passed checks."}