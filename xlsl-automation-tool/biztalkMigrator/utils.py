import re

def extractApplicationName(xmlPath):
    with open(xmlPath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'<ModuleRef Name="\[Application:(.*?)\]"', content)
    if match:
        print("match.group(1).strip()")
        return match.group(1).strip()
    else:
        raise ValueError("Could not find application name in binding file.")

