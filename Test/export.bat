@echo off

echo Export Inkscape file using EzInkscape module...

set INKSCAPE="/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
set EZ_INKSCAPE="../ezinkscape.py"
set INPUT="drawing.svg"
set CLASS="Assets"
set SOURCE="Output/Sources"
set LANGUAGE="m"
set ANCHOR="center"
set QUERY="xy"
set TEXTURES="Output/Textures"
set DPI=90

python %EZ_INKSCAPE% -inkscape=%INKSCAPE% -input=%INPUT% -class=%CLASS% -source=%SOURCE% -language=%LANGUAGE% -anchor=%ANCHOR% -query=%QUERY% -textures=%TEXTURES% -dpi=%DPI%

echo Done...
