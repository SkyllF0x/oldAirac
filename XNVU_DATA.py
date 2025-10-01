import os
import xml.etree.ElementTree as ET
from magvar import magnetic_variation
from math import degrees, radians, floor
from CreateNewData import AIRPORTS, NAVAID


XNVU_NDB = "2"
XNVU_VOR = "3"
XNVU_VORDME = "4"


def processVor(vorEntry):

    Ident = XNVU_VOR
    for subitem in vorEntry:
        if subitem.tag.lower() == "dme":
            Ident = XNVU_VORDME
            break
    
    return "|".join([Ident, 
            vorEntry.attrib["ident"], 
            vorEntry.attrib["name"], 
            vorEntry.attrib["region"], 
            vorEntry.attrib["lat"], 
            vorEntry.attrib["lon"], 
            "0",
            vorEntry.attrib["frequency"],
            "130",
            "0", "0", "0", "0"])

def processNDB(ndbEntry):
    atr = ndbEntry.attrib
    return "|".join([XNVU_NDB, 
            atr["ident"], 
            atr["name"], 
            atr["region"], 
            atr["lat"], 
            atr["lon"], 
            "0",
            atr["frequency"],
            "30",
            "0", "0", "0", "0"])


def processNavFile(file):
    result = ""

    root = ET.parse(file).getroot()

    for entry in root:
        if entry.tag.lower() == "vor":
            result += processVor(entry) + "\n"
        elif entry.tag.lower() == "ndb":
            result += processNDB(entry) + "\n"
    
    return result


def processAirportData(file):
    result = ""

    root = ET.parse(file).getroot()

    for entry in root:
        if entry.tag.lower() == "airport":
            
            for airportFacility in entry:
                if airportFacility.tag.lower() == "ndb":
                    result += processNDB(airportFacility) +"\n"
    return result

def main():
    file = open("xnvu_wps.txt", "w")

    for root, sub, files in os.walk("XmlDataFSX"):
        for sourceFile in files:
            if NAVAID.fullmatch(sourceFile):
                file.write(processNavFile(os.path.join(root, sourceFile)))
            elif AIRPORTS.fullmatch(sourceFile):
                file.write(processAirportData(os.path.join(root, sourceFile)))
    
    file.close()

if __name__ == "__main__":
    main()