import xml.etree.ElementTree as ET
import os
import magvar
from CreateNewData import AIRPORTS, NAVAID

def main():

    with open("Airports.dat", "w") as f:
        for root, sub, files in os.walk("XmlDataFSX"):
            for file in files:
                if AIRPORTS.findall(file):
                    r = ET.parse(os.path.join(root, file)).getroot()
                    for entry in r:
                        if entry.tag.lower() == "airport":
                            airport = entry.attrib["ident"]+"|"+entry.attrib["lat"] + "|" + entry.attrib["lon"] + "|" + entry.attrib["alt"][:-1] +  "\n"
                            f.write(airport)


main()