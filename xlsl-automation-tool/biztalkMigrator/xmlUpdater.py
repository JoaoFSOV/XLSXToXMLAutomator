import xml.etree.ElementTree as ET
import re
from .excelReader import filterData

def updateXmlFile(xmlPath, passwordsData, URIData, mode):
    if mode == 1 or mode == 2:
        print("I will be changing the passwords of the xml file")
        sendPortCredentials = filterData(passwordsData, "Send")
        receivePortCredentials = filterData(passwordsData, "Receive")
        print(f"SendPortCredentials: {sendPortCredentials}")
        print(f"ReceivePortCredentials: {receivePortCredentials}")

        # Update passwords on the send and receive ports
        updateSendPortsWithPasswords(xmlPath, sendPortCredentials)
        updateReceiveLocationsWithPasswords(xmlPath, receivePortCredentials)

    if mode == 1 or mode == 3:
        print("I will be changing the paths of the xml file")
        # Update the paths on the send and receive ports
        #updateSendPortsWithPath(xmlPath, data)
        #updateReceivePortsWithPath(xmlPath, data)

def updateSendPortsWithPasswords(xmlPath, data):
    updatedPorts = 0
    with open(xmlPath, "r", encoding="utf-8") as f:
        content = f.read()

    for info in data:
        portName = info[0]
        user = info[2]
        password = info[3]
        print(f"Starting with port {portName} with user {user} and password {password}.")
        sendport_pattern = rf"(<SendPort\b[^>]*\bName\s*=\s*\"{re.escape(portName)}\"[^>]*>.*?</SendPort>)"
        match = re.search(sendport_pattern, content, re.DOTALL)

        if match:
            print("Found it on the XML file!")
            full_sendport = match.group(1)

            # Replace the password section in TransportTypeData
            def replace_password(match_ttdata):
                ttdata = match_ttdata.group(0)
                new_password_field = f"&lt;Password vt=\"8\"&gt;{password}&lt;/Password&gt;"
                ttdata = re.sub(
                    r"&lt;Password vt=\"1\" ?/(&gt;|>)",
                    lambda m: new_password_field,
                    ttdata
                )
                
                return ttdata

            updated_sendport = re.sub(
                r"<TransportTypeData>.*?</TransportTypeData>",
                lambda m: replace_password(m),
                full_sendport,
                flags=re.DOTALL
            )

            if updated_sendport != full_sendport:
                content = content.replace(full_sendport, updated_sendport)
                updatedPorts += 1
                print(f"Updated port {portName}.")
            else:
                print(f"Port {portName} had no matching password to update.")
        else:
            print("Did not find it on the XML file!")

    if updatedPorts > 0:
        with open(xmlPath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated {updatedPorts} port(s).")
    else:
        print("No ports were updated.")
        
def updateReceiveLocationsWithPasswords(xmlPath, data):
    print(f"-------------------------------------------------------------- UPDATE RECEIVELocationsWITHPASSWORDS ----------------------------------")
    updatedLocations = 0
    with open(xmlPath, "r", encoding="utf-8") as f:
        content = f.read()

    print("Opened the XML file for reading")
    print(f"Data: {data}")
    
    for info in data:
        locationName = info[0]
        user = info[2]
        password = info[3]
        print(f"Starting with receive location {locationName} with user {user} and password {password}.")
        
        receivelocation_pattern = rf"(<ReceiveLocation\b[^>]*\bName\s*=\s*\"{re.escape(locationName)}\"[^>]*>.*?</ReceiveLocation>)"
        match = re.search(receivelocation_pattern, content, re.DOTALL)

        if match:
            print("Found it in the XML file!")
            full_receivelocation = match.group(1)

            def replace_password(match_ttdata):
                ttdata = match_ttdata.group(0)
                new_password_field = f"&lt;Password vt=\"8\"&gt;{password}&lt;/Password&gt;"
                ttdata = re.sub(
                    r"&lt;Password vt=\"1\" ?/(&gt;|>)",
                    lambda m: new_password_field,
                    ttdata
                )
                return ttdata

            updated_receivelocation = re.sub(
                r"<ReceiveLocationTransportTypeData>.*?</ReceiveLocationTransportTypeData>",
                lambda m: replace_password(m),
                full_receivelocation,
                flags=re.DOTALL
            )

            if updated_receivelocation != full_receivelocation:
                content = content.replace(full_receivelocation, updated_receivelocation)
                updatedLocations += 1
                print(f"Updated receive location {locationName}.")
            else:
                print(f"Receive location {locationName} had no matching password to update.")
        else:
            print("Did not find it in the XML file!")

    if updatedLocations > 0:
        with open(xmlPath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated {updatedLocations} receive location(s).")
    else:
        print("No receive locations were updated.")


