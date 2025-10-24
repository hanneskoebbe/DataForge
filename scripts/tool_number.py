import re

def tool_number(s):
    match = re.search(r'(\d{4})-F\d', s)
    if match:
        return match.group(0)
    return None