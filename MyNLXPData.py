import os
import xml.etree.ElementTree as ET
from CreateDataXP11 import convertAlt, getLOCBearing, getAirportRegCode
from CreateNewData import AIRPORTS, NAVAID

ArrayOfData =  ET.Element('ArrayOfEachNAVXP')
ArrayOfDataRoot = ET.ElementTree(ArrayOfData)


def convertCoord(coordStr):
    #9 places
    return "{0:.9f}".format(round(float(coordStr), 9))
    

def processAirportData():
    pass


def processNDB(node, areaCode):
    ndbNode = ET.SubElement(ArrayOfData, 'eachNAVXP')
    ET.SubElement(ndbNode, 'LatitudeDec').text = convertCoord(node.attrib["lat"])
    ET.SubElement(ndbNode, 'LongitudeDec').text = convertCoord(node.attrib["lon"])
    ET.SubElement(ndbNode, 'TypeP').text = 'NDB'
    ET.SubElement(ndbNode, 'Name').text = node.attrib['ident']
    ET.SubElement(ndbNode, 'FullName').text = node.attrib['name']
    ET.SubElement(ndbNode, 'Elevation').text = convertAlt(node.attrib['alt'])
    ET.SubElement(ndbNode, 'GSelevation').text = '0'
    ET.SubElement(ndbNode, 'Frequency').text = node.attrib['frequency']
    ET.SubElement(ndbNode, 'Range').text = '50'
    ET.SubElement(ndbNode, 'Region').text = node.attrib["region"]
    ET.SubElement(ndbNode, 'ICAO').text = areaCode
    ET.SubElement(ndbNode, 'TrueBear').text = '0'
    ET.SubElement(ndbNode, 'Runway')
    ET.SubElement(ndbNode, 'Offset').text = '0'
    return ndbNode


def processILS(node, airport):
    runway = node.attrib["name"].split()[-1]

    ilsNode = ET.SubElement(ArrayOfData, 'eachNAVXP')
    ET.SubElement(ilsNode, 'LatitudeDec').text = convertCoord(node.attrib["lat"])
    ET.SubElement(ilsNode, 'LongitudeDec').text = convertCoord(node.attrib["lon"])
    ET.SubElement(ilsNode, 'TypeP').text = 'ILS'
    ET.SubElement(ilsNode, 'Name').text = node.attrib['ident']
    ET.SubElement(ilsNode, 'FullName')
    ET.SubElement(ilsNode, 'Elevation').text = convertAlt(node.attrib['alt'])
    ET.SubElement(ilsNode, 'GSelevation').text = '0'
    ET.SubElement(ilsNode, 'Frequency').text = node.attrib['frequency']
    ET.SubElement(ilsNode, 'Range').text = '18'
    ET.SubElement(ilsNode, 'Region').text = getAirportRegCode(airport)
    ET.SubElement(ilsNode, 'ICAO').text = airport.attrib["ident"]
    ET.SubElement(ilsNode, 'TrueBear').text =  getLOCBearing(node)
    ET.SubElement(ilsNode, 'Runway').text = runway
    ET.SubElement(ilsNode, 'Offset').text = '0'

    #add GS if present
    for subentry in node:
        if subentry.tag.lower() == "glideslope":
            gs = ET.SubElement(ArrayOfData, 'eachNAVXP')
            ET.SubElement(gs, 'LatitudeDec').text = convertCoord(node.attrib["lat"])
            ET.SubElement(gs, 'LongitudeDec').text = convertCoord(node.attrib["lon"])
            ET.SubElement(gs, 'TypeP').text = 'GS'
            ET.SubElement(gs, 'Name').text = node.attrib['ident']
            ET.SubElement(gs, 'FullName')
            ET.SubElement(gs, 'Elevation').text = convertAlt(node.attrib['alt'])
            ET.SubElement(gs, 'GSelevation').text = '0'
            ET.SubElement(gs, 'Frequency').text = node.attrib['frequency']
            ET.SubElement(gs, 'Range').text = '18'
            ET.SubElement(gs, 'Region').text = getAirportRegCode(airport)
            ET.SubElement(gs, 'ICAO').text = airport.attrib["ident"]
            ET.SubElement(gs, 'TrueBear').text =  node.attrib["heading"]
            ET.SubElement(gs, 'Runway').text = runway
            ET.SubElement(gs, 'Offset').text = '0'
            return {"ILS": ilsNode, "GS":gs}
    
    return {"ILS": ilsNode}


def processNavFile(file):
    tree = ET.parse(file)
    root = tree.getroot()

    for child in root:
        if child.tag.lower() == "vor":
            vorNode = ET.SubElement(ArrayOfData, 'eachNAVXP')
            ET.SubElement(vorNode, 'LatitudeDec').text = convertCoord(child.attrib["lat"])
            ET.SubElement(vorNode, 'LongitudeDec').text = convertCoord(child.attrib["lon"])
            ET.SubElement(vorNode, 'TypeP').text = 'VOR'
            ET.SubElement(vorNode, 'Name').text = child.attrib['ident']
            ET.SubElement(vorNode, 'FullName').text = child.attrib['name']
            ET.SubElement(vorNode, 'Elevation').text = convertAlt(child.attrib['alt'])
            ET.SubElement(vorNode, 'GSelevation').text = '0'
            ET.SubElement(vorNode, 'Frequency').text = "{0:.2f}".format(float(child.attrib['frequency']))
            ET.SubElement(vorNode, 'Range').text = str(round(float(child.attrib["range"][:-1])/1852, 0))
            ET.SubElement(vorNode, 'Region').text = child.attrib["region"]
            ET.SubElement(vorNode, 'ICAO').text = "ENRT"
            ET.SubElement(vorNode, 'TrueBear').text = '0'
            ET.SubElement(vorNode, 'Runway')
            ET.SubElement(vorNode, 'Offset').text = '0'
            ArrayOfData.append(vorNode)
        if child.tag.lower() == "ndb":
            ArrayOfData.append(processNDB(child, "ENRT"))


def processAirportFile(file):
    tree = ET.parse(file)
    root = tree.getroot()

    for child in root:
        if child.tag.lower() == "airport":

            for airportFacility in child:
                if airportFacility.tag.lower() == "ndb":
                    ArrayOfData.append(processNDB(airportFacility, child.attrib["ident"]))

                if airportFacility.tag.lower() == "runway":
                    for RunwayData in airportFacility:
                        if RunwayData.tag.lower() == "ils":
                            ilsNodes = processILS(RunwayData, child)
                            ArrayOfData.append(ilsNodes["ILS"])
                            if "GS" in ilsNodes.keys():
                                ArrayOfData.append(ilsNodes["GS"])


            
def main():
    for root, sub, files in os.walk("XmlDataFSX"):
        for sourceFile in files:
            if NAVAID.fullmatch(sourceFile):
                processNavFile(os.path.join(root, sourceFile))
            elif AIRPORTS.fullmatch(sourceFile):
                processAirportFile(os.path.join(root, sourceFile))

    file = open("earthNAVXP.xml", "wb")
    ArrayOfDataRoot.write(file)
    file.close()

if __name__ == "__main__":
    main()