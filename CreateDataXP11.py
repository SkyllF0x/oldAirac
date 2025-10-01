import os
import xml.etree.ElementTree as ET
import datetime
from magvar import magnetic_variation
from math import degrees, radians, floor
from CreateNewData import AIRPORTS, NAVAID

NDB_CODE = "2"
VOR_CODE = "3"
ILS_LOC_CODE = "4"
LOC_CODE = "5"
GS_CODE = "6"
DME_CODE = "12"
DME_STANDALONE_CODE = "13"


def convertCoords(coords: str):
    return "{0:.8f}".format(round(float(coords), 8))


def convertAlt(altStr: str):
    return str(floor(float(altStr[:-1]) * 3.28))


def convertVhfFreq(freqStr: str):
    return str(floor(float(freqStr) * 100))


def getVorClass(vorAttr):
    match vorAttr["type"]:
        case "HIGH":
            return "130"
        case "LOW":
            return "40"
        case "TERMINAL":
            return "25"
        case _:
            return "125"


def getVorName(vorEntry):
    result = vorEntry.attrib["name"]
    for child in vorEntry:
        if child.tag.lower() == "dme":
            return result + " VOR/DME"
    else:
        return result + " VOR"


def getMagVar(vorAttr: dict):
    lat = radians(float(vorAttr["lat"]))
    lon = radians(float(vorAttr["lon"]))
    alt = float(vorAttr["alt"][:-1])
    return "{0:.3f}".format(degrees(magnetic_variation(2025.03, lat, lon, alt)))


def processVor(item):
    vorStr = (VOR_CODE + " "
    + convertCoords(item.attrib["lat"]) + " "
    + convertCoords(item.attrib["lon"]) + " "
    + convertAlt(item.attrib["alt"]) + " "
    + convertVhfFreq(item.attrib["frequency"]) + " "
    + getVorClass(item.attrib) + " "
    + str(getMagVar(item.attrib)) + " "
    + item.attrib["ident"] + " "
    + "ENRT "
    + item.attrib["region"] + " "
    + getVorName(item))

    #search for DME entry
    for child in item:
        if child.tag.lower() == "dme":
            #add DME entry
            vorStr += ("\n" + 
                       DME_CODE + " "
                       + convertCoords(child.attrib["lat"]) + " "
                       + convertCoords(child.attrib["lon"]) + " "
                       + convertAlt(item.attrib["alt"]) + " "
                       + convertVhfFreq(item.attrib["frequency"]) + " "
                       + getVorClass(item.attrib) + " "
                       + "0.000" + " " 
                       + item.attrib["ident"] + " "
                       + "ENRT "
                       + item.attrib["region"] + " "
                       + getVorName(item))
            return vorStr
    else:
        return vorStr
    

def processNDB(item, terminalArea="ENRT"):
    return (NDB_CODE + " "
        + convertCoords(item.attrib["lat"]) + " "
        + convertCoords(item.attrib["lon"]) + " "
        + convertAlt(item.attrib["alt"]) + " "
        + str(floor(float(item.attrib["frequency"]))) + " "
        + "50" + " "
        + "0.0" + " "
        + item.attrib["ident"] + " "
        + (terminalArea) + " "
        + item.attrib["region"] + " " 
        + item.attrib["name"] + " NDB")


def getLOCBearing(ilsEntry):
    trueDeg = float(ilsEntry.attrib['heading'])
    magHed = floor(trueDeg + float(getMagVar(ilsEntry.attrib)))

    return "{0:.3f}".format(magHed * 360 + trueDeg)


def getAirportRegCode(airport):
    #try find waypoint and get code from it
    for child in airport:
        if child.tag.lower() == "waypoint":
            return child.attrib["waypointRegion"]
    
    return "K1"


