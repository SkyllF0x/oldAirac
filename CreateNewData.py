import os
from ConvertToXML import OUTPUT
import xml.etree.ElementTree as ET
import re
from magvar import magnetic_variation
from math import degrees, radians
import pathlib as Path

AIRPORTS = re.compile("APX(\S*).xml")
NAVAID = re.compile("NVX(\S*).xml")
RESULTFOLDER = "NewNav"

ResultTrees = {}

def addSection(regionPrefix):
    if not regionPrefix in ResultTrees.keys():
            root0, root1 = ET.Element("FSData"), ET.Element("FSData")
            tree0, tree1 = ET.ElementTree(root0), ET.ElementTree(root1)
            ResultTrees[regionPrefix] = [root0, root1, tree0, tree1]
            ResultTrees[regionPrefix][0].attrib = {"version":"9.0"}
            ResultTrees[regionPrefix][1].attrib = {"version":"9.0"}

            airport = ET.SubElement(ResultTrees[regionPrefix][1], "Airport")
            airport.attrib = {"name":"name", "ident":"ICAO", "lat":"0.0", "lon":"0.0", "alt":"0.0"}
            

def getAlt(nav):
    result = 0
    try:
        result = float(nav.attrib["alt"][:len(nav.attrib["alt"]) - 1])
    except KeyError:
        result = 0

    return result

def getMagvar(nav):
    alt = getAlt(nav)
    return str(round(degrees(magnetic_variation(2023.03, 
                                              radians(float(nav.attrib["lat"])),
                                              radians(float(nav.attrib["lon"])),
                                              alt)), 2))
    

def addNavaid(file2dd, navaid):
    nav = ET.SubElement(file2dd, navaid.tag)
    nav.attrib = navaid.attrib
    #correct magvar
    nav.attrib["magvar"] = getMagvar(nav)
    #modify alt alt
    nav.attrib["alt"] = str(getAlt(nav))
    for navAdd in nav:
        print(navAdd.tag)
    
    
def addAirportsNavs(regionPrefix, file):
    addSection(regionPrefix)

    ResultFile = ResultTrees[regionPrefix][1]
    airportEntry = ResultFile.find("Airport")

    data = ET.parse(file).getroot()

    for items in data:
        if items.tag == "Airport":
            for airportFacilities in items:
                if airportFacilities.tag == "Runway":
                    #find ILS
                    for RunwayData in airportFacilities:
                        if RunwayData.tag == "Ils":
                            #add ILS entry
                            ilsEntry = ET.SubElement(airportEntry, "Ils")
                            ilsEntry.attrib = RunwayData.attrib
                            ilsEntry.attrib["magvar"] = getMagvar(ilsEntry)
                            ilsEntry.attrib["alt"] = str(getAlt(ilsEntry))
                            ilsEntry.attrib.pop("end")
                            ilsEntry.attrib.pop("backCourse")


def addNavaids(regionPrefix, file):
    addSection(regionPrefix)

    ResultFile = ResultTrees[regionPrefix][0]

    data = ET.parse(file).getroot()
    for child in data:
        if child.tag == "Vor" or child.tag == "Ndb":
            addNavaid(ResultFile, child)


def processAirportFile(rootDir, file):
    folder = os.path.split(rootDir)[1]
    
    destFolder = os.path.join(RESULTFOLDER, folder)
    if not os.path.exists(destFolder):
        os.mkdir(destFolder)
    
    tree = ET.parse(os.path.join(rootDir, file))
    root = tree.getroot()

    resultRoot = ET.Element("FSData")
    resultRoot.attrib = {"version":"9.0"}
    resultTree = ET.ElementTree(resultRoot)
   
    for items in root:
        if items.tag == "Airport":
            
            airport = ET.SubElement(resultRoot, "Airport")
            airport.attrib = {"name":items.attrib["name"], "ident":items.attrib["ident"], "lat":items.attrib["lat"], "lon":items.attrib["lon"], "alt":"0.0"}
            hasVal = False

            for airportFacilities in items:
                if airportFacilities.tag == "Runway":
                    #find ILS
                    for RunwayData in airportFacilities:
                        if RunwayData.tag == "Ils":
                            #add ILS entry
                            ilsEntry = ET.SubElement(airport, "Ils")
                            ilsEntry.attrib = RunwayData.attrib
                            ilsEntry.attrib["magvar"] = getMagvar(ilsEntry)
                            for ilsAdditional in RunwayData:
                                Additional = ET.SubElement(ilsEntry, ilsAdditional.tag)
                                Additional.attrib = ilsAdditional.attrib

                            #ilsEntry.attrib["alt"] = str(getAlt(ilsEntry))
                            ilsEntry.attrib.pop("end")
                            ilsEntry.attrib.pop("backCourse")
                            hasVal = True
                elif airportFacilities.tag == "Waypoint":
                    waypoint = ET.SubElement(airport, "Waypoint")
                    waypoint.attrib = airportFacilities.attrib
                    waypoint.attrib["magvar"] = getMagvar(waypoint)
                    hasVal = True
            
            if not hasVal:
                #print("skip airport", items.attrib["name"])
                resultRoot.remove(airport)


    resultFile = os.path.join(RESULTFOLDER, folder, Path.Path(file).with_suffix(".xml"))
    print("write file {}".format(resultFile))
    with open(resultFile, "wb") as f:
        resultTree.write(f)


