# OldAirac - FSX NAVAIDS to MSFS/X-Plane
Ports FSX NAVAID(NDB/VOR/ILS) to MSFS/X-Plane so you can enjoy not RNAV flights again

Great, but where find charts? - I use Jeppview 3.0 it comes with Airac from 2009 - [can be found here](https://rutracker.org/forum/viewtopic.php?t=1546438), but you need modify nav base cfg, so it will think you have correct navbase, file can be found in 
    **C:\ProgramData\Jeppesen\Common\TerminalCharts\charts.ini**
maybe later i will create a script which will update it automatically

## Structure
BGL2XML - used for FSX original file convertion to XML
FSX-Data - MSFS addon for SDK, for bgl compile
XmlDataFSX - extracted FSX navbase to XML format, all .py scripts use this(you can try extract your data from different flight sim i.e. Prepar see ConvertToXML.py)
