Bgl2Xml is a command line decompiler for FS9 and FSX bgl scenery files.  It has no GUI insterface.   If you want a GUI version then please use Bgl2Xml_GUI.exe

Bgl2Xml.exe program is a simple interface to the Scenery Design Engine.  The version packaged here is Version 1.3.1  

INSTALL & REMOVAL
This program is installed as part of the Bgl2Xml package.  Removal of this package will remove this.  Please see the package readme for details of installation and removal


USAGE

You may use the command line or a batch file.  Bgl2Xml takes up to three parameters.  These can be in any order.  Only the source file parameter is mandatory.  If path names contain spaces then the path must be enclosed in qoutes (")

	/s "sourcepath" is mandatory and sets the source bgl file
	/d "destinationpath" is optional and sets the destination file
	/m  sets whether models are extracted and saved or not   /m t to extract  /m f to not extract

if /d is not specified then the output xml is the in the source folder with the source filename + .xml
if /m is not specified then models will be extracted into the source folder

	e.g Bgl2Xml.exe /s "C:\My Folder\source.bgl" /d "D:\Results Folder" /m f  


LEGAL BITS
This software is released as freeware and it may not be used whole or in part in any other software without the written permission of the author.  This software is provided as-is and the author cannot be held responsible for any effects it may have on you, your computer, or your flight simulator installation.

Note that you need the permission of copyright holders, or own the copyright yourself of any scenery file that is modified with this program.  We cannot be held responsible for any legal actions taken against you for any breaches of copyright or ownership which may result form the use of this program.

The developer respects the copyright of those third party libraries used with this software.  This software application and it's libraries are copyright ScruffyDuck Software, or the developers of the third party libraries used.


CONTACT DETAILS
Jon Masterson
jon@scruffyduck.co.uk
www.scruffyduckscenery.co.uk