def processNavaidFile(rootDir, file):
    folder = os.path.split(rootDir)[1]
    
    destFolder = os.path.join(RESULTFOLDER, folder)
    if not os.path.exists(destFolder):
        os.mkdir(destFolder)

    tree = ET.parse(os.path.join(rootDir, file))
    root = tree.getroot()

    resultRoot = ET.Element("FSData")
    resultRoot.attrib = {"version":"9.0"}
    resultTree = ET.ElementTree(resultRoot)

    for navaid in root:
        if navaid.tag == "Vor" or navaid.tag == "Ndb":
            nav = ET.SubElement(resultRoot, navaid.tag)
            nav.attrib = navaid.attrib
            #correct magvar
            nav.attrib["magvar"] = getMagvar(nav)
            for navAdd in navaid:
                navAddNode = ET.SubElement(nav, navAdd.tag)
                navAddNode.attrib = navAdd.attrib
            #modify alt alt
            #nav.attrib["alt"] = str(getAlt(nav))
    
    resultFile = os.path.join(RESULTFOLDER, folder, Path.Path(file).with_suffix(".xml"))
    print("write file {}".format(resultFile))
    with open(resultFile, "wb") as f:
        resultTree.write(f)
    

def addData(folder):
    regionPredix = folder[:2]
    print(regionPredix)

    for root, subfolders, files in os.walk(os.path.join(OUTPUT, folder)):
        for file in files:
            if AIRPORTS.fullmatch(file):
                pass
                #addAirportsNavs(regionPredix, os.path.join(root, file))
                processAirportFile(root, file)
            elif NAVAID.fullmatch(file):
                #addNavaids(regionPredix, os.path.join(root, file))
                processNavaidFile(root, file)


def splitNavaidFile(file, prefix):
    number = 1
    while  len(ET.tostring(file)) > 100000:
        addSection(prefix + str(number))
        newFile = ResultTrees[prefix + str(number)][0]

        for i, child in enumerate(file):
            if i > 200:
                break
            nav = ET.SubElement(newFile, child.tag)
            nav.attrib = child.attrib
            file.remove(child)

        number += 1
    print("split to {} parts".format(number))


def splitAirportFile(file, prefix):
    number = 1
    while  len(ET.tostring(file)) > 100000:
        print(len(ET.tostring(file)), " len")

        addSection(prefix + str(number))
        newFile = ResultTrees[prefix + str(number)][1]

        for i, child in enumerate(file[0]):
            if i > 300:
                break
            nav = ET.SubElement(newFile[0], child.tag)
            nav.attrib = child.attrib
            file[0].remove(child)

        number += 1
    print("split to {} parts".format(number))


def splitFiles():
    Amount = len(ResultTrees.keys()) 
    for i in range(Amount):
        key = str(i).rjust(2, "0")
        print(key)
        item = ResultTrees[key]
        if len(ET.tostring(item[0])) > 100000:
                print("{} too big, make split".format(key))
                splitNavaidFile(item[0], key)
        if len(ET.tostring(item[1])) > 100000:
            print("{} too big, make split".format(key))
            splitAirportFile(item[1], key)


#write result
def writeResult():
    #split files if to large


    for key, item in ResultTrees.items():
        subfolder =  Path.Path(os.path.join(RESULTFOLDER, key))
        print(subfolder)
        if not os.path.exists(subfolder):
            os.mkdir(subfolder)
        
        fileNavaid = Path.Path(os.path.join(subfolder, key + "NAV")).with_suffix(".xml")
        fileAirport = Path.Path(os.path.join(subfolder, key + "APT")).with_suffix(".xml")



        with open(fileNavaid, "wb") as f:
            print("write to {}".format(fileNavaid))
            item[2].write(f)

        with open(fileAirport, "wb") as f:
            print("write to {}".format(fileAirport))
            item[3].write(f)


def main():
    if not os.path.exists(RESULTFOLDER):
        os.mkdir(RESULTFOLDER)

    for i, root in enumerate(os.listdir(OUTPUT)):
        addData(root)


if __name__ == "__main__":
    main()
    