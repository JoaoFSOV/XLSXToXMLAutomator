import pandas as pd
import re

# Get the application name of the xml binding file
def extractApplicationName(xmlPath):
    with open(xmlPath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'<ModuleRef Name="\[Application:(.*?)\]"', content)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("Could not find application name in binding file.")

# Returns a list of the ports info we need to change
# The ones with username and password and from the same aplication of the xml binding file
def readCredentials(filepath, bindingXmlPath):
    appName = extractApplicationName(bindingXmlPath)
    df = pd.read_excel(filepath, engine='openpyxl')

    required_columns = {"Name", "User", "Password", "Application", "Type"}
    if not required_columns.issubset(df.columns):
        raise ValueError("You are not using the templates for the .xlsx files.")

    credentials = []
    for _, row in df.iterrows():
        portName = str(row["Name"]).strip()
        user = str(row["User"]).strip()
        password = str(row["Password"]).strip()
        app = str(row["Application"]).strip()
        portType = str(row["Type"]).strip()

        # Exclude empty and 'not_found' for both user and password
        excludedResults = {"not_found", "nan"}
        if user and password and user.strip().lower() not in excludedResults and password.strip().lower() not in excludedResults:
            if app.strip().lower() == appName.lower():
                credentials.append((portName, portType, user.strip(), password.strip()))

    return credentials

# Filter data acording to port type
def filterData(data, portTypeSelector):
    ports = []
    for info in data:
        portType = info[1]
        if portType == portTypeSelector:
            ports.append(info)
    return ports

# Returns a list of the ports info we need to change
# Port name, its current URI and the new one
def readUris(filepath):
    df = pd.read_excel(filepath, engine='openpyxl')
    print("URI Mapping Columns:", df.columns.tolist())

    mappings = []
    for _, row in df.iterrows():
        portName = row['Name']
        old_uri = row['OldURI']
        new_uri = row['NewURI']
        mappings.append((portName, old_uri, new_uri))

    return mappings

