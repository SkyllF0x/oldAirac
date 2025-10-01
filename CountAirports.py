import os
from ConvertToXML import OUTPUT
import xml.etree.ElementTree as ET
import re

AIRPORTS = re.compile("APX(\S*).xml")


def readFile(file):
    counter = 0
    root = ET.parse(file).getroot()
    for child in root:
        if child.tag == "Airport":
            counter += 1
    return counter

def main():
    counter = 0
    for root, subFolders, files in os.walk(OUTPUT):
        for file in files:
            if AIRPORTS.fullmatch(file):
                counter += readFile(os.path.join(root,file))
    print(counter)

if __name__ == "__main__":
    main()