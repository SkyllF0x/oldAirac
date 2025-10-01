import xml.etree.ElementTree as ET
import os

fileOut = ET.parse("sky-olddata.xml")
root = fileOut.getroot()

def main():
    for file in os.listdir("NewNav"):
        node = ET.SubElement(root[2], "AssetGroup")
        node.attrib = {"Name": file}
        typeNode = ET.SubElement(node, "Type")
        typeNode.text = "BGL"

        flagNode = ET.SubElement(node, "Flags")
        FSXComp  = ET.SubElement(flagNode, "FSXCompatibility")
        FSXComp.text = "false"

        AssetDir = ET.SubElement(node, "AssetDir")
        AssetDir.text = os.path.join("PackageSources\Scenery\olddata", file)

        OutputDir = ET.SubElement(node, "OutputDir")
        OutputDir.text = os.path.join("Scenery\olddata", file)
    
    with open("skytest.xml", "wb") as f:
        fileOut.write(f)

#root[2].

if __name__ == "__main__":
    main()