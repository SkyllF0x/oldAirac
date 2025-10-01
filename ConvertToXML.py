from math import *
import subprocess
from pathlib import Path
import os
import shlex
import re

NAVAIDS = re.compile("NVX(\S*).bgl")
AIRPORTS = re.compile("APX(\S*).bgl")
OUTPUT = "XmlDataFSX"

def main():
    if not os.path.exists(OUTPUT):
        os.mkdir(OUTPUT)


    for root, subFolders, files in os.walk("./scenery"):
        for file in files:
            if NAVAIDS.fullmatch(file) or AIRPORTS.fullmatch(file):
                head, tail = os.path.split(root)
                scenerySub = os.path.split(head)[1]
                sourcePath = os.path.join(root, file)
                destinationPath = os.path.join(OUTPUT, scenerySub, Path(file).with_suffix(".xml"))

                outputSubdirectory = os.path.join(OUTPUT, scenerySub)
                if not os.path.exists(os.path.join(OUTPUT, scenerySub)):
                    os.mkdir(outputSubdirectory)

                cmd = '"Bgl2Xml/Bgl2Xml.exe" /s "{}" /d "{}" /m f'.format(sourcePath, destinationPath)
                subprocess.run(shlex.split(cmd))

if __name__ == "__main__":
    main()