def processILS(ilsEntry, airport, runway):
    result = ""
    regCode = getAirportRegCode(airport)
    isIls, hasDME = False, False
    

    for subentry in ilsEntry:
        if subentry.tag.lower() == "dme":
            hasDME = True
            result+=(DME_CODE + " "
                    + convertCoords(subentry.attrib["lat"]) + " "
                    + convertCoords(subentry.attrib["lon"]) + " " 
                    + convertAlt(subentry.attrib["alt"]) + " "
                    + convertVhfFreq(ilsEntry.attrib["frequency"]) + " "
                    + "25" + " " 
                    + "0.0" + " " 
                    + ilsEntry.attrib["ident"] + " "
                    + airport.attrib["ident"] + " "
                    + regCode + " "
                    + airport.attrib["name"] + " DME-ILS"
                    ) + "\n"
        if subentry.tag.lower() == "glideslope":
            isIls = True

            result += (GS_CODE + " "
                    + convertCoords(subentry.attrib["lat"]) + " "
                    + convertCoords(subentry.attrib["lon"]) + " " 
                    + convertAlt(subentry.attrib["alt"]) + " "
                    + convertVhfFreq(ilsEntry.attrib["frequency"]) + " "
                    + "25" + " "
                    + str(round(float(subentry.attrib["pitch"]) * 100000 + float(ilsEntry.attrib["heading"]), 3))  + " "
                    + ilsEntry.attrib["ident"] + " "
                    + airport.attrib["ident"] + " "
                    + regCode + " "
                    + runway + " "
                    + "GS\n"
                    )
            
    code = LOC_CODE
    name = "LOC"
    if isIls:
        code = ILS_LOC_CODE
        name = "ILS-cat-II"

        if not hasDME:
            #add manually XP require it
            result += (DME_CODE + " "
                    + convertCoords(ilsEntry.attrib["lat"]) + " "
                    + convertCoords(ilsEntry.attrib["lon"]) + " " 
                    + convertAlt(ilsEntry.attrib["alt"]) + " "
                    + convertVhfFreq(ilsEntry.attrib["frequency"]) + " "
                    + "25" + " " 
                    + "0.0" + " " 
                    + ilsEntry.attrib["ident"] + " "
                    + airport.attrib["ident"] + " "
                    + regCode + " "
                    + airport.attrib["name"] + " DME-ILS"
                    ) + "\n"

    result = (
        code + " "
        + convertCoords(ilsEntry.attrib["lat"]) + " "
        + convertCoords(ilsEntry.attrib["lon"]) + " " 
        + convertAlt(ilsEntry.attrib["alt"]) + " "
        + convertVhfFreq(ilsEntry.attrib["frequency"]) + " "
        + "25" + " "
        + getLOCBearing(ilsEntry) + " "
        + ilsEntry.attrib["ident"] + " "
        + airport.attrib["ident"] + " "
        + regCode + " "
        + runway + " "
        + name + "\n"
    ) + result

    return result


def processNavFile(fileName):
    result = ""

    tree = ET.parse(fileName)
    root = tree.getroot()
    for item in root:
        if item.tag.lower() == "vor":
            result += (processVor(item) + "\n")
        if item.tag.lower() == "ndb":
            result += (processNDB(item) + "\n")
    
    return result


def processAirportData(file):
    root = ET.parse(file).getroot()
    result = ""

    for entry in root:
        if entry.tag.lower() == "airport":
            
            for airportFacility in entry:
                if airportFacility.tag.lower() == "ndb":
                    result += (processNDB(airportFacility, entry.attrib["ident"]) + "\n")
                if airportFacility.tag.lower() == "runway":
                    for RunwayData in airportFacility:
                        if RunwayData.tag.lower() == "ils":
                            result += (processILS(RunwayData, entry, RunwayData.attrib["name"].split()[-1]))

    return result

def main():
    
    file = open("user_nav.dat", "w")
    file.write("I\n")
    file.write("1150 Version - data cycle 0091, build {}, metadata NavXP1150. \n".format(datetime.date.today().strftime('%Y%m%d')))

    for root, sub, files in os.walk("XmlDataFSX"):
        for sourceFile in files:
            if NAVAID.fullmatch(sourceFile):
                pass
                file.write(processNavFile(os.path.join(root, sourceFile)))
            elif AIRPORTS.fullmatch(sourceFile):
                file.write(processAirportData(os.path.join(root, sourceFile)))
    
    file.write("99")
    file.close()

if __name__ == "__main__":
    main()